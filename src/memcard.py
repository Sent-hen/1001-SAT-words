"""Image 2 · the Memory Card: the absurd OAES link image (word k -> word k+1) drawn ON the loci
station of word k, in a "dream" style that clearly differs from the Story Panel.

Independent of the Route Map (routemap.py): own module, own <svg>, no shared state or page defs.
Data: content/cards/cards_NNN-MMM.txt via content.parse_cards(); falls back to a generic card.
"""
import glob, math, os, random, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import INK, P, C, E, L, T, g, sparkle, spark
import content, objects
from objects import shade

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
STATIONS = ["ARCH", "STEP", "LAMP", "RUG", "HEART", "PILLAR", "WINDOW", "STAIR", "BALCONY", "TOP"]
# district tints (same values as citymap.DISTRICTS; kept here so this module needs nothing from the map)
TINTS = ["#2f6db5", "#1f8a8a", "#e0533b", "#3f9b4a", "#d18b1f", "#8a5a2b", "#b8923a", "#6b4fa0", "#c0262d", "#157a4f"]
ARROW, GOLD, CREAM = "#ff2d95", "#f4c542", "#fff6c9"
S = 300
FLOOR = 262            # station stage floor line (stage = bottom 40%: y 180..300)
FOOT = 266             # badge / OAES row starts here
BANGERS = "'Bangers',Impact,'Arial Black',sans-serif"
esc = lambda s: html.escape(s, quote=True)

_D, _CH, _CARDS = content.D, None, None

def data():
    global _CH, _CARDS
    if _CH is None:
        _CH = content.parse(glob.glob(os.path.join(ROOT, "content", "b*.txt")))
        _CARDS = content.parse_cards(glob.glob(os.path.join(ROOT, "content", "cards", "cards_*.txt")))
    return _CH, _CARDS

# ------------------------------------------------------------------ station templates
# One function per station, drawn the SAME way on every card of every chapter (only the tint changes).
# Each returns (svg, seat) where seat = (x, y) is where object A stands.
def _stone(t):  return shade(t, 1.55)
def _mid(t):    return shade(t, 1.2)
def _dark(t):   return shade(t, 0.7)

def st_arch(t):
    o = P(f"M34,{FLOOR} V206 Q34,168 115,160 Q196,168 196,206 V{FLOOR} H172 V210 Q172,186 115,182 Q58,186 58,210 V{FLOOR} Z", _stone(t), 3)
    o += "".join(L(x1, y1, x2, y2, _dark(t), 1.5) for x1, y1, x2, y2 in [(40, 228, 58, 228), (172, 228, 190, 228), (40, 246, 58, 246), (172, 246, 190, 246)])
    o += P("M103,158 L127,158 L123,182 L107,182 Z", _mid(t), 2.5)
    return o, (115, 160)

def st_step(t):
    o = ""
    for k, (w, y) in enumerate([(160, 244), (126, 226), (92, 208)]):
        o += f'<rect x="{115-w/2}" y="{y}" width="{w}" height="{18 if k else FLOOR-y}" fill="{_stone(t) if k % 2 == 0 else _mid(t)}" stroke="{INK}" stroke-width="3"/>'
    o += C(84, 236, 5, "none", 2.5, _dark(t)) + L(84, 241, 84, 250, _dark(t), 3)
    return o, (115, 208)

def st_lamp(t):
    o = f'<rect x="14" y="186" width="10" height="{FLOOR-186}" fill="{_mid(t)}" stroke="{INK}" stroke-width="2.5"/>'
    o += P("M24,194 H112 Q120,194 118,200", "none", 5, _dark(t)) + L(115, 200, 115, 210, INK, 2)
    o += f'<circle cx="115" cy="232" r="34" fill="#ffd84d" opacity="0.28"/>'
    o += P("M101,212 H129 L125,216 H105 Z", _dark(t), 2) + P("M104,216 H126 L130,246 H100 Z", "#ffe9a8", 3) + L(115, 216, 115, 246, _dark(t), 2)
    o += P("M98,246 H132 L126,254 H104 Z", _dark(t), 2.5)
    return o, (115, 211)

