# Architecture

## Overview

One script, [src/saints_calendar/build.py](../src/saints_calendar/build.py), reads the source data in `data/` and writes two iCalendar files to `calendars/`. Every entry is an all-day event with `RRULE:FREQ=YEARLY`, starting in 2026 (29 February starts in 2028).

## Data

- `data/czech-cs.txt`: calendarium-romanum sanctorale format. `= M` starts a month; each line is `day [rank] [colour] id : title`. Rank letters: `s` solemnity, `f` feast, `m` memorial, none for an optional memorial.
- `data/jmeniny-cs.json`: `{"MM-DD": name or [names]}`, 361 days. The five state holidays without a name day are added in code.

## Flows

`uv run saints-calendar` → `calendars/svati-cz.ics`, `calendars/jmeniny-cz.ics` → Google Calendar subscribes to their raw GitHub URLs.
