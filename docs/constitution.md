---
title: Saints calendar
pitch: A Google Calendar with a saint for every day.
created: 2026-10-17
updated: 2026-10-17
idea: https://github.com/mojzis/ideas/blob/main/ideas/saints-calendar.md
---

# Saints calendar

<!-- Seeded from the idea file in mojzis/ideas when this repo was created. -->

## Purpose

"I would like to have a google calendar of saints for every day." No good ready-made feed exists, so this repo builds one from open data.

## Goals

- Saints of the day in Google Calendar, from the Czech national liturgical calendar, in Czech and English.
- Files that can be subscribed to by URL, so fixes reach the calendar without re-importing.

## Non-goals

- Czech name days (dropped 2026-10-17; not wanted).
- A full liturgical calendar app (readings, seasons, colours).

## Principles

- Build from open, citable data; keep the source files in `data/`.
- The generated `.ics` files are committed, so their raw URLs work as feeds.

## Open questions

- Fill the days without a saint from the Roman Martyrology (every day has several)?
- Add movable feasts (Easter-based), which need dates per year?
- Offer other calendars too (General Roman Calendar in English or Latin)?
