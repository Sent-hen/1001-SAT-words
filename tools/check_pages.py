"""Acceptance checks for the three-images pages (docs/TASK_three_images_per_frame.md, section 7).

    python tools/check_pages.py            # static checks on all 100 pages + contrast report
    python tools/check_pages.py --browser  # + Playwright toggle test and screenshots to docs/screens/

Exit code 0 only if every check passes.
"""
import glob, hashlib, html, json, math, os, re, subprocess, sys
from xml.dom import minidom

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import content, routemap

STATIONS = ["ARCH", "STEP", "LAMP", "RUG", "HEART", "PILLAR", "WINDOW", "STAIR", "BALCONY", "TOP"]
MAX_BYTES = 700 * 1024
D = content.D
CH = content.parse(glob.glob(os.path.join(ROOT, "content", "b*.txt")))
PTS = {c: (x, y) for c, x, y in json.load(open(os.path.join(ROOT, "data", "map_points.json"), encoding="utf-8"))}
fails, notes = [], []

def fail(msg):
    fails.append(msg)

# ------------------------------------------------------------------ helpers
def top_level_svgs(doc):
    """(start, end) spans of every <svg> that is not nested inside another <svg>."""
    spans, depth, start = [], 0, None
    for m in re.finditer(r"<svg\b|</svg>", doc):
        if m.group(0) == "<svg":
            if depth == 0: start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0: spans.append((start, m.end()))
    return spans

def attr(tag, name):
    m = re.search(r'\b%s="([^"]*)"' % re.escape(name), tag)
    return m.group(1) if m else None

def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True).stdout

def baseline_ref():
    """main if it has content/, else the first commit that added content/ (the branch baseline)."""
    if subprocess.run(["git", "cat-file", "-e", "main:content/b00.txt"], cwd=ROOT, capture_output=True).returncode == 0:
        return "main"
    return git("log", "--diff-filter=A", "--format=%H", "--", "content/b00.txt").decode().split()[-1]

norm = lambda b: b.replace(b"\r\n", b"\n")
sha = lambda b: hashlib.sha256(norm(b)).hexdigest()

# ------------------------------------------------------------------ 1. source text untouched
ref = baseline_ref()
protected = sorted(glob.glob(os.path.join(ROOT, "content", "b*.txt"))) + [os.path.join(ROOT, "data", "saga.json")] + sorted(glob.glob(os.path.join(ROOT, "*.md")))
changed = []
for p in protected:
    rel = os.path.relpath(p, ROOT).replace("\\", "/")
    old = git("show", f"{ref}:{rel}")
    if not old: notes.append(f"{rel}: not in {ref[:10]}, skipped"); continue
    if sha(old) != sha(open(p, "rb").read()): changed.append(rel)
if changed: fail(f"text files differ from {ref[:10]}: {changed}")
print(f"[text] {len(protected)} source/doc files checksum-equal to {ref if ref == 'main' else ref[:10]} (baseline)" if not changed else f"[text] CHANGED: {changed}")

