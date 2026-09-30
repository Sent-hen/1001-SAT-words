import json, importlib, sys, html
sys.path.insert(0, ".")
from scenes import panel

STATIONS = ["ARCH", "STEP", "LAMP", "RUG", "HEART", "PILLAR", "WINDOW", "STAIR", "BALCONY", "TOP"]
DATA = json.load(open("../data/saga.json"))

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@700&family=Nunito:wght@500;700;800&display=swap');
:root{--ink:#1b1b2f;--paper:#fbf1dc;--gold:#ffd23f;--story:#2f6db5;--link:#c0262d;--loci:#157a4f;--bg:#2a1f3d}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);font-family:Nunito,Arial,sans-serif;color:var(--ink)}
.page{max-width:1320px;margin:24px auto;background:var(--paper);border:5px solid var(--ink);border-radius:10px;padding:18px 18px 24px;box-shadow:0 10px 40px #0008}
header{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:4px solid var(--ink);padding-bottom:10px;margin-bottom:14px;flex-wrap:wrap}
.saga{font-family:Bangers,Impact,sans-serif;letter-spacing:2px;font-size:18px;color:#6b2fa0}
h1{font-family:Bangers,Impact,sans-serif;font-size:44px;letter-spacing:2px;margin:0;line-height:1}
h1 .num{background:var(--ink);color:var(--gold);padding:2px 12px;border-radius:8px;margin-right:10px}
.meta{font-weight:800;font-size:15px;text-align:right}
.meta .loc{color:var(--loci)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.frame{background:#fff;border:3px solid var(--ink);border-radius:8px;overflow:hidden;display:flex;flex-direction:column}
.frame.wide{grid-column:1/-1}
.art svg{display:block;width:100%;height:auto;aspect-ratio:4/3}
.frame.wide .art svg{aspect-ratio:4/1}
.fno{font-family:Bangers,Impact,sans-serif;font-size:15px;letter-spacing:1px;background:var(--ink);color:#fff;padding:3px 10px;display:flex;justify-content:space-between}
.word{padding:8px 10px 6px;border-bottom:2px dashed #d6c9a8;background:#fff8e6}
.word b{font-family:Bangers,Impact,sans-serif;font-size:26px;letter-spacing:1.5px;color:var(--link)}
.word .pos{font-style:italic;font-weight:700;margin:0 6px;color:#555}
.word .mean{font-weight:800}
.word .hook{display:block;font-size:13px;color:#6b2fa0;font-weight:700;margin-top:2px}
.row{display:grid;grid-template-columns:62px 1fr;border-top:1px solid #eadfc4;font-size:13.5px;line-height:1.38}
.row .lab{font-family:Bangers,Impact,sans-serif;letter-spacing:1px;color:#fff;display:flex;align-items:flex-start;justify-content:center;padding-top:7px;font-size:15px}
.row p{margin:0;padding:6px 9px}
.row.s .lab{background:var(--story)} .row.l .lab{background:var(--link)} .row.c .lab{background:var(--loci)}
.frame.wide .rows{display:grid;grid-template-columns:repeat(3,1fr)}
.frame.wide .row{border-left:1px solid #eadfc4}
footer{margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.box{border:3px solid var(--ink);border-radius:8px;padding:10px 12px;background:#fff}
.box h3{font-family:Bangers,Impact,sans-serif;letter-spacing:1.5px;margin:0 0 6px;font-size:20px}
.chain{font-weight:800;line-height:1.8}
.chain span{background:var(--gold);border:2px solid var(--ink);border-radius:12px;padding:1px 8px;white-space:nowrap}
.stations{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;font-size:12.5px;font-weight:700}
.stations div{border:2px solid var(--loci);border-radius:6px;padding:4px 6px;background:#effaf2}
.stations i{display:block;font-style:normal;color:var(--loci);font-family:Bangers,Impact,sans-serif;letter-spacing:1px;font-size:14px}
.chant{margin-top:8px;font-family:Bangers,Impact,sans-serif;letter-spacing:1px;color:var(--loci);font-size:16px;text-align:center}
.oaes{font-size:12px;margin-top:8px;color:#555}
@media (max-width:900px){.grid{grid-template-columns:1fr}.frame.wide .rows{grid-template-columns:1fr}footer{grid-template-columns:1fr}.stations{grid-template-columns:repeat(2,1fr)}h1{font-size:32px}.page{margin:0;border-radius:0}}
@media print{body{background:#fff}.page{box-shadow:none;margin:0}}
"""

def esc(s):
    return html.escape(s, quote=False)

def build(num, modname):
    mod = importlib.import_module(modname)
    ch = DATA[num - 1]
    words = ch["words"]
    nxt = DATA[num]["words"][0]["word"] if num < 100 else DATA[0]["words"][0]["word"]
    cells = []
    order = list(range(10))
    for i in order:
        w = words[i]
        f = mod.FRAMES[i]
        p = mod.PANELS[i]
        wide = p.get("wide")
        label = f"FRAME {i+1 if i < 9 else 0}"
        svg = panel(p["art"], 1200 if wide else 400, 300)
        cells.append(f"""
<section class="frame{' wide' if wide else ''}">
 <div class="fno"><span>{label} · WORD #{w['n']}</span><span>📍 STATION {i+1} · {STATIONS[i]}</span></div>
 <div class="art">{svg}</div>
 <div class="word"><b>{w['word'].upper()}</b><span class="pos">{w['pos']}</span><span class="mean">{esc(w['meaning'])}</span><span class="hook">🔊 Sound-hook: {esc(f['hook'])}</span></div>
 <div class="rows">
  <div class="row s"><div class="lab">STORY</div><p>{esc(f['story'])}</p></div>
  <div class="row l"><div class="lab">LINK</div><p>{esc(f['link'])}</p></div>
  <div class="row c"><div class="lab">LOCI</div><p>{esc(f['loci'])}</p></div>
 </div>
</section>""")
    chain = " → ".join(f"<span>{w['word']}</span>" for w in words) + f" → <span style='background:#fff'>{nxt} (Ch.{num+1 if num<100 else 1})</span>"
    stations = "".join(f"<div><i>{k+1} · {STATIONS[k]}</i>{esc(mod.LOCUS_STATIONS[k+1])} → <b>{words[k]['word']}</b></div>" for k in range(10))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter {num} · {esc(ch['title'])} | The Thousand and One Words</title><style>{CSS}</style></head><body>
<div class="page">
<header>
 <div><div class="saga">THE THOUSAND AND ONE WORDS · The Saga of the Shattered Lexicon</div>
 <h1><span class="num">CHAPTER {num}</span>{esc(ch['title'].upper())}</h1></div>
 <div class="meta"><div class="loc">📍 {esc(ch['locus'])}</div><div>District {(num-1)//10+1}: {esc(ch['district'])}</div><div>Words {words[0]['n']}–{words[-1]['n']}</div></div>
</header>
<div class="grid">{''.join(cells)}</div>
<footer>
 <div class="box"><h3 style="color:var(--link)">🔗 THE LINK CHAIN (recite it!)</h3><div class="chain">{chain}</div>
 <div class="oaes"><b>OAES</b> = <b>O</b>ut of proportion · <b>A</b>ction · <b>E</b>xaggeration · <b>S</b>ubstitution (a sound-alike picture for the word)</div></div>
 <div class="box"><h3 style="color:var(--loci)">🏛️ WALK {esc(ch['locus'].upper() if ch['locus'].startswith('The ') else 'THE ' + ch['locus'].upper())}</h3><div class="stations">{stations}</div>
 <div class="chant">ARCH · STEP · LAMP · RUG · HEART! — PILLAR · WINDOW · STAIR · BALCONY · TOP!</div></div>
</footer>
</div></body></html>"""

def prompts_md(num, modname):
    mod = importlib.import_module(modname)
    ch = DATA[num - 1]
    out = [f"# Chapter {num} · {ch['title']} — AI image prompts\n", f"**Style prefix (use for every frame):** {mod.STYLE}\n"]
    for i, f in enumerate(mod.FRAMES):
        w = ch["words"][i]
        out.append(f"### Frame {i+1 if i < 9 else 0} · #{w['n']} {w['word'].upper()}{' (wide 4:1)' if i == 9 else ' (4:3)'}\n{mod.STYLE}. {f['prompt']}.\n")
    return "\n".join(out)

if __name__ == "__main__":
    import os
    num = int(sys.argv[1]); mod = sys.argv[2]
    os.makedirs("../chapters", exist_ok=True)
    open(f"../chapters/chapter_{num:03d}.html", "w").write(build(num, mod))
    open(f"../chapters/chapter_{num:03d}_prompts.md", "w").write(prompts_md(num, mod))
    print("built", num)
