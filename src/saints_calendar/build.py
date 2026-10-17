"""Build the .ics files in calendars/ from the data in data/.

Run with `uv run saints-calendar` from the repo root.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "calendars"
START_YEAR = 2026
LEAP_START = "20280229"
RANKS = {"s": "slavnost", "f": "svátek", "m": "památka"}

# State holidays have no name day in the civil calendar; show them so every day
# has an entry.
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


def saints(text: str) -> list[Event]:
    """Events from a calendarium-romanum sanctorale file."""
    events, month = [], 0
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
        desc = f"{rank} (Český národní liturgický kalendář)"
        uid = f"svati-{month:02d}{day:02d}-{sid}@saints-calendar"
        events.append(event(uid, month, day, title, desc))
    return events


def namedays(data: dict[str, str | list[str]]) -> list[Event]:
    """Events from a {"MM-DD": name or [names]} mapping, plus state holidays."""
    events = []
    entries: list[tuple[str, str, str]] = [
        (key, title, "Státní svátek") for key, title in HOLIDAYS.items()
    ]
    for key, names in data.items():
        listed = [names] if isinstance(names, str) else names
        entries.append((key, "Svátek: " + ", ".join(listed), "Český občanský kalendář"))
    for key, title, desc in sorted(entries):
        month, day = map(int, key.split("-"))
        events.append(
            event(
                f"jmeniny-{month:02d}{day:02d}@saints-calendar", month, day, title, desc
            )
        )
    return events


def main() -> None:
    """Write calendars/svati-cz.ics and calendars/jmeniny-cz.ics."""
    OUT.mkdir(exist_ok=True)
    svati = saints((DATA / "czech-cs.txt").read_text(encoding="utf-8"))
    jmeniny = namedays(
        json.loads((DATA / "jmeniny-cs.json").read_text(encoding="utf-8"))
    )
    with (OUT / "svati-cz.ics").open("w", encoding="utf-8", newline="") as f:
        f.write(calendar("Svatí (liturgický kalendář CZ)", svati))
    with (OUT / "jmeniny-cz.ics").open("w", encoding="utf-8", newline="") as f:
        f.write(calendar("Jmeniny CZ", jmeniny))
