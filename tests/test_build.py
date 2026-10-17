import pytest

from saints_calendar.build import calendar, event, fold, saints, site_days

SAMPLE = """---
title: test
---

= 10
16 hedwig : Sv. Hedviky, řeholnice
17 m R ignatius_of_antioch : Sv. Ignáce Antiochijského, biskupa a mučedníka
"""
EN = {"hedwig": "Saint Hedwig", "ignatius_of_antioch": "Saint Ignatius of Antioch"}


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


def test_saints_in_english_take_titles_by_id():
    names = {
        "hedwig": "Saint Hedwig, religious",
        "ignatius_of_antioch": "Saint Ignatius",
    }
    second = "\n".join(saints(SAMPLE, "en", names)[1])
    assert "SUMMARY:Saint Ignatius" in second
    assert "DESCRIPTION:memorial (Czech national liturgical calendar)" in second
    assert "UID:saints-en-1017-ignatius_of_antioch@saints-calendar" in second


def test_saints_in_english_reject_untranslated_ids():
    with pytest.raises(KeyError, match="ignatius_of_antioch"):
        saints(SAMPLE, "en", {"hedwig": "Saint Hedwig"})


def test_leap_day_repeats_only_on_leap_years():
    lines = event("x", 2, 29, "Horymír", "d")
    assert "DTSTART;VALUE=DATE:20280229" in lines
    assert "RRULE:FREQ=YEARLY;BYMONTH=2;BYMONTHDAY=29" in lines


def test_calendar_wraps_events():
    text = calendar("Test", [event("x", 1, 2, "a", "b")])
    assert text.startswith("BEGIN:VCALENDAR\r\n")
    assert text.endswith("END:VCALENDAR\r\n")


def test_site_days_attaches_images_by_saint_id():
    days = site_days(SAMPLE, EN, {"hedwig.jpg"})
    assert days["10-16"]["saints"] == [
        {
            "id": "hedwig",
            "title": {"cs": "Sv. Hedviky, řeholnice", "en": "Saint Hedwig"},
            "rank": "optional",
            "image": "img/hedwig.jpg",
        }
    ]
    assert "image" not in days["10-17"]["saints"][0]


def test_site_days_adds_holidays():
    days = site_days(SAMPLE, EN, set())
    assert days["05-01"]["holiday"] == {"cs": "Svátek práce", "en": "Labour Day"}
