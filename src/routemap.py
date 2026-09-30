"""Image 3 · the Route Map: a cropped, night-mode view of the city map with airport-style wayfinding.

Independent of the Memory Card (memcard.py): own module, own <svg>, no shared state.
The base map is inlined ONCE per page by base_defs(); every Route Map <use>s it.
"""
import json, math, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import citymap

HERE_DIR = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE_DIR, "..", "data", "saga.json"), encoding="utf-8"))
PTS = {c: (x, y) for c, x, y in json.load(open(os.path.join(HERE_DIR, "..", "data", "map_points.json"), encoding="utf-8"))}
STATIONS = ["ARCH", "STEP", "LAMP", "RUG", "HEART", "PILLAR", "WINDOW", "STAIR", "BALCONY", "TOP"]
LETTERS = [s[0] for s in STATIONS]

MW, MH = citymap.W, citymap.H          # map coordinate space (1500 x 1160)
VW, VH, STRIP = 300, 240, 60           # map window + station strip = 300 x 300
CROP_W, CROP_H, MARGIN = 520, 416, 40

# overlay palette (also exposed as CSS custom properties on the page; attributes are the standalone defaults)
NIGHT = "#0f1d2e"
COL = {"here": "#ff2d95", "next": "#00e5ff", "traveled": "#9cff57", "future": "#8a94a6", "label": "#ffffff", "pill": NIGHT}
SATURATE, DIM, OVERLAY = 0.15, 0.8, 0.55   # filter: saturate 0.15, then scale RGB by 0.8; then NIGHT overlay at 55%

FONT = "Nunito,Arial,sans-serif"
esc = lambda s: html.escape(s, quote=True)

def nxt(n):
    return n + 1 if n < 100 else 1

# ------------------------------------------------------------------ page-level base map (once per page)
def base_defs():
    """Hidden SVG with the night-mode base map as <symbol id="cm-base">.
    Hidden with width/height 0 rather than display:none. Chrome renders either way, but Firefox has
    historically not applied patterns/filters that live inside a display:none subtree."""
    return (f'<svg class="cm-defs" width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false">'
            f'<defs><filter id="cm-night" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feColorMatrix type="saturate" values="{SATURATE}"/>'
            f'<feComponentTransfer><feFuncR type="linear" slope="{DIM}"/><feFuncG type="linear" slope="{DIM}"/><feFuncB type="linear" slope="{DIM}"/></feComponentTransfer></filter>'
            f'<symbol id="cm-base" viewBox="0 0 {MW} {MH}"><g filter="url(#cm-night)">{citymap.body(route=False, chrome=False)}</g>'
            f'<rect width="{MW}" height="{MH}" fill="{NIGHT}" opacity="{OVERLAY}"/></symbol></defs></svg>')

# ------------------------------------------------------------------ geometry
def crop(n):
    """520x416 window centered between here and next, grown (same aspect) until both points
    have >= 40px margin, then clamped to the map bounds."""
    (x1, y1), (x2, y2) = PTS[n], PTS[nxt(n)]
    w = max(CROP_W, abs(x2 - x1) + 2 * MARGIN, (abs(y2 - y1) + 2 * MARGIN) * CROP_W / CROP_H)
    h = w * CROP_H / CROP_W
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    x0 = min(max(cx - w / 2, 0), MW - w)
    y0 = min(max(cy - h / 2, 0), MH - h)
    return round(x0, 1), round(y0, 1), round(w, 1), round(h, 1)

def project(pt, cr):
    x0, y0, w, h = cr
    return round((pt[0] - x0) * VW / w, 1), round((pt[1] - y0) * VH / h, 1)

# ------------------------------------------------------------------ small drawing helpers
def text_w(s, size):  # generous width estimate for bold Nunito / Arial fallback
    wd = lambda ch: (0.28 if ch in " .,':;|!il·" else 0.36 if ch in "()-/" else 0.95 if ch in "→▸MW" else
                     0.74 if ch.isupper() else 0.6 if ch.isdigit() else 0.57)
    return sum(wd(ch) for ch in s) * size * 1.1

LABEL = 10.5          # label font size in the 300px map window
MAXW = VW - 16        # widest a pill may get

def wrap_label(head, name, size=LABEL):
    """[head, name] lines; the name wraps onto a second line if it is too wide."""
    if text_w(name, size) + 12 <= MAXW:
        return [head, name]
    words, a = name.split(" "), ""
    for k in range(len(words), 0, -1):
        a = " ".join(words[:k])
        if text_w(a, size) + 12 <= MAXW: break
    return [head, a, " ".join(words[k:])]

