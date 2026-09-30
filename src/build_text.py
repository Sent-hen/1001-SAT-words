"""Build text-only chapter pages (image prompts instead of drawings) + combined script."""
import json, glob, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = content.D
CH = content.parse(glob.glob(os.path.join(ROOT, "content", "b*.txt")))
assert not content.validate(CH, D)
STATIONS = ["ARCH", "STEP", "LAMP", "RUG", "HEART", "PILLAR", "WINDOW", "STAIR", "BALCONY", "TOP"]
STYLE = ("Vibrant modern comic-book panel, Arabian Nights fantasy, mythic medieval Baghdad, bold clean ink outlines, "
         "cel shading, warm jewel-tone palette (saffron, teal, indigo, gold), cinematic angle, expressive faces, aimed at teenagers, no text")
CAST = ("Character key: Zayn = 15-year-old boy, wild black curls, orange headband with trailing tails, saffron sleeveless tunic, teal trousers, courier satchel. "
        "Layla = 15-year-old girl scholar, loose indigo headscarf, reed pen behind ear, long black braid, turquoise ink-spotted robe, brass spectacles, glowing leather book on a strap. "
        "Qalam = small djinn of flowing black calligraphy ink with big golden eyes and a gold pen-nib crest. "
        "Tariq = 10-year-old boy, curls, missing front tooth, oversized lime-green cap. "
        "Sinbad = 70-year-old sailor, huge white beard braided into anchors, red-and-white striped turban, patched blue coat, whale-bone cane. "
        "Pebble = baby roc, fluffy sunset-red and gold, eggshell on head (grows to house-size). "
        "Marjana = 16-year-old girl, crimson bandana, bandolier of throwing knives, gold coin belt. "
        "Yasmin = 16-year-old girl, white heron-feather hooded cloak, silver winged eyeliner, one grey streak in black hair, crescent pendant. "
        "Zulmat = very tall vizier, violet-black robes fading to smoke, silver mask with no mouth, staff topped with black glowing meteorite. "
        "Hushlings = mouthless dripping ink-shadow creatures with pale hollow eyes.")
