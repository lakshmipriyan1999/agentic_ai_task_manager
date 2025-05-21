# test_input_parser.py

import pytest
from input_parser import parse_deadline, parse_input

@pytest.mark.parametrize("txt", [
    "Finish by next Monday",
    "Due date: 2025-06-01 at 15:00",
    "Remind me tomorrow",     # Should now work
    "Complete today"          # And this
])
def test_parse_deadline_returns_date(txt):
    val = parse_deadline(txt)
    assert val is not None, f"parse_deadline failed on: {txt!r}"
    assert "T" in val

def test_parse_input_dict():
    res = parse_input("Finish report by Friday")
    assert "deadline" in res
    assert res["deadline"] is not None
    assert "T" in res["deadline"]
