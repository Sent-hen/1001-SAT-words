"""Fill / verify the OAES field of card lines from each frame's L: text (the tags it already names).
    python tools/fill_oaes.py content/cards/cards_011-020.txt   -> rewrites OAES in place, prints changes"""
import glob, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import content, memcard
CH = content.parse(glob.glob(os.path.join(ROOT, "content", "b*.txt")))
for path in sys.argv[1:]:
    out, cur, changed = [], None, 0
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.startswith("## "): cur = int(line[3:])
        m = re.match(r"^(\d+) \|(.*)\| OAES: *([A-Z,\-?]*)\s*$", line)
        if m and cur:
            k = int(m.group(1)); want = ",".join(memcard.oaes_from_link(CH[cur]["frames"][k - 1]["link"])) or "-"
            if m.group(3) not in (want, "?"): print(f"  {cur}.{k}: {m.group(3)} -> {want}")
            changed += m.group(3) != want
            line = f"{m.group(1)} |{m.group(2)}| OAES: {want}"
        out.append(line)
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"{path}: {changed} OAES fields set from L:")