def st_rug(t):
    o = P(f"M22,{FLOOR-2} L56,232 H206 L176,{FLOOR-2} Z", _mid(t), 3)
    o += P(f"M40,{FLOOR-7} L63,237 H196 L167,{FLOOR-7} Z", "none", 2, CREAM)
    o += P(f"M114,237 L140,247 L114,{FLOOR-7} L88,247 Z", _stone(t), 2)
    o += "".join(L(x, FLOOR - 2, x - 2, FLOOR + 3, CREAM, 2) for x in range(30, 176, 12))
    return o, (114, 248)

def st_heart(t):
    o = P(f"M49,234 V{FLOOR-4} Q115,{FLOOR+10} 181,{FLOOR-4} V234", _mid(t), 3) + E(115, 234, 66, 13, _stone(t), 3)
    o += P("M115,258 Q98,248 101,241 Q105,234 115,241 Q125,234 129,241 Q132,248 115,258 Z", "#ff5fa2", 2)
    return o, (115, 234)

def st_pillar(t):
    o = f'<rect x="99" y="192" width="32" height="{FLOOR-192}" fill="{_stone(t)}" stroke="{INK}" stroke-width="3"/>'
    o += "".join(L(x, 196, x, FLOOR - 4, _dark(t), 1.5) for x in (107, 115, 123))
    o += f'<rect x="89" y="180" width="52" height="12" rx="2" fill="{_mid(t)}" stroke="{INK}" stroke-width="3"/>'
    o += f'<rect x="91" y="{FLOOR-10}" width="48" height="10" fill="{_mid(t)}" stroke="{INK}" stroke-width="3"/>'
    return o, (115, 180)

def st_window(t):
    o = P(f"M62,{FLOOR-8} V210 Q62,170 115,170 Q168,170 168,210 V{FLOOR-8} Z", _stone(t), 3)
    o += P(f"M74,{FLOOR-8} V212 Q74,182 115,182 Q156,182 156,212 V{FLOOR-8} Z", "#1c2a5a", 2.5)
    o += "".join(C(x, y, 1.4, "#fff", 0) for x, y in [(90, 200), (138, 196), (128, 222), (96, 232)])
    o += L(115, 182, 115, FLOOR - 8, _stone(t), 3) + L(74, 222, 156, 222, _stone(t), 3)
    o += f'<rect x="54" y="{FLOOR-10}" width="122" height="10" fill="{_mid(t)}" stroke="{INK}" stroke-width="3"/>'
    return o, (115, FLOOR - 10)

def st_stair(t):
    o = ""
    for k in range(5):
        x, y = 30 + k * 30, FLOOR - (k + 1) * 14
        o += f'<rect x="{x}" y="{y}" width="{200-x}" height="14" fill="{_stone(t) if k % 2 == 0 else _mid(t)}" stroke="{INK}" stroke-width="2.5"/>'
    o += P(f"M36,{FLOOR-26} L186,{FLOOR-96}", "none", 3, _dark(t)) + L(36, FLOOR - 26, 36, FLOOR - 4, _dark(t), 3) + L(186, FLOOR - 96, 186, FLOOR - 72, _dark(t), 3)
    return o, (172, FLOOR - 70)

def st_balcony(t):
    o = f'<rect x="16" y="{FLOOR-8}" width="196" height="8" fill="{_mid(t)}" stroke="{INK}" stroke-width="2.5"/>'
    o += "".join(P(f"M{x-5},{FLOOR-8} Q{x-8},{FLOOR-22} {x},{FLOOR-26} Q{x+8},{FLOOR-22} {x+5},{FLOOR-8} Z M{x-3},{FLOOR-26} V{FLOOR-34} H{x+3} V{FLOOR-26}", _stone(t), 2) for x in range(28, 206, 20))
    o += f'<rect x="12" y="{FLOOR-42}" width="204" height="9" rx="3" fill="{_mid(t)}" stroke="{INK}" stroke-width="3"/>'
    return o, (115, FLOOR - 42)

