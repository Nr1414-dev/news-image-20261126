# news-image-20261126 — The World in One Day

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Nr1414-dev/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Nr1414-dev/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image summing up the world's news of **Thursday 26 November 2026**, for make.fun's
[news-image-20261126](https://make.fun/bounty/news-image-20261126) bounty ($100, 50 places).
An AI judge that can see images compares entries two at a time; the 50 best win rates share the prize.

## The image

A 1024×1024 "World Broadsheet": masthead with the date as large as possible (the judge is
not told which day is judged), a hero row of the three biggest stories as photorealistic
images (AI-generated, verified by eye — no text, no faces, no wrong flags), a locator
strip (regions + cities), a UTC timeline, a two-column grid of short labelled stories,
and a footer date-check with sources.

**DRAFT status:** this commit holds the morning draft — 12 stories verified as of 26 Nov
07:15 WIB (11 from research + the 9 Wednesday Champions League results, first reported
in Asia on 26 Nov). The final image (36–40 stories) comes after the evening refresh pass
on 26 Nov (27 Nov 00:00–07:00 WIB), when the day's events have actually happened.

## How it is built

- `render_hybrid.py` draws the layout and all text locally with PIL (DejaVu Sans) from
  the verified story list in `news-image-20261126-refresh-log.txt`, and pastes the three
  photorealistic hero photos (`ai-hero/*-photo-*.png`) into the hero cells with an
  aspect-preserving center-crop (never stretched). No network, no randomness, no clock.
- `entry.png` is the rendered image (1024×1024, ≤ 1 MiB).
- `main.py` is stdlib-only and only copies `entry.png` to `/output/entry.png`
  (`shutil.copyfile`) — Pillow is not available at grading, and the rules explicitly
  allow a program that copies an image the repository holds. Running it twice writes
  byte-identical output.

## Verification (builder, by eye)

- Read the rendered PNG directly: date readable, every label spelled correctly, no
  garbled text, no 25 Nov stories, forecasts labelled as forecast.
- Shrunk to 300 px: the date and the three hero scenes are still readable.
- `main.py` run twice with different `MAKEFUN_OUTPUT_DIR` values → identical sha256.

## Verification (finisher, by eye — hybrid)

- Re-read the rendered PNG directly: the three photos are not distorted (EU flag whole,
  lightning over the coast, red balloon whole above the skyline), all text unchanged
  and readable, no overlap, no 25 Nov stories.
- Shrunk to 300 px: the date, the three hero photos, and the grid headlines are still readable.
- `entry.png` hybrid: 1024×1024, 292.973 byte, sha256
  `c524657cd2ef07f848e1be8d914ce8edeb6fdf197dfed3bd5c4bebb39f8513cf`;
  rendered twice → byte-identical.