# ------------------------------------------------------------------ per-page checks
sizes, n_svgs = {}, 0
for n in range(1, 101):
    path = os.path.join(ROOT, "chapters", f"chapter_{n:03d}.html")
    doc = open(path, encoding="utf-8").read()
    sizes[n] = os.path.getsize(path)
    if sizes[n] > MAX_BYTES: fail(f"ch{n}: {sizes[n]} bytes > {MAX_BYTES}")
    spans = top_level_svgs(doc)
    svgs = [doc[a:b] for a, b in spans]
    n_svgs += len(svgs)
    story = [s for s in svgs if 'class="routemap"' not in s[:400] and 'class="memcard"' not in s[:400] and 'class="cm-defs"' not in s[:200]]
    maps = [s for s in svgs if 'class="routemap"' in s[:400]]
    cards = [s for s in svgs if 'class="memcard"' in s[:400]]
    defs = [s for s in svgs if 'class="cm-defs"' in s[:200]]
    if (len(story), len(cards), len(maps), len(defs)) != (10, 10, 10, 1):
        fail(f"ch{n}: story/card/map/defs = {len(story)}/{len(cards)}/{len(maps)}/{len(defs)}, want 10/10/10/1")
    if doc.count('id="cm-base"') != 1: fail(f"ch{n}: base-map symbol defined {doc.count('id=\"cm-base\"')} times")
    # 2. every SVG is well-formed XML
    for k, s in enumerate(svgs):
        try: minidom.parseString(s if "xmlns:xlink" in s or "xlink:" not in s else s.replace("<svg", '<svg xmlns:xlink="http://www.w3.org/1999/xlink"', 1))
        except Exception as e: fail(f"ch{n}: svg #{k} not XML: {str(e)[:80]}")
    # independence: cards never touch map defs, maps never touch card ids
    for s in cards:
        if "cm-" in s: fail(f"ch{n}: a memory card references the map defs")
    for s in maps:
        if re.search(r'id="mc|url\(#mc', s): fail(f"ch{n}: a route map references memory-card ids")
    # 3. rendered STORY / LINK / LOCI / prompt text == content/
    frames = re.findall(r'<section class="frame.*?</section>', doc, re.S)
    if len(frames) != 10: fail(f"ch{n}: {len(frames)} frame sections")
    for i, sec in enumerate(frames):
        f = CH[n]["frames"][i]
        got = {k: html.unescape(re.search(r'<div class="row %s"><div class="lab">[A-Z]+</div><p>(.*?)</p>' % c, sec, re.S).group(1)) for k, c in (("story", "s"), ("link", "l"), ("loci", "c"))}
        got["prompt"] = html.unescape(re.search(r'<div class="prompt">.*?<p>(.*?)\.</p>', sec, re.S).group(1))
        got["hook"] = html.unescape(re.search(r'Sound-hook: (.*?)</span>', sec, re.S).group(1))
        for k, v in got.items():
            if v != f[k]: fail(f"ch{n} frame {i}: rendered {k} differs from content/")
    # 4-5. route maps: pin, leg, station strip
    nxt = n + 1 if n < 100 else 1
    for i, s in enumerate(maps):
        if attr(s[:300], "data-frame") != str(i) or attr(s[:300], "data-ch") != str(n): fail(f"ch{n}: map {i} has wrong data-ch/frame")
        crop = tuple(float(v) for v in attr(s[:400], "data-crop").split(","))
        pin = re.search(r'<circle class="rm-here rm-pin"[^>]*>', s).group(0)
        at = tuple(int(v) for v in attr(pin, "data-at").split(","))
        if at != PTS[n]: fail(f"ch{n}.{i}: pin data-at {at} != map_points[{n}] {PTS[n]}")
        px, py = routemap.project(PTS[n], crop)
        if abs(float(attr(pin, "cx")) - px) > 0.2 or abs(float(attr(pin, "cy")) - py) > 0.2: fail(f"ch{n}.{i}: pin not drawn at map_points[{n}]")
        leg = re.search(r'<path class="rm-next rm-leg"[^>]*>', s).group(0)
        to = tuple(int(v) for v in attr(leg, "data-to").split(","))
        if to != PTS[nxt]: fail(f"ch{n}.{i}: leg ends at {to}, want map_points[{nxt}] {PTS[nxt]}")
        dot = re.search(r'<circle class="rm-next rm-next-dot"[^>]*>', s).group(0)
        nx_, ny_ = routemap.project(PTS[nxt], crop)
        if abs(float(attr(dot, "cx")) - nx_) > 0.2 or abs(float(attr(dot, "cy")) - ny_) > 0.2: fail(f"ch{n}.{i}: next stop not drawn at map_points[{nxt}]")
        if not (0 <= px <= 300 and 0 <= py <= 240 and 0 <= nx_ <= 300 and 0 <= ny_ <= 240): fail(f"ch{n}.{i}: pin or next stop outside the map window")
        if 'dasharray="10 8"' not in leg: fail(f"ch{n}.{i}: leg is not dashed 10 8")
        op = float(attr(leg, "opacity"))
        if (i == 9 and op != 1) or (i < 9 and op != 0.5): fail(f"ch{n}.{i}: leg opacity {op}")
        here = re.findall(r'class="rm-here rm-strip-here" data-k="(\d+)"', s)
        if here != [str(i)]: fail(f"ch{n}.{i}: strip highlights {here}, want [{i}]")
        if "<title>" not in s or "<desc>" not in s: fail(f"ch{n}.{i}: map missing title/desc")
    # 6. memory cards: station badge + title
    words = [w["word"] for w in D[n - 1]["words"]] + [D[nxt - 1]["words"][0]["word"]]
    for i, s in enumerate(cards):
        badge = re.search(r'<g class="mc-badge" data-station="([A-Z]+)"', s)
        if not badge or badge.group(1) != STATIONS[i]: fail(f"ch{n}.{i}: card badge {badge and badge.group(1)} != {STATIONS[i]}")
        t = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
        if t != f"Memory card · {words[i]} → {words[i+1]}": fail(f"ch{n}.{i}: card title {t!r}")
        vis = html.unescape(re.sub(r"<[^>]+>", " ", re.search(r'<text[^>]*class="mc-title".*?</text>', s, re.S).group(0)))
        if " ".join(vis.split()) != f"{words[i].upper()} → {words[i+1].upper()}": fail(f"ch{n}.{i}: visible card title {vis!r}")
        if attr(s[:400], "data-card") != "1": notes.append(f"ch{n}.{i}: generic fallback card")

