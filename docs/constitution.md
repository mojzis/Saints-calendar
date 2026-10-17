---
title: Saints calendar
pitch: A Google Calendar with a saint (and Czech name day) for every day.
created: 2026-10-17
updated: 2026-10-17
---

# Saints calendar

## Purpose

"I would like to have a google calendar of saints for every day." No good ready-made feed exists, so this repo builds one from open data.

## Goals

- Saints of the day in Google Calendar, from the Czech national liturgical calendar.
- Czech name days for every day.
- Files that can be subscribed to by URL, so fixes reach the calendar without re-importing.

## Non-goals

- A full liturgical calendar app (readings, seasons, colours).

## Principles

- Build from open, citable data; keep the source files in `data/`.
- The generated `.ics` files are committed, so their raw URLs work as feeds.

## Open questions

- Fill the days without a saint from the Roman Martyrology (every day has several)?
- Add movable feasts (Easter-based), which need dates per year?
- Offer other calendars too (General Roman Calendar in English or Latin)?
