# Data sources

Checked on 2026-10-17.

## Ready-made feeds

- Google Calendar has no built-in saints or Czech name-day calendar.
- Web searches for subscribable saints `.ics` feeds return mostly spam pages. [calendar.center](https://calendar.center/cz/jmeniny/) lists a Czech name-day calendar (not checked; the site was out of reach).
- [GCatholic](https://gcatholic.org/calendar/2026/CZ-prah0-cs) shows the Czech liturgical calendar per diocese and year, but no feed was found.

## Data used

- [calendarium-romanum](https://github.com/igneus/calendarium-romanum/tree/master/data): plain-text sanctorale files for the General Roman Calendar (en, la, it, ...) and national calendars, including `czech-cs.txt`. Fixed-date entries only.
- [namedays-cs](https://github.com/OzzyCzech/namedays-cs) (MIT, npm): Czech civil name days as JSON.

## Not used yet

- Wikidata (feast-day property on saints) could fill every day, but needs curation.
- The church-calendar API by the calendarium-romanum author (calapi.inadiutorium.cz) computes movable feasts per year.
