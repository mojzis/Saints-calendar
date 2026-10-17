"""Build the .ics files in calendars/ from the data in data/.

Run with `uv run saints-calendar` from the repo root.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "calendars"
SITE = ROOT / "site"
IMAGE_EXTS = (".webp", ".jpg", ".jpeg", ".png")
START_YEAR = 2026
LEAP_START = "20280229"
RANKS = {"s": "slavnost", "f": "svátek", "m": "památka"}

# State holidays, shown on the website next to the saints.
HOLIDAYS = {
    "01-01": "Nový rok, Den obnovy samostatného českého státu",
    "05-01": "Svátek práce",
    "05-08": "Den vítězství",
    "07-06": "Den upálení mistra Jana Husa",
    "12-25": "1. svátek vánoční",
}

Event = list[str]


def fold(line: str) -> str:
    """Fold a content line at 75 octets, as RFC 5545 requires."""
    out, cur = [], b""
    for ch in line:
        b = ch.encode()
        if len(cur) + len(b) > 75:  # noqa: PLR2004
            out.append(cur.decode())
            cur = b" "
        cur += b
    out.append(cur.decode())
    return "\r\n".join(out)


def esc(text: str) -> str:
    """Escape a TEXT value."""
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def event(uid: str, month: int, day: int, summary: str, desc: str) -> Event:
    """One all-day event that repeats every year."""
    start = f"{START_YEAR}{month:02d}{day:02d}"
    rule = "RRULE:FREQ=YEARLY"
    if (month, day) == (2, 29):
        start, rule = LEAP_START, "RRULE:FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=29"
    return [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{START_YEAR}0101T000000Z",
        f"DTSTART;VALUE=DATE:{start}",
        rule,
        f"SUMMARY:{esc(summary)}",
        f"DESCRIPTION:{esc(desc)}",
        "TRANSP:TRANSPARENT",
        "END:VEVENT",
    ]


def calendar(name: str, events: list[Event]) -> str:
    """Wrap events in a VCALENDAR."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//mojzis//saints-calendar//CS",
        "CALSCALE:GREGORIAN",
        f"X-WR-CALNAME:{name}",
        "X-WR-TIMEZONE:Europe/Prague",
    ]
    for ev in events:
        lines += ev
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(line) for line in lines) + "\r\n"


def parse_saints(text: str) -> list[dict[str, str | int]]:
    """Records from a calendarium-romanum sanctorale file."""
    records: list[dict[str, str | int]] = []
    month = 0
    for raw in text.splitlines():
        if raw.startswith("= "):
            month = int(raw[2:])
            continue
        if " : " not in raw or not month:
            continue
        left, title = raw.split(" : ", 1)
        tokens = left.split()
        day, sid, flags = int(tokens[0]), tokens[-1], tokens[1:-1]
        rank = next((RANKS[f[0]] for f in flags if f[0] in RANKS), "nezávazná památka")
        records.append(
            {"month": month, "day": day, "id": sid, "title": title, "rank": rank}
        )
    return records


def saints(text: str) -> list[Event]:
    """Events from a calendarium-romanum sanctorale file."""
    events = []
    for r in parse_saints(text):
        month, day = int(r["month"]), int(r["day"])
        desc = f"{r['rank']} (Český národní liturgický kalendář)"
        uid = f"svati-{month:02d}{day:02d}-{r['id']}@saints-calendar"
        events.append(event(uid, month, day, str(r["title"]), desc))
    return events


def site_days(saint_text: str, images: set[str]) -> dict[str, dict]:
    """Per-day data for the website, keyed "MM-DD".

    `images` holds file names found in site/img/; a saint gets an "image"
    when a file named after its id is there (e.g. site/img/aquinas.jpg).
    """
    days: dict[str, dict] = {}
    for key, title in HOLIDAYS.items():
        days.setdefault(key, {})["holiday"] = title
    for r in parse_saints(saint_text):
        key = f"{int(r['month']):02d}-{int(r['day']):02d}"
        saint = {"id": r["id"], "title": r["title"], "rank": r["rank"]}
        image = next(
            (f"img/{r['id']}{e}" for e in IMAGE_EXTS if f"{r['id']}{e}" in images), None
        )
        if image:
            saint["image"] = image
        days.setdefault(key, {}).setdefault("saints", []).append(saint)
    return dict(sorted(days.items()))


def main() -> None:
    """Write calendars/*.ics and site/days.json."""
    OUT.mkdir(exist_ok=True)
    saint_text = (DATA / "czech-cs.txt").read_text(encoding="utf-8")
    with (OUT / "svati-cz.ics").open("w", encoding="utf-8", newline="") as f:
        f.write(calendar("Svatí (liturgický kalendář CZ)", saints(saint_text)))
    img_dir = SITE / "img"
    images = {p.name for p in img_dir.iterdir()} if img_dir.is_dir() else set()
    days = site_days(saint_text, images)
    (SITE / "days.json").write_text(
        json.dumps(days, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
