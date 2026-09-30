"""Memory-card coverage report.
    python tools/card_coverage.py [lo hi]
Lists chapters without reviewed cards and every noun that still uses the thought-bubble fallback."""
import collections, glob, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import content, objects

lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (1, 100)
cards = content.parse_cards(glob.glob(os.path.join(ROOT, "content", "cards", "cards_*.txt")))
missing_ch = [n for n in range(lo, hi + 1) if n not in cards]
missing_fr = [(n, k) for n in range(lo, hi + 1) if n in cards for k in range(1, 11) if k not in cards[n]]
fall = collections.defaultdict(list)
total = drawn = 0
for n in range(lo, hi + 1):
    for k, c in sorted((cards.get(n) or {}).items()):
        for who in ("a", "b"):
            total += 1
            noun = c[who][0]
            if objects.resolve(noun): drawn += 1
            else: fall[noun].append(f"{n}.{k}{who.upper()}")
frames = sum(len(cards.get(n) or {}) for n in range(lo, hi + 1))
print(f"chapters {lo}-{hi}: {frames}/{(hi-lo+1)*10} frames have cards; {drawn}/{total} objects drawn from the library "
      f"({100*drawn/max(total,1):.1f}%), {total-drawn} use the thought-bubble fallback ({len(fall)} distinct nouns)")
if missing_ch: print("chapters with no cards (generic fallback card):", ", ".join(map(str, missing_ch)))
if missing_fr: print("frames with no card line:", ", ".join(f"{n}.{k}" for n, k in missing_fr))
for noun, where in sorted(fall.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    print(f"  {noun:22s} {len(where):3d}  {' '.join(where[:8])}{' …' if len(where) > 8 else ''}")