def st_top(t):
    o = f'<rect x="54" y="{FLOOR-16}" width="122" height="16" fill="{_mid(t)}" stroke="{INK}" stroke-width="3"/>'
    o += P(f"M58,{FLOOR-16} Q58,200 115,196 Q172,200 172,{FLOOR-16} Z", _stone(t), 3)
    o += P(f"M78,{FLOOR-16} Q80,214 115,204", "none", 2, CREAM)
    o += L(115, 196, 115, 176, _dark(t), 3.5) + C(115, 180, 4, GOLD, 1.5)
    o += P("M109,168 A8,8 0 1 0 121,168 A6,6 0 1 1 109,168 Z", GOLD, 1.5)
    return o, (115, 166)

STATION_FNS = [st_arch, st_step, st_lamp, st_rug, st_heart, st_pillar, st_window, st_stair, st_balcony, st_top]

def station_stage(k, tint):
    """Station template k (0..9) tinted with the district colour -> (svg, seat)."""
    body, seat = STATION_FNS[k](tint)
    floor = f'<rect x="8" y="{FLOOR}" width="{S-16}" height="{S-8-FLOOR}" fill="{_dark(tint)}" opacity="0.55"/>'
    return f'<g class="mc-station" data-station="{STATIONS[k]}">{floor}{body}</g>', seat

# ------------------------------------------------------------------ decoration
def background(uid):
    return (f'<defs><radialGradient id="{uid}-bg" cx="50%" cy="42%" r="70%"><stop offset="0" stop-color="#6b2fa0"/><stop offset="1" stop-color="#2a1450"/></radialGradient>'
            f'<radialGradient id="{uid}-gl" cx="50%" cy="45%" r="45%"><stop offset="0" stop-color="#ff9fc4" stop-opacity="0.45"/><stop offset="1" stop-color="#ff9fc4" stop-opacity="0"/></radialGradient></defs>'
            f'<rect x="3" y="3" width="{S-6}" height="{S-6}" rx="16" fill="url(#{uid}-bg)"/>'
            f'<rect x="3" y="3" width="{S-6}" height="{S-6}" rx="16" fill="url(#{uid}-gl)"/>')

def border():
    return (f'<rect x="3" y="3" width="{S-6}" height="{S-6}" rx="16" fill="none" stroke="{GOLD}" stroke-width="6"/>'
            f'<rect x="9.5" y="9.5" width="{S-19}" height="{S-19}" rx="11" fill="none" stroke="{CREAM}" stroke-width="2"/>')

def sparkles(seed):
    r = random.Random(seed)
    spots = [(r.randint(22, 278), r.randint(52, 172), r.choice([3, 4, 5])) for _ in range(7)]
    return '<g class="mc-sparkles" opacity="0.85">' + "".join(sparkle(x, y, s, "#fff6c9") for x, y, s in spots) + "</g>"

def title(wa, wb):
    txt = f"{wa.upper()} → {wb.upper()}"
    size = min(28, 256 / (len(txt) * 0.58))
    if size >= 16:
        return T(S / 2, 40, esc(txt), round(size, 1), "#fff", extra=f'class="mc-title" stroke="{INK}" stroke-width="4" paint-order="stroke" letter-spacing="1"')
    s2 = min(24, 256 / (max(len(wa) + 2, len(wb)) * 0.58))
    return (f'<text class="mc-title" x="{S/2}" y="32" font-size="{s2:.1f}" fill="#fff" text-anchor="middle" font-weight="700" font-family="{BANGERS}" '
            f'stroke="{INK}" stroke-width="4" paint-order="stroke" letter-spacing="1"><tspan x="{S/2}">{esc(wa.upper())} →</tspan>'
            f'<tspan x="{S/2}" dy="{s2*0.95:.1f}">{esc(wb.upper())}</tspan></text>')

def badge(k):
    name = STATIONS[k]
    w = 30 + len(name) * 8.2
    return (f'<g class="mc-badge" data-station="{name}"><rect x="14" y="{FOOT+4}" width="{w:.0f}" height="22" rx="11" fill="{INK}" stroke="{GOLD}" stroke-width="2"/>'
            + C(26, FOOT + 15, 8.5, GOLD, 1.5, INK)
            + T(26, FOOT + 19.5, str(k + 1), 11 if k < 9 else 9.5, INK, family="Arial,sans-serif", weight="800")
            + T(38, FOOT + 20.5, name, 14, "#fff", anchor="start", extra='letter-spacing="1"') + "</g>")

