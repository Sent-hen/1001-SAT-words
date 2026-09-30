"""Draft Memory-Card spec lines from each frame's L: (link) text.

    python tools/draft_cards.py            -> writes content/cards/drafts/cards_NNN-MMM.draft.txt
    python tools/draft_cards.py 11 20      -> only chapters 11..20, printed to stdout (for review)

Drafts are NOT read by the build. After a human review, the corrected lines go into
content/cards/cards_NNN-MMM.txt (the only files content.parse_cards() reads).

Line format (one per frame, k = frame number 1..10):
    k | A: noun(mod, mod) | B: noun(mod) | ACT: slug | SCALE: A=giant | OAES: O,A,S
"""
import glob, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import content, objects

D = content.D
CH = content.parse(glob.glob(os.path.join(ROOT, "content", "b*.txt")))

STOP = set("""a an the that who which whose what so and or but of in on at to into onto from with by for as is are was
were be been being it its his her their he she they them this these those than then there here named called like
who's while when where because if out up down over under off not no just very really all one some every each any
about around through across his itself himself herself themselves s""".split())
BIG = ("giant", "huge", "enormous", "gigantic", "colossal", "massive", "towering", "mountain-sized", "as tall as", "swells", "house-sized", "whale-sized")
SMALL = ("tiny", "little", "small", "mini", "miniature", "teeny", "pocket-sized")
MODS = ("red", "green", "blue", "gold", "golden", "silver", "black", "white", "pink", "purple", "orange", "yellow", "brown", "grey", "gray",
        "glowing", "flaming", "burning", "frozen", "crying", "smiling", "angry", "mean", "sleepy", "fat", "skinny", "fluffy", "spiky",
        "talking", "dancing", "singing", "rusty", "shiny", "wooden", "stone", "iron", "brass", "crystal", "invisible", "ghostly", "rubber")
MANY = ("thousand", "hundreds", "hundred", "dozens", "dozen", "swarm", "flock", "army", "crowd", "herd", "many", "millions")
ACTS = [("bursts-out", ("burst", "explode", "erupt", "pop out", "pops out", "shoots out", "spray", "gush", "spew", "pour out", "pours out", "fly out", "flies out")),
        ("rides", ("ride", "rides", "riding", "surf")),
        ("gulps", ("swallow", "gulp", "eat", "eats", "munch", "chomp", "devour", "bite", "gobble", "slurp", "lick")),
        ("chases", ("chase", "chasing", "hunt", "pursue")),
        ("smashes", ("smash", "stomp", "crush", "kick", "punch", "whack", "squash", "flatten", "slam", "hammer", "knock")),
        ("drops-on", ("drop", "falls", "fall", "rain", "shower", "pour", "land", "plop")),
        ("turns-into", ("turns into", "turn into", "becomes", "transforms", "morph", "melts into", "grows into", "hatches")),
        ("climbs-out", ("climb", "crawl", "emerge", "hatch", "sprout", "rise", "rises")),
        ("hugs", ("hug", "cuddle", "kiss", "embrace")),
        ("catches", ("catch", "caught", "grab", "snatch", "seize", "trap", "net")),
        ("opens", ("open", "unlock", "unlocks", "split")),
        ("throws", ("throw", "hurl", "toss", "fling", "launch", "fire", "shoot")),
        ("carries", ("carry", "carries", "lift", "hoist", "hold")),
        ("pulls", ("pull", "drag", "tow", "tug"))]
OAES = [("O", "out of proportion"), ("A", "action"), ("E", "exaggeration"), ("S", "substitution")]

def singular(w):
    w = w.lower().strip("-")
    for a, b in (("ies", "y"), ("ves", "f"), ("oes", "o"), ("ches", "ch"), ("shes", "sh"), ("sses", "ss"), ("xes", "x")):
        if w.endswith(a) and len(w) > len(a) + 2: return w[: -len(a)] + b
    if w.endswith("s") and not w.endswith(("ss", "us", "is")) and len(w) > 3: return w[:-1]
    return w

def oaes(link):
    low = link.lower()
    return [k for k, name in OAES if re.search(r"\(\s*[^)]*\b" + name, low)]

def words_of(s):
    return re.findall(r"[A-Za-z][A-Za-z'\-]*", s)

def noun_after_quote(rest):
    """rest = text after a closing ” . First non-stopword word, if it looks like a noun."""
    for w in words_of(rest)[:3]:
        if w.lower() in STOP: continue
        if w.isupper() and len(w) > 2: return None
        return w
    return None

def body_after_a(link, word_a):
    """Part of the link after the '(word k)' mention; falls back to the whole text."""
    m = re.search(r"\(" + re.escape(word_a) + r"\)", link, re.I)
    return link[m.end():] if m else link

def _vocabish(tok, words):
    t = re.sub(r"[^a-z]", "", tok.lower())
    return any(t[:5] == re.sub(r"[^a-z]", "", w.lower())[:5] for w in words if len(t) >= 4)