def pill_box(lines, size=LABEL):
    return max(text_w(t, size) for t in lines) + 12, len(lines) * (size + 3) + 5

def pill(x, y, lines, border, colors, size=LABEL):
    """Dark rounded label at (x, y) (already clamped by the caller)."""
    w, h = pill_box(lines, size)
    out = f'<rect class="rm-pill" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{min(8, h/2):.1f}" fill="{COL["pill"]}" stroke="{border}" stroke-width="1.5"/>'
    for k, t in enumerate(lines):
        c = colors[min(k, len(colors) - 1)]
        out += f'<text x="{x+6:.1f}" y="{y + 3 + size + k*(size+3) - 1.5:.1f}" font-size="{size}" font-weight="800" font-family="{FONT}" fill="{c}">{esc(t)}</text>'
    return out

def candidates(ax, ay, w, h, gap):
    """Pill positions around an anchor point, clamped into the window: (x, y, w, h, drift)."""
    raw = [(ax - w / 2, ay - gap - h), (ax - w / 2, ay + gap), (ax + gap, ay - h / 2), (ax - gap - w, ay - h / 2),
           (ax - w + 20, ay - gap - h), (ax - 20, ay - gap - h), (ax - w + 20, ay + gap), (ax - 20, ay + gap),
           (ax - w / 2, 4), (ax - w / 2, VH - 4 - h)]  # window edges, joined by a leader line
    out = []
    for x, y in raw:
        cx, cy = min(max(x, 4), VW - 4 - w), min(max(y, 4), VH - 4 - h)
        out.append((cx, cy, w, h, abs(cx - x) + abs(cy - y)))
    return out

def hits_circle(box, cx, cy, r):
    x, y, w, h = box[:4]
    nx, ny = min(max(cx, x), x + w), min(max(cy, y), y + h)
    return math.dist((nx, ny), (cx, cy)) < r

def place_labels(here, nextp, hsize, nsize):
    """Choose non-overlapping spots for the two pills, keeping both dots and the leg visible."""
    (hx, hy), (nx_, ny_) = here, nextp
    best = None
    for hb in candidates(hx, hy, *hsize, 14):
        for nb in candidates(nx_, ny_, *nsize, 10):
            cost = hb[4] + nb[4]
            if overlaps(hb, nb): cost += 1000
            for b in (hb, nb):
                if hits_circle(b, hx, hy, 13): cost += 800
                if hits_circle(b, nx_, ny_, 9): cost += 600
            # keep the leg visible: penalise a pill sitting on its midpoint
            mx, my = (hx + nx_) / 2, (hy + ny_) / 2
            if hits_circle(hb, mx, my, 4) or hits_circle(nb, mx, my, 4): cost += 150
            cost += 0.02 * (math.dist((hb[0] + hb[2] / 2, hb[1] + hb[3] / 2), (hx, hy)) + math.dist((nb[0] + nb[2] / 2, nb[1] + nb[3] / 2), (nx_, ny_)))
            if best is None or cost < best[0]: best = (cost, hb, nb)
    return best[1], best[2]

def overlaps(a, b, pad=3):
    return not (a[0] + a[2] + pad < b[0] or b[0] + b[2] + pad < a[0] or a[1] + a[3] + pad < b[1] or b[1] + b[3] + pad < a[1])

def arrowhead(x1, y1, x2, y2, stop, size, color, cls, op=1):
    """Arrowhead whose tip sits `stop` px short of (x2,y2), pointing from (x1,y1)."""
    d = math.dist((x1, y1), (x2, y2)) or 1
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    tx, ty = x2 - ux * stop, y2 - uy * stop
    bx, by = tx - ux * size, ty - uy * size
    px, py = -uy * size * 0.6, ux * size * 0.6
    return (f'<polygon class="{cls}" points="{tx:.1f},{ty:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{color}" '
            f'stroke="{NIGHT}" stroke-width="1" opacity="{op}"/>'), (bx, by)

