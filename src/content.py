import json, re, glob
import os
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "saga.json"), encoding="utf-8"))
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
def _noun(spec):
    """'gnome(lying, green-moon hat)' -> ('gnome', ['lying', 'green-moon hat'])"""
    m = re.match(r"^\s*([^()]+?)\s*(?:\((.*)\))?\s*$", spec)
    if not m: raise ValueError(f"bad object spec: {spec!r}")
    return m.group(1).strip(), [x.strip() for x in (m.group(2) or "").split(",") if x.strip()]

def parse_cards(files):
    """Memory-Card specs (content/cards/cards_*.txt) -> {chapter: {frame_no 1..10: card}}.
    Line:  k | A: noun(mods) | B: noun(mods) | ACT: slug | SCALE: A=giant,B=tiny | OAES: O,A,S
    '#' starts a comment. Missing chapters/frames are simply absent (memcard falls back)."""
    cards, cur = {}, None
    for f in sorted(files):
        for raw in open(f, encoding="utf-8"):
            line = raw.split("#", 1)[0].strip() if not raw.lstrip().startswith("##") else raw.strip()
            if not line: continue
            if line.startswith("## "):
                cur = int(line[3:].strip()); cards.setdefault(cur, {}); continue
            parts = [p.strip() for p in line.split("|")]
            k = int(parts[0])
            kv = dict((p.split(":", 1)[0].strip().upper(), p.split(":", 1)[1].strip()) for p in parts[1:])
            scale = {}
            for s in kv.get("SCALE", "-").split(","):
                if "=" in s: a, b = s.split("="); scale[a.strip().upper()] = b.strip().lower()
            oaes = [x.strip().upper() for x in kv.get("OAES", "-").split(",") if x.strip() and x.strip() != "-"]
            if cur is None or not 1 <= k <= 10: raise ValueError(f"{f}: bad card line {line[:60]}")
            cards[cur][k] = {"a": _noun(kv["A"]), "b": _noun(kv["B"]), "act": kv.get("ACT", "-").strip("- ") and kv.get("ACT"),
                             "scale": scale, "oaes": oaes}
    return cards

if __name__ == "__main__":
    import sys
    chs = parse(glob.glob("content/b*.txt"))
    e = validate(chs, D)
    print(sorted(chs), "\n".join(e) or "OK")