def draft_b(link, word_a, word_b):
    """Object B = the picture for word k+1. Preference: a capitalised/quoted token the object library
    can draw -> the noun right after a quoted sound-alike -> any drawable noun -> first capitalised word."""
    body = body_after_a(link, word_a)
    body = re.sub(r"\((?:[^()]*(?:Out of proportion|Action|Exaggeration|Substitution)[^()]*)\)", " ", body)
    toks = [(m.start(), m.group(0)) for m in re.finditer(r"[A-Za-z][A-Za-z'\-]*", body)]
    noun, where = None, None
    caps = [(p, t) for p, t in toks if t.isupper() and len(t) >= 3 and not _vocabish(t, (word_a, word_b))]
    for p, t in caps:  # a capitalised word the library knows (whole word or a hyphen part)
        cand = [t] + t.split("-")
        hit = next((c for c in cand if objects.resolve(singular(c))), None)
        if hit: noun, where = hit, p; break
    if not noun:
        for q in re.finditer(r"“([^”]+)”", body):
            cand = noun_after_quote(body[q.end():])
            if cand and objects.resolve(singular(cand)):
                noun, where = cand, q.end(); break
    if not noun:
        for p, t in toks[:40]:
            if t.lower() in STOP or t.isupper() or _vocabish(t, (word_a, word_b)): continue
            if objects.resolve(singular(t)): noun, where = t, p; break
    if not noun:
        for q in re.finditer(r"“([^”]+)”", body):
            cand = noun_after_quote(body[q.end():])
            if cand: noun, where = cand, q.end(); break
    if not noun and caps:
        where, noun = caps[0]
    if not noun:
        return None, [], body
    pre = [w.lower() for w in words_of(body[max(0, where - 40):where])][-3:]
    mods = [w for w in pre if w in MODS]
    around = body[max(0, where - 40):where + 40].lower()
    if any(k in around for k in MANY):
        mods.append("many")
    return singular(noun), mods, body

def draft_act(body):
    low = body.lower()
    best = None
    for slug, keys in ACTS:
        for k in keys:
            m = re.search(r"\b" + re.escape(k), low)
            if m and (best is None or m.start() < best[0]): best = (m.start(), slug)
    return best[1] if best else "links-to"

def draft_scale(link, word_a, b_noun):
    low = link.lower()
    head = low[: low.find("(" + word_a.lower() + ")")] if ("(" + word_a.lower() + ")") in low else ""
    out = []
    if any(k in head for k in BIG): out.append("A=giant")
    if b_noun:
        m = low.find(b_noun[:5])
        win = low[max(0, m - 45): m] if m >= 0 else ""
        if any(k in win for k in BIG): out.append("B=giant")
        elif any(k in win for k in SMALL): out.append("B=tiny")
    return ",".join(out) or "-"

def fmt(noun, mods):
    return f"{noun}({', '.join(dict.fromkeys(mods))})" if mods else noun

def draft_chapter(n, prev_b):
    lines = []
    words = [w["word"] for w in D[n - 1]["words"]]
    nextw = D[n]["words"][0]["word"] if n < 100 else D[0]["words"][0]["word"]
    for i, f in enumerate(CH[n]["frames"]):
        wa, wb = words[i], (words[i + 1] if i < 9 else nextw)
        b, bmods, body = draft_b(f["link"], wa, wb)
        b = b or wb
        a = prev_b or (wa, [])
        lines.append(f"{i+1} | A: {fmt(*a)} | B: {fmt(b, bmods)} | ACT: {draft_act(body)} | SCALE: {draft_scale(f['link'], wa, b)} | OAES: {','.join(oaes(f['link'])) or '-'}")
        prev_b = (b, [m for m in bmods if m != "many"] + (["many"] if "many" in bmods else []))
    return lines, prev_b

def draft_all(lo=1, hi=100):
    out, prev = {}, None
    if lo > 1:  # seed the chain with the previous chapter's last B
        for n in range(1, lo):
            _, prev = draft_chapter(n, prev)
    for n in range(lo, hi + 1):
        out[n], prev = draft_chapter(n, prev)
    return out

if __name__ == "__main__":
    if len(sys.argv) == 3:
        lo, hi = int(sys.argv[1]), int(sys.argv[2])
        for n, ls in draft_all(lo, hi).items():
            print(f"## {n}"); print("\n".join(ls))
    else:
        dd = os.path.join(ROOT, "content", "cards", "drafts"); os.makedirs(dd, exist_ok=True)
        allc = draft_all()
        for b in range(10):
            lo, hi = b * 10 + 1, b * 10 + 10
            with open(os.path.join(dd, f"cards_{lo:03d}-{hi:03d}.draft.txt"), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(f"# DRAFT (machine-made by tools/draft_cards.py, NOT reviewed). The build ignores this folder.\n")
                for n in range(lo, hi + 1):
                    fh.write(f"## {n}\n" + "\n".join(allc[n]) + "\n")
        print("drafts written to", dd)
