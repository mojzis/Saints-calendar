# Architecture

## Overview

One script, [src/saints_calendar/build.py](../src/saints_calendar/build.py), reads the source data in `data/` and writes two iCalendar files (Czech and English titles) to `calendars/` plus `site/days.json` for the website. Every entry is an all-day event with `RRULE:FREQ=YEARLY`, starting in 2026 (29 February starts in 2028).

## Data

- `data/czech-cs.txt`: calendarium-romanum sanctorale format. `= M` starts a month; each line is `day [rank] [colour] id : title`. Rank letters: `s` solemnity, `f` feast, `m` memorial, none for an optional memorial.
- `data/universal-en.txt`: same format, General Roman Calendar in English. English titles are looked up by saint id.
- `data/czech-en.json`: `{id: English title}` for Czech-only saints missing from `universal-en.txt`. The build fails on an id with no English title.

## Flows

`uv run saints-calendar` → `calendars/svati-cz.ics`, `calendars/saints-cz-en.ics` → Google Calendar subscribes to their raw GitHub URLs.

`site/` (static HTML + `app.js`, which reads `days.json` keyed `"MM-DD"`; `site/en/` holds the English pages, which load the same `app.js` and pick the language from `<html lang>`) + `calendars/` → GitHub Pages via `.github/workflows/pages.yml`. The workflow reruns the build and fails if the committed output is stale.
