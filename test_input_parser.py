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
    ("Call Priyan ASAP", "call"),
    ("Email Anusri the report", "email"),
    ("No verbs here", ""),
])
def test_parse_action(txt, expected):
    assert parse_action(txt) == expected

# ----------------- Test: Assignee Extraction -----------------
@pytest.mark.parametrize("txt, assignee", [
    ("Email Henali the report", "Henali"),
    ("Call Priyan tomorrow", "Priyan"),
    ("Send docs to Anusri by Friday", "Anusri"),
    ("Schedule meeting", None),  # No name
    ("Remind Poluru Krishna to update", None),  # Not in TEAM
])
def test_parse_assignee(txt, assignee):
    assert parse_assignee(txt, TEAM) == assignee

# ----------------- Test: Combined parse_input -----------------
def test_parse_input_dict():
    res = parse_input("Email Henali the report by Friday")

    assert "task_id" in res
    assert res["task_id"].startswith("TASK-HENALI-")  # ✅ Fixed: uppercase

    assert "employee_id" in res
    assert res["employee_id"] == "EMP002"

    assert res["assignee"] == "Henali"
    assert res["action"] == "email"
    assert res["deadline"] is not None

# ----------------- Test: parse_input() variations for Week 2 Day 5 -----------------
@pytest.mark.parametrize("txt,expected", [
    ("Email Henali the report by Friday", {
        "assignee": "Henali",
        "employee_id": "EMP002",
        "action": "email",
        "deadline_contains": "T",
        "task_id_prefix": "TASK-HENALI-"  # ✅ Fixed
    }),
    ("Call Priyan tomorrow", {
        "assignee": "Priyan",
        "employee_id": "EMP001",
        "action": "call",
        "deadline_contains": "T",
        "task_id_prefix": "TASK-PRIYAN-"  # ✅ Fixed
    }),
    ("Schedule meeting next week", {
        "assignee": None,
        "employee_id": None,
        "action": "schedule",
        "deadline_contains": "T",
        "task_id_prefix": None
    }),
    ("Remind Anusri to submit", {
        "assignee": "Anusri",
        "employee_id": "EMP003",
        "action": "remind",
        "deadline_contains": None,
        "task_id_prefix": "TASK-ANUSRI-"  # ✅ Fixed
    }),
])
def test_parse_input_variations(txt, expected):
    res = parse_input(txt)
    assert res["assignee"] == expected["assignee"]
    assert res["employee_id"] == expected["employee_id"]
    assert res["action"] == expected["action"]

    if expected["deadline_contains"]:
        assert res["deadline"] is not None
        assert expected["deadline_contains"] in res["deadline"]
    else:
        assert res["deadline"] is None

    if expected["task_id_prefix"]:
        assert res["task_id"].startswith(expected["task_id_prefix"])  # ✅ Fixed
    else:
        assert res["task_id"] is None
