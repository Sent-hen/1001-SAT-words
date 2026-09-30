# Report · Three images per frame (Story Panel · Memory Card · Route Map)

Branch `three-images`. Build: `python src/build_text.py` (on this Windows machine `python3` is only the Store stub, so use `python`). Checks: `python tools/check_pages.py --browser`, which reports **PASS**.

## What changed

| Area | Change |
|---|---|
| `src/routemap.py` (new) | **Route Map**, a 300×300 night-mode crop of the city map. It has a YOU ARE HERE pin with a pulse (off under `prefers-reduced-motion`), a dashed `10 8` leg to the next landmark (50% opacity on frames 1–9, full opacity and thicker on Frame 0, where it carries a "→ next chapter" tag), the traveled route (lime) and future stops (hollow, dotted), and a station strip that highlights the current station. The 100 → 1 loop closes. Every map has a `<title>`/`<desc>`, and the label pills are placed so they never cover the pin or the next stop. |
| `src/citymap.py` | `svg()` is split into `body()` + `route_layer()` + `chrome_layer()`, and `sand` is renamed `cm-sand`. `svg()` output is otherwise identical. `images/city_map.svg` was not regenerated, which keeps its C2PA metadata. |
| `src/memcard.py` (new) | **Memory Card**, 300×300. It has a radial purple dream gradient with a pink glow, a double gold border and sparkles. `station_stage(k, tint)` draws 10 fixed station templates re-tinted per district. Object A sits on the station and object B is drawn beside it, joined by a pink 5px link arrow labelled with the action. It also has action effects, the `① ARCH`-style badge, O/A/E/S chips lit from the `L:` tags, and `<title>`/`<desc>`. A generic fallback card is used when a frame has no card line. |
| `src/objects.py` (new) | Object library of **593 keys** plus aliases and people roles. Factories cover quadrupeds, birds, bugs and people; people are built on `human()`, the existing NPC specs and `SPECS`. The rest are things, reusing `props.py` and `ch001.crow`. Mods (colours, `many`, `lying`, hats, moods, `glowing`…) are supported, and unknown nouns fall back to a labelled thought bubble. |
| `src/content.py` | New `parse_cards()` and `_noun()`. `parse()` and `validate()` are untouched. |
| `src/build_text.py` | New image row (card + map), `📖 STORY` / `🔗 MEMORY CARD` / `🗺️ ROUTE` caption tabs, and a sticky **Story · Card · Map** toolbar that remembers its state in `localStorage` inside `try/catch`. The base map is inlined once per page. Frame 0 shows two centred 300px squares; the row stacks below 600px, and toolbar and pulse are off in print. The index page is unchanged. |
| `content/cards/cards_NNN-MMM.txt` (new) | 1000 card lines, all reviewed (see below). |
| `tools/` (new) | `draft_cards.py`, `card_coverage.py`, `check_pages.py`, `fill_oaes.py` (sets each OAES field from its `L:` tags), `show_links.py` and `objects_sheet.py`. |

No file under `content/b*.txt`, `data/saga.json` or `*.md` changed. `check_pages.py` verifies all 21 files against the baseline commit `7d54b60` by checksum, and verifies all 1000 rendered story/link/loci/hook/prompt texts against `content/`. `06_ALL_CHAPTERS.md` regenerates byte-identical.

## Cards: which chapters were reviewed

- **Chapter 1** was written by hand from its `L:` lines.
- **Chapters 2–100** were drafted by `tools/draft_cards.py` and then **reviewed by hand in 10 batches** (2–10, 11–20, …, 91–100) against every `L:` line, with the coverage report run after each batch. Review kept the drafted object B in 687/990 frames (69%) and changed 303. Object A usually chains from the previous link's B, but where the `L:` text names A differently (e.g. "the broom-and-bucket army (makeshift)"), the card follows the text.
- The unreviewed drafts are kept in `content/cards/drafts/` for comparison. The build never reads them.

## Fallback coverage

- **1000/1000 frames have a card line.** No frame uses the generic fallback card.
- **2000/2000 card objects are drawn from the library**, so the thought-bubble fallback is never used. Of these, 1722 are drawn under their own name and 278 through an alias or role. Some aliases are loose approximations (e.g. `knee` → skeleton, `verge` → flower, `hallway` → door), so "drawn" does not always mean "exact". `tools/card_coverage.py` lists any nouns that would fall back.

## Page sizes

Maximum **502 KB** (chapter 85), median 382 KB; the limit is 700 KB. Pages were 236 KB (chapter 1) before. The base map is inlined once per page as `<symbol id="cm-base">` (~10 KB), and each route map draws only the route points near its crop.

## Contrast (printed by `check_pages.py`)

| Pair | Ratio | Required |
|---|---|---|
| pin outer ring (white) vs lightest darkened map | 5.34:1 | ✓ |
| pin core `--here` vs its dark ring | 4.91:1 | ✓ |
| label text white on pill | 17.00:1 | ✓ |
| "YOU ARE HERE" `--here` on pill | 4.91:1 | ✓ |
| NEXT `--next` on pill | 11.05:1 | ✓ |

The raw magenta core measures only 1.54:1 against the brightest darkened map, so the pin is built as white ring → dark ring → magenta core and each adjacent pair clears 4.5:1. The night mode is feColorMatrix `saturate 0.15`, then an extra `slope 0.8` dim, then a `#0f1d2e` overlay at 55%. Without the dim step, the white ring only reached about 4.2:1 against the lightest map colour.

## Deviations from the task text

1. **The hidden base-map SVG is zero-size and absolutely positioned, not `display:none`.** Chrome renders both identically (tested). Firefox has historically not applied patterns and filters from a `display:none` subtree; that was not tested here.
2. **Route overlays** (dots, legs, pin, labels) are drawn in 300×240 window pixels, projected from map coordinates, rather than inside the map-coordinate `<svg>`. This keeps line widths and label sizes constant whatever the crop zoom. The map-coordinate positions are kept in `data-at` and `data-to` and verified by the checker.
3. **"Compare with `git show main:content/`"**: `main` has no `content/` (it was untracked), so the branch's first commit `7d54b60` records the untouched baseline and the checker compares against that. It will use `main` automatically once `main` has `content/`.
4. **Generic people roles** (kid, athlete, sailor, queen…) use the existing NPC specs rather than the main cast. That way Zayn, Layla, Hakim etc. appear on a card only when the story names them.

## Story-panel bugs fixed

No story-panel drawing was changed. Build and tooling fixes (Windows):

- Every `open()` in `src/` now reads and writes UTF-8 (and writes LF). The Windows cp1252 default mangled "cliché", which made `content.validate()` fail and stopped the build.
- `citymap.py` resolved `../data` relative to the working directory, not the file.
- `shot.py` wrote to `/tmp`, built a `file://` URL by string concatenation, and never stripped the `@import` inside the page `<style>`. It now uses `tempfile` and `pathlib`, strips the import, and falls back to the system Chrome or Edge.

After the rebuild, 96/100 pages were byte-identical to the originals. Four differ only in the last digit of some floats, from the platform's math library.

## Screenshots

`docs/baseline_ch001.png` (before), `docs/screens/chapter_001/025/050/075/100.png`, `docs/screens/chapter_050_mobile.png` and `docs/screens/step2_routemaps_ch1-10-20-50-100-6.png`.
