# The Thousand and One Words
### The Saga of the Shattered Lexicon

A 100-chapter comic, loosely based on the Arabian Nights, that teaches the 1,000 most common SAT words. It's written for readers around 14 to 16.

![Cast](images/characters/_cast_lineup.svg)

Shahrazad told a thousand and one stories to save one life. Here, a thousand words have to be saved to save a city. The Silencer, Grand Vizier Zulmat, has scattered 1,000 word-sparks across the Round City of Baghdad. Getting them back falls to a rooftop courier who can barely read, a scribe who's scared of heights, and a djinn made of living ink. Each chapter takes place at one landmark, covers ten words and ends on a cliffhanger.

## How the words stick

Every page uses three memory techniques at once, so a reader can lean on whichever one works for them.

| Method | Good for readers who remember... | How it shows up |
|---|---|---|
| **Story** | plots and characters | each word is said or acted out in a scene |
| **Link** | weird pictures | consecutive words are chained with OAES images (Out of proportion, Action, Exaggeration, Substitution), plus a sound-alike hook |
| **Loci** | places | 100 landmarks along one spiral route through the city. Every landmark has the same 10 stations: arch, step, lamp, rug, heart, pillar, window, stair, balcony, top |

## What's in the repo

| What | Where |
|---|---|
| Plot summary (2-3 pages) | [02_PLOT.md](02_PLOT.md) |
| All 100 chapters and 1,000 words, with a glossary | [03_CHAPTERS.md](03_CHAPTERS.md), data in [data/saga.json](data/saga.json) |
| City layout (100 landmarks, 10 stations each) | [04_CITY_LAYOUT.md](04_CITY_LAYOUT.md) |
| Characters, with image prompts | [05_CHARACTERS.md](05_CHARACTERS.md) |
| Character art | [images/characters/](images/characters/) |
| City map | [images/city_map.svg](images/city_map.svg) |
| The 100 chapter pages, with an image prompt for every frame | [chapters/index.html](chapters/index.html) (`chapters/chapter_001.html` to `chapter_100.html`; prompts alone are in `chapters/chapter_NNN_prompts.md`) |
| The full comic script in one file | [06_ALL_CHAPTERS.md](06_ALL_CHAPTERS.md) |

## Page layout

Each chapter is one page. The top has the chapter number, title and landmark. Under that is a 3×3 grid (frames 1-9, one word each) and a wide cliffhanger frame for word 10, which I call frame 0. Each frame has a Story, Link and Loci row underneath.

The link chain goes 1→2 in frame 1, 2→3 in frame 2, and so on up to 9→10. Frame 0 then links word 10 to the first word of the next chapter. That way all 1,000 words form one continuous chain.

## Building the pages

```
content/b00.txt … b13.txt   script for all 100 chapters (story, sound hook, link, loci and image prompt per frame)
data/saga.json              the 1,000 words with meanings, chapters and landmarks
src/build_text.py           python3 src/build_text.py  → chapters/*.html, chapters/*_prompts.md, 06_ALL_CHAPTERS.md
src/art.py, characters.py, citymap.py   vector character sheets and the city map
```

To change something, edit the line in `content/` and run `build_text.py` again. Every page gets rebuilt.
