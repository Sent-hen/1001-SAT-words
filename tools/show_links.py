"""Print each frame's L: line (for reviewing card drafts).  python tools/show_links.py LO HI"""
import glob, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import content
CH = content.parse(glob.glob(os.path.join(ROOT, "content", "b*.txt")))
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for n in range(lo, hi + 1):
    print(f"## {n}")
    for k, f in enumerate(CH[n]["frames"]):
        print(f"{k+1}. {f['link'].split(' · ', 1)[-1]}")
