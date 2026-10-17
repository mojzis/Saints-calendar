from saints_calendar.build import calendar, event, fold, namedays, saints

SAMPLE = """---
title: test
---

= 10
16 hedwig : Sv. Hedviky, řeholnice
17 m R ignatius_of_antioch : Sv. Ignáce Antiochijského, biskupa a mučedníka
"""


def test_fold_keeps_lines_within_75_octets():
    folded = fold("SUMMARY:" + "ž" * 100)
    parts = folded.split("\r\n")
    assert all(len(p.encode()) <= 75 for p in parts)
    assert "".join(p.removeprefix(" ") for p in parts) == "SUMMARY:" + "ž" * 100


def test_saints_parses_rank_and_escapes_commas():
    events = saints(SAMPLE)
    assert len(events) == 2
    second = "\n".join(events[1])
    assert "DTSTART;VALUE=DATE:20261017" in second
    assert "SUMMARY:Sv. Ignáce Antiochijského\\, biskupa a mučedníka" in second
    assert "DESCRIPTION:památka" in second


def test_namedays_cover_holidays_and_lists():
    events = namedays({"10-17": "Hedvika", "01-06": ["Kašpar", "Melichar"]})
    text = "\n".join(line for ev in events for line in ev)
    assert "SUMMARY:Svátek: Hedvika" in text
    assert "SUMMARY:Svátek: Kašpar\\, Melichar" in text
    assert "SUMMARY:Svátek práce" in text


def test_leap_day_repeats_only_on_leap_years():
    lines = event("x", 2, 29, "Horymír", "d")
    assert "DTSTART;VALUE=DATE:20280229" in lines
    assert "RRULE:FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=29" in lines


def test_calendar_wraps_events():
    text = calendar("Test", [event("x", 1, 2, "a", "b")])
    assert text.startswith("BEGIN:VCALENDAR\r\n")
    assert text.endswith("END:VCALENDAR\r\n")