def oaes_chips(used):
    o = '<g class="mc-oaes">'
    for j, ch in enumerate("OAES"):
        x = 206 + j * 22
        on = ch in used
        o += (C(x, FOOT + 15, 9.5, GOLD if on else "#3a2060", 2, CREAM if on else "#7a6a9a")
              + T(x, FOOT + 20, ch, 13, INK if on else "#9a8ab8", extra=f'data-on="{int(on)}"'))
    return o + "</g>"

def oaes_from_link(link):
    low = link.lower()
    parens = " ".join(re.findall(r"\(([^)]*)\)", low))
    return [k for k, w in (("O", "out of proportion"), ("A", "action"), ("E", "exaggeration"), ("S", "substitution")) if w in parens]

def arrow(x1, y1, x2, y2, lift=46, label=None):
    """Thick curved link arrow from A to B (with a white under-stroke so it reads on any colour)."""
    cx, cy = (x1 + x2) / 2, min(y1, y2) - lift
    d = f"M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}"
    ang = math.atan2(y2 - cy, x2 - cx)
    hx, hy = x2 + 4 * math.cos(ang), y2 + 4 * math.sin(ang)
    head = " ".join(f"{hx + r * math.cos(ang + a):.1f},{hy + r * math.sin(ang + a):.1f}" for r, a in ((0, 0), (15, 2.6), (15, -2.6)))
    o = (f'<path d="{d}" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity="0.8"/>'
         f'<path class="mc-arrow" d="{d}" fill="none" stroke="{ARROW}" stroke-width="5" stroke-linecap="round"/>'
         f'<polygon points="{head}" fill="{ARROW}" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/>')
    if label:
        mx, my = 0.25 * x1 + 0.5 * cx + 0.25 * x2, 0.25 * y1 + 0.5 * cy + 0.25 * y2
        w = len(label) * 5.6 + 12
        mx = min(max(mx, 18 + w / 2), S - 18 - w / 2)
        o += (f'<rect x="{mx-w/2:.1f}" y="{my-19:.1f}" width="{w:.1f}" height="15" rx="7.5" fill="{INK}" opacity="0.85"/>'
              + T(round(mx, 1), round(my - 8, 1), esc(label), 10, "#fff", family="Nunito,Arial,sans-serif", weight="800"))
    return o