# ------------------------------------------------------------------ the Route Map
def route_map(n, i, stations=None):
    """Route Map SVG for chapter n, frame i (0..9; i=9 is the wide Frame 0)."""
    m = nxt(n)
    ch, nch = D[n - 1], D[m - 1]
    cr = crop(n)
    hx, hy = project(PTS[n], cr)
    nx_, ny_ = project(PTS[m], cr)
    last = i == 9
    o = []

    # --- map window: base map (cropped) ---
    x0, y0, w, h = cr
    o.append(f'<svg x="0" y="0" width="{VW}" height="{VH}" viewBox="{x0} {y0} {w} {h}" preserveAspectRatio="xMidYMid slice">'
             f'<use href="#cm-base" xlink:href="#cm-base" width="{MW}" height="{MH}"/></svg>')

    # --- overlays, in window pixels so sizes stay constant whatever the crop zoom ---
    ov = []
    order = list(range(1, 101))
    pos = {c: project(PTS[c], cr) for c in order}
    inview = lambda c: -12 <= pos[c][0] <= VW + 12 and -12 <= pos[c][1] <= VH + 12

    def runs(seq):
        """Split a route into polylines that touch the window (keeps one point beyond each edge)."""
        keep = [k for k, c in enumerate(seq) if inview(c) or (k > 0 and inview(seq[k - 1])) or (k + 1 < len(seq) and inview(seq[k + 1]))]
        out, cur = [], []
        for k in keep:
            if cur and k != cur[-1] + 1: out.append(cur); cur = []
            cur.append(k)
        return [[seq[k] for k in r] for r in out + ([cur] if cur else []) if len(r) > 1]
    pts = lambda seq: " ".join(f"{pos[c][0]},{pos[c][1]}" for c in seq)
    # future: hollow, faint, dotted (after the next stop)
    fut = [c for c in order if c > m] if m != 1 else []
    for r in runs([m] + fut if fut else []):
        ov.append(f'<polyline class="rm-future" points="{pts(r)}" fill="none" stroke="{COL["future"]}" stroke-width="1.5" '
                  f'stroke-dasharray="1 4" stroke-linecap="round" opacity="0.6"/>')
    ov += [f'<circle class="rm-future" cx="{pos[c][0]}" cy="{pos[c][1]}" r="2.6" fill="none" stroke="{COL["future"]}" '
           f'stroke-width="1.2" stroke-dasharray="1.6 1.4" opacity="0.8"/>' for c in fut if inview(c)]
    # traveled: filled dots joined by a solid line, ending at you
    trav = list(range(1, n))
    for r in runs(trav + [n] if trav else []):
        ov.append(f'<polyline class="rm-traveled" points="{pts(r)}" fill="none" stroke="{COL["traveled"]}" stroke-width="2.5" '
                  f'stroke-linejoin="round" stroke-linecap="round" opacity="0.85"/>')
    ov += [f'<circle class="rm-traveled" cx="{pos[c][0]}" cy="{pos[c][1]}" r="2.8" fill="{COL["traveled"]}" stroke="{NIGHT}" stroke-width="1"/>'
           for c in trav if inview(c)]
    # next leg: bold dashed line with arrowhead (emphasised on Frame 0)
    op, sw = (1, 4.5) if last else (0.5, 3.5)
    head, (bx, by) = arrowhead(hx, hy, nx_, ny_, 7, 9 if last else 7.5, COL["next"], "rm-next", op)
    ov.append(f'<path class="rm-next rm-leg" d="M{hx},{hy} L{bx:.1f},{by:.1f}" fill="none" stroke="{COL["next"]}" stroke-width="{sw}" '
              f'stroke-dasharray="10 8" stroke-linecap="round" opacity="{op}" data-from="{PTS[n][0]},{PTS[n][1]}" data-to="{PTS[m][0]},{PTS[m][1]}"/>')
    ov.append(head)
    ov.append(f'<circle class="rm-next rm-next-dot" cx="{nx_}" cy="{ny_}" r="5.5" fill="{NIGHT}" stroke="{COL["next"]}" stroke-width="2.5"/>')
    # YOU ARE HERE pin: pulse, white ring (contrast vs map), dark ring, magenta core
    ov.append(f'<circle class="rm-pulse" cx="{hx}" cy="{hy}" r="11" fill="none" stroke="{COL["here"]}" stroke-width="3"/>')
    ov.append(f'<circle cx="{hx}" cy="{hy}" r="9.5" fill="#fff"/><circle cx="{hx}" cy="{hy}" r="7.8" fill="{NIGHT}"/>'
              f'<circle class="rm-here rm-pin" cx="{hx}" cy="{hy}" r="6" fill="{COL["here"]}" data-at="{PTS[n][0]},{PTS[n][1]}"/>')

    # labels: YOU ARE HERE pill near the pin, NEXT pill near the next stop, never covering either dot
    here_lines = wrap_label("YOU ARE HERE", f"Ch.{n} · {ch['locus']}")
    nlab = wrap_label("NEXT ▸", f"Ch.{m} · {nch['locus']}")
    nlab = [nlab[0] + " " + nlab[1]] + nlab[2:] if text_w(nlab[0] + " " + nlab[1], LABEL) + 12 <= MAXW else nlab
    if last: nlab = nlab + ["→ next chapter"]
    hbox, nbox = place_labels((hx, hy), (nx_, ny_), pill_box(here_lines), pill_box(nlab))
    hp_svg = pill(hbox[0], hbox[1], here_lines, COL["here"], [COL["here"], COL["label"]])
    np_svg = pill(nbox[0], nbox[1], nlab, COL["next"], [COL["next"], COL["next"], COL["label"]] if len(nlab) == 3 and last else [COL["next"], COL["label"]] if last else [COL["next"]])
    # leaders from each dot to the nearest point of its pill
    for (ax, ay), b, col in (((hx, hy), hbox, COL["here"]), ((nx_, ny_), nbox, COL["next"])):
        lx, ly = min(max(ax, b[0] + 6), b[0] + b[2] - 6), min(max(ay, b[1]), b[1] + b[3])
        ov.insert(0, f'<line x1="{ax}" y1="{ay}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{col}" stroke-width="1.5" opacity="0.9"/>')
    ov += [np_svg, hp_svg]
    o.append(f'<svg x="0" y="0" width="{VW}" height="{VH}" viewBox="0 0 {VW} {VH}">{"".join(ov)}</svg>')

    # --- station strip (inside the building) ---
    o.append(station_strip(n, i, m))
    o.append(f'<rect x="1" y="1" width="{VW-2}" height="{VW-2}" rx="10" fill="none" stroke="{NIGHT}" stroke-width="2"/>')

    st_name = STATIONS[i].title()
    where = f"; {stations[i]}" if stations else ""
    title = f"Route map · Chapter {n}, {ch['locus']}, station {i+1} {st_name}"
    desc = (f"Chapter {n}, {ch['locus']}, station {i+1} {st_name}{where}. Next: {nch['locus']} (Chapter {m})."
            + (" The next leg leaves this landmark." if last else f" Next station: {i+2} {STATIONS[i+1].title()}."))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {VW} {VW}" class="routemap" role="img" '
            f'data-ch="{n}" data-frame="{i}" data-crop="{x0},{y0},{w},{h}">'
            f'<title>{esc(title)}</title><desc>{esc(desc)}</desc>'
            f'<rect width="{VW}" height="{VW}" rx="10" fill="{NIGHT}"/>{"".join(o)}</svg>')

