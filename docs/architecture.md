# Architecture

## Overview

One script, [src/saints_calendar/build.py](../src/saints_calendar/build.py), reads the source data in `data/` and writes an iCalendar file to `calendars/` plus `site/days.json` for the website. Every entry is an all-day event with `RRULE:FREQ=YEARLY`, starting in 2026 (29 February starts in 2028).

## Data

- `data/czech-cs.txt`: calendarium-romanum sanctorale format. `= M` starts a month; each line is `day [rank] [colour] id : title`. Rank letters: `s` solemnity, `f` feast, `m` memorial, none for an optional memorial.

## Flows

`uv run saints-calendar` → `calendars/svati-cz.ics` → Google Calendar subscribes to its raw GitHub URL.

`site/` (static HTML + `app.js`, which reads `days.json` keyed `"MM-DD"`) + `calendars/` → GitHub Pages via `.github/workflows/pages.yml`. The workflow reruns the build and fails if the committed output is stale.