# ------------------------------------------------------------------ effects per action
def effect(act, ax, ay, bx, by, sb):
    act = act or ""
    if act.startswith("bursts") or "out-of" in act or "pours" in act or "spray" in act:
        return "".join(L(ax + 8 * math.cos(a), ay - 6 + 8 * math.sin(a), ax + 30 * math.cos(a), ay - 6 + 30 * math.sin(a), "#fff", 2.5, 'opacity="0.8"')
                       for a in [math.radians(d) for d in (-150, -120, -90, -60, -30)])
    if any(k in act for k in ("ride", "rocket", "chase", "fly", "throw", "zoom", "race", "drop", "rain", "fall")):
        return "".join(L(bx - 50 * sb - dx, by - 30 * sb + dy, bx - 26 * sb - dx, by - 30 * sb + dy, "#fff", 2.5, 'opacity="0.7"') for dx, dy in ((0, -10), (8, 0), (0, 10)))
    if any(k in act for k in ("smash", "stomp", "crush", "kick", "punch", "poke", "hit", "crash", "slam")):
        pts = " ".join(f"{bx - 30*sb + (16 if j % 2 == 0 else 7) * math.cos(j * math.pi / 6):.1f},{by - 60*sb + (16 if j % 2 == 0 else 7) * math.sin(j * math.pi / 6):.1f}" for j in range(12))
        return f'<polygon points="{pts}" fill="#ffd23f" stroke="{INK}" stroke-width="2"/>'
    if any(k in act for k in ("gulp", "swallow", "eat", "chomp", "bite", "into-mouth", "rolls-into")):
        return T(bx - 44 * sb, by - 8, "CHOMP!", 14, "#ffd23f", extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke" transform="rotate(-8 {bx-44*sb:.0f} {by-8})"')
    if any(k in act for k in ("hug", "love", "kiss")):
        return "".join(P(f"M{x},{y} q-5,-6 -8,-1 q-2,5 8,11 q10,-6 8,-11 q-3,-5 -8,1 Z", "#ff5fa2", 1.5) for x, y in ((bx - 34, by - 70), (bx + 26, by - 84)))
    if any(k in act for k in ("turn", "melt", "become", "transform", "morph", "hatch")):
        return "".join(sparkle((ax + bx) / 2 + dx, min(ay, by) - 70 + dy, 5, "#ffe066") for dx, dy in ((-18, 8), (0, -6), (18, 10)))
    if any(k in act for k in ("bounce", "boing", "pop")):
        return P(f"M{bx-40},{by-4} q10,-40 20,0 q8,-26 16,0", "none", 2, "#fff", 'stroke-dasharray="4 4"')
    return ""

# ------------------------------------------------------------------ the card
def _scale(scale, who):
    v = (scale or {}).get(who)
    return 1.3 if v in ("giant", "huge", "big") else 0.7 if v in ("tiny", "small") else 1.0

def memory_card(n, i):
    """Memory Card SVG for chapter n, frame i (0..9)."""
    CH, CARDS = data()
    words = _D[n - 1]["words"]
    wa = words[i]["word"]
    wb = words[i + 1]["word"] if i < 9 else (_D[n]["words"][0]["word"] if n < 100 else _D[0]["words"][0]["word"])
    link = CH[n]["frames"][i]["link"]
    tint = TINTS[(n - 1) // 10]
    uid = f"mc{n}-{i}"
    card = (CARDS.get(n) or {}).get(i + 1)
    stage, (sx, sy) = station_stage(i, tint)
    o = [background(uid), sparkles(n * 100 + i), stage]
    if card:
        used = card["oaes"] or oaes_from_link(link)
        sa, sb = _scale(card["scale"], "A"), _scale(card["scale"], "B")
        sb = min(sb, 1.25)
        bx, by = 236, 176 if i not in (7,) else 166
        b_svg, b_key = objects.draw(card["b"][0], bx, by, 0.9 * sb, card["b"][1])
        a_svg, a_key = objects.draw(card["a"][0], sx, sy, 0.78 * sa, card["a"][1])
        a_top = sy - 80 * 0.78 * sa
        eff = effect(card["act"], sx, a_top, bx, by, 0.9 * sb)
        x1, y1 = sx + 22, max(a_top + 18, 58)
        x2, y2 = bx - 38 * sb, by - 58 * sb
        label = (card["act"] or "").replace("-", " ") or None
        o += [f'<g class="mc-a" data-noun="{esc(card["a"][0])}" data-key="{a_key or ""}">{a_svg}</g>',
              f'<g class="mc-b" data-noun="{esc(card["b"][0])}" data-key="{b_key or ""}">{b_svg}</g>',
              eff, arrow(x1, y1, x2, y2, 40, label)]
        desc = (f"Station {i+1} {STATIONS[i].title()}: {card['a'][0]}" + (f" ({', '.join(card['a'][1])})" if card['a'][1] else "")
                + f" links to {card['b'][0]}" + (f" ({', '.join(card['b'][1])})" if card['b'][1] else "")
                + (f", {label}" if label else "") + f". OAES: {', '.join(used) or 'none'}.")
    else:  # generic fallback: station stage + a glowing spark + the two words + an arrow
        used = oaes_from_link(link)
        o += [spark(sx, sy - 22, wa, 14, 12), spark(236, 132, wb, 16, 12), arrow(sx + 18, sy - 44, 214, 126, 34)]
        desc = f"Station {i+1} {STATIONS[i].title()}: {wa} links to {wb}. OAES: {', '.join(used) or 'none'}."
    o += [f'<rect x="8" y="{FOOT}" width="{S-16}" height="{S-8-FOOT-2}" fill="{INK}" opacity="0.35"/>',
          title(wa, wb), badge(i), oaes_chips(used), border()]
    t = f"Memory card · {wa} → {wb}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" class="memcard" role="img" data-ch="{n}" data-frame="{i}" '
            f'data-station="{STATIONS[i]}" data-from="{esc(wa)}" data-to="{esc(wb)}" data-card="{1 if card else 0}">'
            f'<title>{esc(t)}</title><desc>{esc(desc)}</desc>{"".join(o)}</svg>')
