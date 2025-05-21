# input_parser.py

from typing import Optional, Dict
from datetime import datetime, timedelta
import dateparser
from dateparser.search import search_dates

def parse_deadline(text: str) -> Optional[str]:
    """
    1) If text mentions 'tomorrow' or 'today', handle explicitly.
    2) Else try direct dateparser.parse (handles many natural expressions).
    3) Else scan for explicit dates via search_dates.
    """

    lower = text.lower()

    # 1) Explicit relative terms
    if "tomorrow" in lower:
        dt = datetime.now() + timedelta(days=1)
        # Round to midnight for consistency:
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        return dt.isoformat()
    if "today" in lower:
        dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return dt.isoformat()

    # 2) Direct parse
    dt = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})
    if dt:
        return dt.isoformat()

    # 3) search_dates for explicit fragments
    results = search_dates(
        text,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False
        }
    )
    if results:
        _, dt2 = results[0]
        return dt2.isoformat()

    return None


def parse_input(text: str) -> Dict:
    """
    Day 1 pipeline: only deadline parsing.
    """
    return {"deadline": parse_deadline(text)}


if __name__ == "__main__":
    examples = [
        "Finish report by next Friday",
        "Submit by 2025-06-01 10:00",
        "Do this ASAP",         # None
        "Remind me tomorrow",   # Now explicitly handled
        "Complete today",       # Explicitly handled
    ]
    for s in examples:
        print(f"{s!r} → {parse_input(s)}")
