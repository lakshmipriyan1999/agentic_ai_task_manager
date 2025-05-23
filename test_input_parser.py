import pytest
from input_parser import parse_deadline, parse_action, parse_assignee, parse_input, TEAM

# ----------------- Test: Deadline Parsing -----------------
@pytest.mark.parametrize("txt", [
    "Finish by next Monday",
    "Due date: 2025-06-01 at 15:00",
    "Remind me tomorrow",
    "Complete today"
])
def test_parse_deadline_returns_date(txt):
    val = parse_deadline(txt)
    assert val is not None
    assert "T" in val

# ----------------- Test: Action Extraction -----------------
@pytest.mark.parametrize("txt, expected", [
    ("Schedule meeting tomorrow", "schedule"),
    ("Prepare slides by Friday", "prepare"),
    ("Call Alice ASAP", "call"),
    ("Email Carol the report", "email"),
    ("No verbs here", ""),
])
def test_parse_action(txt, expected):
    assert parse_action(txt) == expected

# ----------------- Test: Assignee Extraction -----------------
@pytest.mark.parametrize("txt, assignee", [
    ("Email Bob the report", "Bob"),
    ("Call Alice tomorrow", "Alice"),
    ("Send docs to Carol by Friday", "Carol"),
    ("Schedule meeting", None),  # No name
    ("Remind Poluru Krishna to update", None),  # Not in TEAM
])
def test_parse_assignee(txt, assignee):
    assert parse_assignee(txt, TEAM) == assignee

# ----------------- Test: Combined parse_input -----------------
def test_parse_input_dict():
    res = parse_input("Email Bob the report by Friday")

    assert "task_id" in res
    assert res["task_id"].startswith("TASK-BOB-")

    assert "employee_id" in res
    assert res["employee_id"] == "EMP002"

    assert res["assignee"] == "Bob"
    assert res["action"] == "email"
    assert res["deadline"] is not None