DISTRICTS = [c["district"] for c in D[::10]]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@500;700;800&display=swap');
:root{--ink:#1b1b2f;--paper:#fbf1dc;--gold:#ffd23f;--story:#2f6db5;--link:#c0262d;--loci:#157a4f;--bg:#2a1f3d;--prompt:#241b35}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);font-family:Nunito,Arial,sans-serif;color:var(--ink)}
.page{max-width:1320px;margin:24px auto;background:var(--paper);border:5px solid var(--ink);border-radius:10px;padding:18px 18px 24px;box-shadow:0 10px 40px #0008}
nav{display:flex;justify-content:space-between;gap:8px;margin-bottom:10px;font-weight:800;flex-wrap:wrap}
nav a{color:#6b2fa0;text-decoration:none;border:2px solid #6b2fa0;border-radius:20px;padding:3px 12px;font-size:14px}
nav a:hover{background:#6b2fa0;color:#fff}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:4px solid var(--ink);padding-bottom:10px;margin-bottom:14px;flex-wrap:wrap}
.saga{font-family:Bangers,Impact,sans-serif;letter-spacing:2px;font-size:18px;color:#6b2fa0}
h1{font-family:Bangers,Impact,sans-serif;font-size:42px;letter-spacing:2px;margin:0;line-height:1.05}
h1 .num{background:var(--ink);color:var(--gold);padding:2px 12px;border-radius:8px;margin-right:10px;display:inline-block}
.meta{font-weight:800;font-size:15px;text-align:right}
.meta .loc{color:var(--loci)}
details.style{margin:0 0 14px;background:#fff;border:2px dashed #b9a57a;border-radius:8px;padding:8px 12px;font-size:13px}
details.style summary{cursor:pointer;font-weight:800;color:#6b2fa0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.frame{background:#fff;border:3px solid var(--ink);border-radius:8px;overflow:hidden;display:flex;flex-direction:column}
.frame.wide{grid-column:1/-1}
.fno{font-family:Bangers,Impact,sans-serif;font-size:15px;letter-spacing:1px;background:var(--ink);color:#fff;padding:3px 10px;display:flex;justify-content:space-between;gap:6px}
.art svg{display:block;width:100%;height:auto;aspect-ratio:4/3}
.frame.wide .art svg{aspect-ratio:4/1}
.prompt{background:var(--prompt);color:#efe6ff;padding:12px 14px;min-height:0;display:flex;flex-direction:column;gap:6px;position:relative}
.frame.wide .prompt{min-height:0}
.prompt .lab{font-family:Bangers,Impact,sans-serif;letter-spacing:1.5px;color:var(--gold);font-size:15px;display:flex;justify-content:space-between;align-items:center}
.prompt p{margin:0;font-size:13.5px;line-height:1.45;font-style:italic}
.prompt button{font:700 11px Nunito,sans-serif;background:var(--gold);border:0;border-radius:12px;padding:3px 10px;cursor:pointer;color:var(--ink)}
.word{padding:8px 10px 6px;border-bottom:2px dashed #d6c9a8;background:#fff8e6}
.word b{font-family:Bangers,Impact,sans-serif;font-size:26px;letter-spacing:1.5px;color:var(--link)}
.word .pos{font-style:italic;font-weight:700;margin:0 6px;color:#555}
.word .mean{font-weight:800}
.word .hook{display:block;font-size:13px;color:#6b2fa0;font-weight:700;margin-top:2px}
.row{display:grid;grid-template-columns:62px 1fr;border-top:1px solid #eadfc4;font-size:13.5px;line-height:1.4}
.row .lab{font-family:Bangers,Impact,sans-serif;letter-spacing:1px;color:#fff;display:flex;align-items:flex-start;justify-content:center;padding-top:7px;font-size:15px}
.row p{margin:0;padding:6px 9px}
.row.s .lab{background:var(--story)} .row.l .lab{background:var(--link)} .row.c .lab{background:var(--loci)}
.frame.wide .rows{display:grid;grid-template-columns:repeat(3,1fr)}
.frame.wide .row{border-left:1px solid #eadfc4}
footer{margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.box{border:3px solid var(--ink);border-radius:8px;padding:10px 12px;background:#fff}
.box h3{font-family:Bangers,Impact,sans-serif;letter-spacing:1.5px;margin:0 0 6px;font-size:20px}
.chain{font-weight:800;line-height:1.9}
.chain span{background:var(--gold);border:2px solid var(--ink);border-radius:12px;padding:1px 8px;white-space:nowrap}
.stations{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;font-size:12.5px;font-weight:700}
.stations div{border:2px solid var(--loci);border-radius:6px;padding:4px 6px;background:#effaf2}
.stations i{display:block;font-style:normal;color:var(--loci);font-family:Bangers,Impact,sans-serif;letter-spacing:1px;font-size:14px}
.chant{margin-top:8px;font-family:Bangers,Impact,sans-serif;letter-spacing:1px;color:var(--loci);font-size:16px;text-align:center}
.oaes{font-size:12px;margin-top:8px;color:#555}
@media (max-width:900px){.grid{grid-template-columns:1fr}.frame.wide .rows{grid-template-columns:1fr}footer{grid-template-columns:1fr}.stations{grid-template-columns:repeat(2,1fr)}h1{font-size:30px}.page{margin:0;border-radius:0;padding:12px}}
@media print{body{background:#fff}.page{box-shadow:none;margin:0}nav,.prompt button{display:none}}
"""
# --- three images per frame (Story Panel · Memory Card · Route Map); chapter pages only
IMG_CSS = """
:root{--here:#ff2d95;--next:#00e5ff;--traveled:#9cff57;--future:#8a94a6}
.toolbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;background:var(--ink);color:#fff;padding:7px 12px;border-bottom:3px solid var(--gold);font-weight:800;font-size:13px}
.toolbar span{font-family:Bangers,Impact,sans-serif;letter-spacing:1.5px;font-size:15px;color:var(--gold);margin-right:4px}
.toolbar button{font:800 13px Nunito,Arial,sans-serif;border:2px solid #fff;border-radius:16px;padding:3px 12px;cursor:pointer;background:transparent;color:#fff}
.toolbar button[aria-pressed=true]{color:#fff;border-color:transparent}
.toolbar button[data-toggle=story][aria-pressed=true]{background:var(--story)}
.toolbar button[data-toggle=card][aria-pressed=true]{background:var(--link)}
.toolbar button[data-toggle=map][aria-pressed=true]{background:var(--loci)}
.toolbar button[aria-pressed=false]{text-decoration:line-through;opacity:.75}
.toolbar button:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
figure.img{margin:0;display:flex;flex-direction:column;min-width:0}
figure.img .tab{font-family:Bangers,Impact,sans-serif;letter-spacing:1.2px;font-size:12.5px;color:#fff;padding:2px 9px;line-height:1.35}
.img-story .tab{background:var(--story)} .img-card .tab{background:var(--link)} .img-map .tab{background:var(--loci)}
.duo{display:grid;grid-template-columns:1fr 1fr;border-top:3px solid var(--ink);background:var(--ink);gap:3px}
.duo svg{display:block;width:100%;height:auto;aspect-ratio:1/1}
.frame.wide .duo{grid-template-columns:repeat(2,300px);justify-content:center;gap:14px;padding:10px 0;background:#2a1f3d}
.hide-story .img-story,.hide-card .img-card,.hide-map .img-map{display:none}
.hide-card.hide-map .duo{display:none}
.hide-story .duo{border-top:0}
.hide-card .duo,.hide-map .duo{grid-template-columns:minmax(0,300px);justify-content:center;background:#2a1f3d}
.routemap .rm-pulse{transform-box:fill-box;transform-origin:center;animation:rm-pulse 1.8s ease-out infinite}
@keyframes rm-pulse{0%{transform:scale(.7);opacity:.95}100%{transform:scale(2.1);opacity:0}}
@media (prefers-reduced-motion:reduce){.routemap .rm-pulse{animation:none;opacity:.6}}
.routemap .rm-here{fill:var(--here)} .routemap .rm-pulse{stroke:var(--here)}
.routemap polyline.rm-traveled,.routemap line.rm-traveled{stroke:var(--traveled)} .routemap circle.rm-traveled{fill:var(--traveled)}
.routemap path.rm-next,.routemap line.rm-next,.routemap circle.rm-next{stroke:var(--next)} .routemap polygon.rm-next{fill:var(--next)}
.routemap .rm-future{stroke:var(--future)}
@media (max-width:600px){.duo,.frame.wide .duo{grid-template-columns:1fr}.frame.wide .duo{padding:0;gap:3px}}
@media print{.toolbar{display:none}.routemap .rm-pulse{animation:none}}
"""
TOGGLE_JS = """<script>
(function(){var K='taow-images',s={story:true,card:true,map:true};
try{var v=JSON.parse(localStorage.getItem(K)||'null');if(v)for(var k in s)if(typeof v[k]==='boolean')s[k]=v[k]}catch(e){}
function apply(){for(var k in s){document.body.classList.toggle('hide-'+k,!s[k]);var b=document.querySelector('[data-toggle="'+k+'"]');if(b)b.setAttribute('aria-pressed',String(s[k]))}}
document.querySelectorAll('[data-toggle]').forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-toggle');s[k]=!s[k];apply();
try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}})});apply()})();
</script>"""

JS = """<script>
function cp(b){const t=document.getElementById('style').innerText+'. '+b.closest('.prompt').querySelector('p').innerText;
try{navigator.clipboard.writeText(t);b.textContent='Copied!';setTimeout(()=>b.textContent='Copy full prompt',1200)}catch(e){}}
</script>"""

e = lambda s: html.escape(s, quote=False)

def art_panels(n):
    import scenes, autoart
    if n == 1:
        import importlib.util
        here = os.path.dirname(os.path.abspath(__file__))
        spec = importlib.util.spec_from_file_location("ch001", os.path.join(here, "ch001.py")); m = importlib.util.module_from_spec(spec)
        cwd = os.getcwd(); os.chdir(here); spec.loader.exec_module(m); os.chdir(cwd)
        return [scenes.panel(p["art"], 1200 if p.get("wide") else 400, 300) for p in m.PANELS]
    scenes.VOCAB.clear()
    nt = D[n]["title"] if n < 100 else None
    return [autoart.compose(n, i, CH[n]["frames"][i], D[n - 1]["words"][i]["word"], nt) for i in range(10)]

def memory_cards(n):
    try:
        import memcard
    except ImportError:
        return None
    return [memcard.memory_card(n, i) for i in range(10)]

def page(n):
    import routemap
    ch, c = D[n - 1], CH[n]
    arts = art_panels(n)
    cards = memory_cards(n)
    maps = [routemap.route_map(n, i, c["stations"]) for i in range(10)]
    words = ch["words"]
    nxt = D[n]["words"][0] if n < 100 else D[0]["words"][0]
    cells = []
    for i, f in enumerate(c["frames"]):
        w = words[i]
        wide = i == 9
        cells.append(f"""<section class="frame{' wide' if wide else ''}">
 <div class="fno"><span>FRAME {i+1 if i < 9 else 0} · WORD #{w['n']}</span><span>📍 STATION {i+1} · {STATIONS[i]}</span></div>
 <figure class="img img-story"><figcaption class="tab">📖 STORY</figcaption><div class="art">{arts[i]}</div></figure>
 <div class="duo">{f'<figure class="img img-card"><figcaption class="tab">🔗 MEMORY CARD</figcaption>{cards[i]}</figure>' if cards else ''}<figure class="img img-map"><figcaption class="tab">🗺️ ROUTE</figcaption>{maps[i]}</figure></div>
 <div class="prompt"><div class="lab"><span>🎨 IMAGE PROMPT{' · WIDE 4:1' if wide else ' · 4:3'}</span><button onclick="cp(this)">Copy full prompt</button></div><p>{e(f['prompt'])}.</p></div>
 <div class="word"><b>{w['word'].upper()}</b><span class="pos">{w['pos']}</span><span class="mean">{e(w['meaning'])}</span><span class="hook">🔊 Sound-hook: {e(f['hook'])}</span></div>
 <div class="rows">
  <div class="row s"><div class="lab">STORY</div><p>{e(f['story'])}</p></div>
  <div class="row l"><div class="lab">LINK</div><p>{e(f['link'])}</p></div>
  <div class="row c"><div class="lab">LOCI</div><p>{e(f['loci'])}</p></div>
 </div>
</section>""")
    chain = " → ".join(f"<span>{w['word']}</span>" for w in words) + f" → <span style='background:#fff'>{nxt['word']} (Ch.{n+1 if n < 100 else 1})</span>"
    stations = "".join(f"<div><i>{k+1} · {STATIONS[k]}</i>{e(c['stations'][k])} → <b>{words[k]['word']}</b></div>" for k in range(10))
    loc = ch["locus"]
    walk = loc.upper() if loc.startswith("The ") else "THE " + loc.upper()
    prev_l = f'<a href="chapter_{n-1:03d}.html">◀ Chapter {n-1}</a>' if n > 1 else "<span></span>"
    next_l = f'<a href="chapter_{n+1:03d}.html">Chapter {n+1} ▶</a>' if n < 100 else "<span></span>"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter {n} · {e(ch['title'])} | The Thousand and One Words</title><style>{CSS}{IMG_CSS}</style></head><body>
{routemap.base_defs()}
<div class="toolbar" role="group" aria-label="Show or hide each image type"><span>SHOW:</span><button type="button" data-toggle="story" aria-pressed="true">📖 Story</button><button type="button" data-toggle="card" aria-pressed="true">🔗 Card</button><button type="button" data-toggle="map" aria-pressed="true">🗺️ Map</button></div>
<div class="page">
<nav>{prev_l}<a href="index.html">All 100 chapters</a>{next_l}</nav>
<header>
 <div><div class="saga">THE THOUSAND AND ONE WORDS · The Saga of the Shattered Lexicon</div>
 <h1><span class="num">CHAPTER {n}</span>{e(ch['title'].upper())}</h1></div>
 <div class="meta"><div class="loc">📍 {e(loc)}</div><div>District {(n-1)//10+1}: {e(ch['district'])}</div><div>Words {words[0]['n']}–{words[-1]['n']}</div></div>
</header>
<details class="style"><summary>🎨 Image style prefix &amp; character key (added automatically by “Copy full prompt”)</summary>
<p id="style">{e(STYLE)}. {e(CAST)}</p></details>
<div class="grid">{''.join(cells)}</div>
<footer>
 <div class="box"><h3 style="color:var(--link)">🔗 THE LINK CHAIN (recite it!)</h3><div class="chain">{chain}</div>
 <div class="oaes"><b>OAES</b> = <b>O</b>ut of proportion · <b>A</b>ction · <b>E</b>xaggeration · <b>S</b>ubstitution (a sound-alike picture for the word)</div></div>
 <div class="box"><h3 style="color:var(--loci)">🏛️ WALK {e(walk)}</h3><div class="stations">{stations}</div>
 <div class="chant">ARCH · STEP · LAMP · RUG · HEART! — PILLAR · WINDOW · STAIR · BALCONY · TOP!</div></div>
</footer>
</div>{JS}{TOGGLE_JS}</body></html>"""

def prompts_md(n):
    ch, c = D[n - 1], CH[n]
    out = [f"# Chapter {n} · {ch['title']} — Image prompts", f"📍 {ch['locus']} · Words {ch['words'][0]['n']}–{ch['words'][-1]['n']}\n",
           f"**Style prefix (put before every prompt):** {STYLE}.\n", f"**{CAST}**\n"]
    for i, f in enumerate(c["frames"]):
        w = ch["words"][i]
        out.append(f"### Frame {i+1 if i < 9 else 0} · #{w['n']} {w['word'].upper()} ({'wide 4:1' if i == 9 else '4:3'})\n{f['prompt']}.\n")
    return "\n".join(out)

def index():
    rows = []
    for d in range(10):
        items = "".join(f'<li><a href="chapter_{c["chapter"]:03d}.html"><b>{c["chapter"]}.</b> {e(c["title"])}</a><small>📍 {e(c["locus"])} · {c["words"][0]["n"]}–{c["words"][-1]["n"]}</small></li>' for c in D[d*10:d*10+10])
        rows.append(f"<section><h2>Arc {d+1} · {e(DISTRICTS[d])}</h2><ol>{items}</ol></section>")
    css = CSS + """ .idx{display:grid;grid-template-columns:repeat(2,1fr);gap:14px} .idx section{background:#fff;border:3px solid var(--ink);border-radius:8px;padding:10px 14px}
 .idx h2{font-family:Bangers,Impact,sans-serif;letter-spacing:1.5px;margin:0 0 6px;color:#6b2fa0;font-size:22px} .idx ol{list-style:none;margin:0;padding:0}
 .idx li{padding:4px 0;border-bottom:1px dashed #e0d3b0} .idx li a{color:var(--ink);text-decoration:none;font-weight:700} .idx li a:hover{color:var(--link)}
 .idx small{display:block;color:#6b6b6b;font-size:12px} @media (max-width:900px){.idx{grid-template-columns:1fr}}"""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Thousand and One Words · All Chapters</title><style>{css}</style></head><body><div class="page">
<header><div><div class="saga">THE SAGA OF THE SHATTERED LEXICON</div><h1>THE THOUSAND AND ONE WORDS</h1></div>
<div class="meta">100 chapters · 1000 SAT words<br>Story · Link · Loci</div></header>
<div class="idx">{''.join(rows)}</div></div></body></html>"""

def all_md():
    out = ["# 06 · All 100 Chapters — Full Comic Script with Image Prompts",
           "Each chapter is one page: a 3×3 grid (Frames 1–9 = words 1–9) plus a wide Frame 0 (word 10). Every frame has an IMAGE PROMPT, the word, a sound-hook, and STORY / LINK / LOCI rows.\n",
           f"**Image style prefix (put before every prompt):** {STYLE}.\n", f"**{CAST}**\n"]
    for d in range(10):
        out.append(f"\n---\n\n# Arc {d+1} · {DISTRICTS[d]}\n")
        for ch in D[d*10:d*10+10]:
            n = ch["chapter"]; c = CH[n]
            out.append(f"\n## Chapter {n} — {ch['title']}\n📍 **{ch['locus']}** · Words {ch['words'][0]['n']}–{ch['words'][-1]['n']}\n")
            out.append("**Loci stations:** " + " · ".join(f"{k+1} {STATIONS[k]}: {c['stations'][k]}" for k in range(10)) + "\n")
            for i, f in enumerate(c["frames"]):
                w = ch["words"][i]
                out.append(f"### Frame {i+1 if i < 9 else 0} · #{w['n']} {w['word'].upper()} ({w['pos']}) — {w['meaning']}\n"
                           f"- 🎨 **Image prompt{' (wide 4:1)' if i == 9 else ''}:** {f['prompt']}.\n- 🔊 **Sound-hook:** {f['hook']}\n"
                           f"- **STORY:** {f['story']}\n- **LINK:** {f['link']}\n- **LOCI:** {f['loci']}\n")
    return "\n".join(out)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "chapters"), exist_ok=True)
    for n in range(1, 101):
        open(os.path.join(ROOT, "chapters", f"chapter_{n:03d}.html"), "w", encoding="utf-8", newline="\n").write(page(n))
        open(os.path.join(ROOT, "chapters", f"chapter_{n:03d}_prompts.md"), "w", encoding="utf-8", newline="\n").write(prompts_md(n))
    open(os.path.join(ROOT, "chapters", "index.html"), "w", encoding="utf-8", newline="\n").write(index())
    open(os.path.join(ROOT, "06_ALL_CHAPTERS.md"), "w", encoding="utf-8", newline="\n").write(all_md())
    print("built 100")