def station_strip(n, i, m):
    y0 = VH
    gap = 27
    xs = [22 + k * gap for k in range(10)]
    cy = y0 + 30
    o = [f'<rect x="0" y="{y0}" width="{VW}" height="{STRIP}" fill="#0a1522"/>',
         f'<line x1="0" y1="{y0}" x2="{VW}" y2="{y0}" stroke="#2b3d55" stroke-width="1.5"/>',
         f'<text x="8" y="{y0+13}" font-size="8.5" font-weight="800" font-family="{FONT}" fill="#c9d3e3" letter-spacing="0.6">'
         f'INSIDE · STATION {i+1} {STATIONS[i]}</text>']
    # traveled solid line through past stations up to here
    if i > 0:
        o.append(f'<line x1="{xs[0]}" y1="{cy}" x2="{xs[i]}" y2="{cy}" stroke="{COL["traveled"]}" stroke-width="2.5" opacity="0.85"/>')
    # dotted line to the next station, or off the right edge toward the next landmark on Frame 0
    if i < 9:
        o.append(f'<line class="rm-strip-next" x1="{xs[i]+8}" y1="{cy}" x2="{xs[i+1]-7}" y2="{cy}" stroke="{COL["next"]}" stroke-width="2.5" '
                 f'stroke-dasharray="3 3" stroke-linecap="round"/>')
        if i < 8:
            o.append(f'<line x1="{xs[i+1]+6}" y1="{cy}" x2="{xs[9]}" y2="{cy}" stroke="{COL["future"]}" stroke-width="1.2" stroke-dasharray="1 4" opacity="0.6"/>')
    else:
        o.append(f'<line class="rm-strip-next" x1="{xs[9]+9}" y1="{cy}" x2="{VW-9}" y2="{cy}" stroke="{COL["next"]}" stroke-width="3" '
                 f'stroke-dasharray="3 3" stroke-linecap="round"/>'
                 f'<polygon points="{VW-2},{cy} {VW-10},{cy-5} {VW-10},{cy+5}" fill="{COL["next"]}"/>'
                 f'<text x="{VW-6}" y="{y0+13}" text-anchor="end" font-size="8.5" font-weight="800" font-family="{FONT}" fill="{COL["next"]}">Ch.{m} ▸</text>')
    for k, x in enumerate(xs):
        if k == i:
            o.append(f'<circle cx="{x}" cy="{cy}" r="9" fill="#fff"/><circle class="rm-here rm-strip-here" data-k="{k}" cx="{x}" cy="{cy}" r="7" fill="{COL["here"]}" stroke="{NIGHT}" stroke-width="1.5"/>')
        elif k < i:
            o.append(f'<circle class="rm-traveled" cx="{x}" cy="{cy}" r="5" fill="{COL["traveled"]}" stroke="{NIGHT}" stroke-width="1"/>')
        else:
            cls, col = ("rm-next", COL["next"]) if k == i + 1 else ("rm-future", COL["future"])
            o.append(f'<circle class="{cls}" cx="{x}" cy="{cy}" r="5" fill="{NIGHT}" stroke="{col}" stroke-width="1.5"/>')
        o.append(f'<text x="{x}" y="{y0+54}" text-anchor="middle" font-size="9" font-weight="800" font-family="{FONT}" '
                 f'fill="{"#fff" if k == i else "#c9d3e3"}">{LETTERS[k]}</text>')
    return "".join(o)