print(f"[pages] 100 pages, {n_svgs} top-level SVGs (30 frame images + 1 base-map symbol each), all parsed as XML")
print(f"[size] max {max(sizes.values())/1024:.0f} KB (ch{max(sizes, key=sizes.get)}), median {sorted(sizes.values())[50]/1024:.0f} KB, limit {MAX_BYTES/1024:.0f} KB")

# ------------------------------------------------------------------ 9. contrast
print("[contrast] (>= 4.5:1 required for pin and labels; 'info' rows are not required)")
for name, r in routemap.contrast_report():
    need = not name.startswith("info")
    ok = r >= 4.5 or not need
    if not ok: fail(f"contrast {name}: {r:.2f}")
    print(f"   {r:5.2f}:1  {'PASS' if ok and need else '    '}  {name}")

# ------------------------------------------------------------------ 7. toggles (browser) + screenshots
if "--browser" in sys.argv:
    import asyncio, pathlib, tempfile
    from playwright.async_api import async_playwright
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import shot

    async def toggles():
        src = os.path.join(ROOT, "chapters", "chapter_007.html")
        txt = re.sub(r"@import url\([^)]*\);", "", open(src, encoding="utf-8").read())
        tmp = os.path.join(tempfile.gettempdir(), "_check_toggles.html"); open(tmp, "w", encoding="utf-8").write(txt)
        async with async_playwright() as p:
            b = await shot.launch(p); pg = await b.new_page(viewport={"width": 1280, "height": 900})
            await pg.goto(pathlib.Path(tmp).as_uri())
            vis = lambda: pg.evaluate("""() => Object.fromEntries(['story','card','map'].map(k => [k,
                [...document.querySelectorAll('.img-' + k)].filter(e => getComputedStyle(e).display !== 'none').length]))""")
            start = await vis()
            if start != {"story": 10, "card": 10, "map": 10}: fail(f"toggles: initial visible {start}")
            for k in ("story", "card", "map"):
                await pg.click(f'[data-toggle="{k}"]')
                v = await vis()
                want = {x: (0 if x == k else 10) for x in ("story", "card", "map")}
                if v != want: fail(f"toggles: hiding {k} gave {v}, want {want}")
                pressed = await pg.get_attribute(f'[data-toggle="{k}"]', "aria-pressed")
                if pressed != "false": fail(f"toggles: {k} aria-pressed={pressed}")
                await pg.click(f'[data-toggle="{k}"]')
                if await vis() != start: fail(f"toggles: showing {k} again failed")
            await pg.click('[data-toggle="card"]'); await pg.reload()
            v = await vis()
            if v != {"story": 10, "card": 0, "map": 10}: fail(f"toggles: choice not remembered after reload: {v}")
            await pg.click('[data-toggle="card"]')
            await b.close()
        print("[toggles] Story / Card / Map hide and show independently; choice survives reload (localStorage)")

    asyncio.run(toggles())
    os.makedirs(os.path.join(ROOT, "docs", "screens"), exist_ok=True)
    for n in (1, 25, 50, 75, 100):
        out = os.path.join(ROOT, "docs", "screens", f"chapter_{n:03d}.png")
        asyncio.run(shot.main(os.path.join(ROOT, "chapters", f"chapter_{n:03d}.html"), out, 1360, 900))
    asyncio.run(shot.main(os.path.join(ROOT, "chapters", "chapter_050.html"), os.path.join(ROOT, "docs", "screens", "chapter_050_mobile.png"), 390, 800))
    print("[screens] docs/screens/chapter_001/025/050/075/100.png + chapter_050_mobile.png")

fallbacks = [x for x in notes if "fallback" in x]
if fallbacks: print(f"[cards] {len(fallbacks)} frames use the generic fallback card")
else: print("[cards] every frame has a card spec (no generic fallback cards)")
for x in notes:
    if "fallback" not in x: print("   note:", x)
print("\nRESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
for f_ in fails[:40]: print("  -", f_)
sys.exit(1 if fails else 0)
