# Saints calendar

A Google Calendar of saints, repeating every year: the saints from the Czech national liturgical calendar (fixed dates; movable feasts such as Easter are left out), 214 days, 240 entries. Two versions: [svati-cz.ics](calendars/svati-cz.ics) with Czech titles, [saints-cz-en.ics](calendars/saints-cz-en.ics) with English ones.

## Website

[mojzis.github.io/saints-calendar](https://mojzis.github.io/saints-calendar/) shows today's saint in Czech or English (`site/en/`), the next 7 days, and a month calendar. It also serves the `.ics` files and has one-click "add to Google Calendar" links. Source is in `site/`; `.github/workflows/pages.yml` publishes it on every push to `main`.

Pictures: drop `site/img/<saint id>.jpg` (or `.webp`/`.png`; the id is the one in `data/czech-cs.txt`, e.g. `aquinas`) and rerun the build: it is added to `site/days.json` and shown on the home page on that day.

## Subscribe in Google Calendar

On a computer, open calendar.google.com, click **+** next to "Other calendars", choose **From URL** and paste:

```
https://raw.githubusercontent.com/mojzis/saints-calendar/main/calendars/svati-cz.ics
https://raw.githubusercontent.com/mojzis/saints-calendar/main/calendars/saints-cz-en.ics
```

A subscribed calendar picks up changes pushed here (Google refreshes it every few hours to a day). To get a static copy instead, download the file and use Settings → **Import & export** → **Import**.

## Rebuild

```
uv sync
uv run saints-calendar
```

This rewrites `calendars/` and `site/days.json` from `data/`.

## Data

- `data/czech-cs.txt`: Czech national calendar from [calendarium-romanum](https://github.com/igneus/calendarium-romanum/blob/master/data/czech-cs.txt) (based on liturgie.cz).
- `data/universal-en.txt`: English titles of the General Roman Calendar, from the same project.
- `data/czech-en.json`: English titles for the Czech-only saints, by id.

See [docs/research/data-sources.md](docs/research/data-sources.md) for what else was looked at.

## Origin

This project started as an idea in [mojzis/ideas](https://github.com/mojzis/ideas/blob/main/ideas/saints-calendar.md).