# ------------------------------------------------------------------ contrast
def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(rgb):
    r, g, b = (_lin(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def hex_rgb(hx):
    hx = hx.lstrip("#")
    if len(hx) == 3: hx = "".join(ch * 2 for ch in hx)
    return tuple(int(hx[k:k + 2], 16) / 255 for k in (0, 2, 4))

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

def darkened(rgb):
    """Emulate the night-mode pipeline in sRGB space: feColorMatrix saturate, slope DIM, NIGHT overlay."""
    s = SATURATE
    r, g, b = rgb
    m = [(0.213 + 0.787 * s, 0.715 - 0.715 * s, 0.072 - 0.072 * s),
         (0.213 - 0.213 * s, 0.715 + 0.285 * s, 0.072 - 0.072 * s),
         (0.213 - 0.213 * s, 0.715 - 0.715 * s, 0.072 + 0.928 * s)]
    sat = [min(1, max(0, row[0] * r + row[1] * g + row[2] * b)) * DIM for row in m]
    nt = hex_rgb(NIGHT)
    return tuple(OVERLAY * nt[k] + (1 - OVERLAY) * sat[k] for k in range(3))

def contrast_report():
    """Worst case = the brightest colour anywhere in the darkened base map."""
    import re
    cols = set(re.findall(r'(?:fill|stroke|stop-color)="(#[0-9a-fA-F]{3,6})"', citymap.body(route=False, chrome=False)))
    dark = sorted((darkened(hex_rgb(c)) for c in cols), key=lum)
    lightest, darkest = dark[-1], dark[0]
    pill_bg, white = hex_rgb(COL["pill"]), (1, 1, 1)
    rows = [
        ("pin outer ring (white) vs lightest darkened map", ratio(white, lightest)),
        ("pin core (--here) vs its dark ring", ratio(hex_rgb(COL["here"]), pill_bg)),
        ("label text white on pill", ratio(white, pill_bg)),
        ("label 'YOU ARE HERE' (--here) on pill", ratio(hex_rgb(COL["here"]), pill_bg)),
        ("label NEXT (--next) on pill", ratio(hex_rgb(COL["next"]), pill_bg)),
        ("info: --next leg vs lightest darkened map", ratio(hex_rgb(COL["next"]), lightest)),
        ("info: --next leg vs darkest darkened map", ratio(hex_rgb(COL["next"]), darkest)),
        ("info: --traveled vs lightest darkened map", ratio(hex_rgb(COL["traveled"]), lightest)),
        ("info: --here core vs lightest darkened map", ratio(hex_rgb(COL["here"]), lightest)),
    ]
    return rows

if __name__ == "__main__":
    for name, r in contrast_report():
        if r is not None: print(f"{r:5.2f}:1  {name}")
