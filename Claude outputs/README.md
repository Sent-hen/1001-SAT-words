# THE THOUSAND AND ONE WORDS
## *The Saga of the Shattered Lexicon*

> **A 100-chapter Arabian-Nights comic epic that makes the 1000 most-used SAT words unforgettable, for readers aged 14–16.**
> *Shahrazad told a thousand and one stories to save one life. Now a thousand words must be saved to save a whole city.*

![Cast](images/characters/_cast_lineup.svg)

A rooftop courier who can barely read, a scribe who's terrified of heights, and a djinn made of living ink race through the legendary Round City of Baghdad to recapture 1000 word-sparks scattered by the Silencer, Grand Vizier Zulmat. Each chapter is one landmark, ten words, and one cliff-hanger.

## Three memory methods on every page

| Method | For the kid who… | On the page |
|---|---|---|
| **STORY** | remembers plots and characters | every word is spoken or acted out in a fast, gripping scene |
| **LINK** | remembers crazy pictures | word pairs are chained with **OAES** (Out of proportion, Action, Exaggeration, Substitution) plus a sound-alike hook |
| **LOCI** | remembers places | 100 fixed landmarks on one spiral route, each with the same **10 stations**: ARCH · STEP · LAMP · RUG · HEART · PILLAR · WINDOW · STAIR · BALCONY · TOP |

## Contents (the 108 outputs)

| # | Output | File |
|---|---|---|
| 1 | Epic name | this README |
| 2 | Plot (2–3 pages) | [02_PLOT.md](02_PLOT.md) |
| 3 | 100 chapters and 1000 words (+ glossary) | [03_CHAPTERS.md](03_CHAPTERS.md) · data: [data/saga.json](data/saga.json) |
| 4 | City layout (100 landmarks, 10 stations) | [04_CITY_LAYOUT.md](04_CITY_LAYOUT.md) |
| 5 | Characters (+ AI image prompts) | [05_CHARACTERS.md](05_CHARACTERS.md) |
| 6 | Character pictures | [images/characters/](images/characters/) |
| 7 | City map picture | [images/city_map.svg](images/city_map.svg) |
| 8–108 | All 100 chapter pages (words 1–1000) with an image prompt in every frame | [chapters/index.html](chapters/index.html) → `chapters/chapter_001.html` … `chapter_100.html` · prompts only: `chapters/chapter_NNN_prompts.md` |
| + | The complete comic script in one file | [06_ALL_CHAPTERS.md](06_ALL_CHAPTERS.md) |

## Page format

Each chapter is one page. At the top are the chapter number, the title and the landmark. Below that is a 3×3 grid of frames (**Frames 1–9**, words 1–9) and a wide cliff-hanger **Frame 0** (word 10). Under every frame are three rows: **STORY**, **LINK** and **LOCI**. The link chain runs 1→2 in Frame 1 through 9→10 in Frame 9. Frame 0 links word 10 to word 1 of the *next* chapter, so all 1000 words form one unbroken chain.

## How pages are built

```
content/b00.txt … b13.txt   the script of all 100 chapters (story, sound-hook, link, loci, image prompt per frame)
data/saga.json              the 1000 words, meanings, chapters and landmarks
src/build_text.py           python3 src/build_text.py  → chapters/*.html, chapters/*_prompts.md, 06_ALL_CHAPTERS.md
src/art.py, characters.py, citymap.py   the vector character sheets and city map
```
Edit a line in `content/`, re-run `build_text.py`, and every page updates.
