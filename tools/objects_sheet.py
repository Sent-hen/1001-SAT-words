"""Contact sheet of every drawing in src/objects.py (QA while growing the library).
    python tools/objects_sheet.py out.html [filter]"""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import objects

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "objects_sheet.html")
flt = sys.argv[2] if len(sys.argv) > 2 else ""
cells = []
for k in sorted(objects.LIB):
    if flt and flt not in k: continue
    svg, _ = objects.draw(k, 50, 88, 1.0)
    cells.append(f'<figure><svg viewBox="0 0 100 100"><rect width="100" height="100" fill="#3a2060"/><line x1="0" y1="88" x2="100" y2="88" stroke="#ff2d95" stroke-width=".5"/>'
                 f'<rect x="10" y="8" width="80" height="80" fill="none" stroke="#fff" stroke-width=".4" stroke-dasharray="2 2"/>{svg}</svg><figcaption>{k}</figcaption></figure>')
cells.append('<figure><svg viewBox="0 0 100 100"><rect width="100" height="100" fill="#3a2060"/>' + objects.draw("whatchamacallit", 50, 88)[0] + '</svg><figcaption>(fallback)</figcaption></figure>')
open(out, "w", encoding="utf-8").write('<!doctype html><meta charset=utf-8><style>body{margin:0;background:#222;display:flex;flex-wrap:wrap;gap:4px;padding:4px;font:10px Arial;color:#fff}'
                                        'figure{margin:0;width:100px}svg{display:block;width:100px;height:100px}figcaption{text-align:center}</style>' + "".join(cells))
print(len(cells), "objects ->", out)
