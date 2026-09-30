import json, re, glob
import os
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "saga.json")))
def parse(files):
    chs = {}; cur = None; fr = None
    for f in sorted(files):
        for raw in open(f, encoding="utf-8"):
            line = raw.rstrip("\n")
            if not line.strip(): continue
            if line.startswith("## "):
                cur = int(line[3:].strip()); chs[cur] = {"stations": None, "frames": []}; continue
            if line.startswith("ST:"):
                chs[cur]["stations"] = [s.strip() for s in line[3:].split("|")]; continue
            if line.startswith("== "):
                fr = {"word": line[3:].strip()}; chs[cur]["frames"].append(fr); continue
            m = re.match(r"^([THLCP]): (.*)$", line)
            if m:
                fr[{"T": "story", "H": "hook", "L": "link", "C": "loci", "P": "prompt"}[m.group(1)]] = m.group(2).strip(); continue
            raise ValueError(f"{f}: bad line: {line[:80]}")
    return chs
def validate(chs, D):
    errs = []
    for n, c in chs.items():
        exp = [w["word"] for w in D[n-1]["words"]]
        got = [f["word"] for f in c["frames"]]
        if got != exp: errs.append(f"ch{n} words {got} != {exp}")
        if not c["stations"] or len(c["stations"]) != 10: errs.append(f"ch{n} stations {len(c['stations'] or [])}")
        for f in c["frames"]:
            for k in ("story", "hook", "link", "loci", "prompt"):
                if k not in f: errs.append(f"ch{n} {f['word']} missing {k}")
        # link numbering check
        for i, f in enumerate(c["frames"]):
            a = D[n-1]["words"][i]["n"]; b = a + 1 if a < 1000 else 1
            if "link" in f and not f["link"].startswith(f"{a}→{b}"): errs.append(f"ch{n} {f['word']} link prefix {f['link'][:12]} expected {a}→{b}")
            st = f"Station {i+1} ·"
            if "loci" in f and not f["loci"].startswith(st): errs.append(f"ch{n} {f['word']} loci prefix")
    return errs
if __name__ == "__main__":
    import sys
    chs = parse(glob.glob("content/b*.txt"))
    e = validate(chs, D)
    print(sorted(chs), "\n".join(e) or "OK")
