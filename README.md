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
strip (region chips, 8 regions), a UTC timeline, a three-column grid of short labelled
stories (33 cells), and a footer date-check with sources.

**FINAL status:** 36 stories verified as of 27 Nov ~06:30 WIB (11 base stories + 25
refresh stories — full list with sources and URLs in
`news-image-20261126-refresh-log.txt`). The morning draft (12 stories) is superseded.
Refresh slots R18 (Ecuador IMF — decided 23 Nov) and R28 (COP31 — ended 22 Nov) were
correctly left empty: both are verifiably not 26 Nov events.

## How it is built

- `render_final.py` draws the layout and all text locally with PIL (DejaVu Sans) from
  the verified story list in `news-image-20261126-refresh-log.txt`, and pastes the three
  photorealistic hero photos (`ai-hero/*-photo-*.png`) into the hero cells with an
  aspect-preserving center-crop (never stretched). No network, no randomness, no clock.
  (`render_hybrid.py` is the morning-draft script, kept for reference.)
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

## Verification (refresher, final — by eye)

- Re-read the rendered PNG directly: the date is huge and readable, all 36 stories
  spelled correctly, no garbled text, no 25 Nov stories, 8 regions, 3 hero photos
  undistorted (EU flag whole, lightning over the coast, red balloon whole above the
  skyline). Two v1 defects found and fixed: timeline title overlapped the "04:45 UCL
  results" label (title shortened to "UTC TIMELINE"); hero 1 source line clipped at
  the cell bottom (photo 98→94 px, labels moved up 4 px). Re-read after fix: both clean.
- Shrunk to 300 px: the date, the three hero photos, and the grid headlines are still
  readable; grid bodies are small at that width (expected at 36-story density).
- `entry.png` final: 1024×1024, 330.954 byte, sha256
  `678d1575f48bfb3e46572541b918eadeb599cb5c519abd0e7c92810fd4a8fd62`.
- `main.py` run twice with different `MAKEFUN_OUTPUT_DIR` values → identical sha256
  (678d1575…).
