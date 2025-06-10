# -------------------- Imports --------------------
from scheduler import (
    create_schedule_entry,
    save_schedule,
    task_store,
    view_tasks_by_assignee,
    delete_task_by_id,
    prioritize_tasks
)
from google_calendar import get_busy_times, is_conflict, find_next_available_slot
from dateutil.parser import parse
from datetime import timedelta  # ✅ Fixed: missing import added

# -------------------- Week 3 Day 2: Test create_schedule_entry --------------------
def test_create_schedule_entry_valid():
    parsed = {
        "assignee": "Priyan",
        "employee_id": "EMP001",
        "action": "call",
        "deadline": "2025-06-01T17:00"
    }

    schedule = create_schedule_entry(parsed)

    assert schedule["title"] == "Call task for Priyan"
    assert schedule["assigned_to"] == "Priyan"
    assert schedule["deadline"] == "2025-06-01T17:00"
    assert schedule["task_id"].startswith("TASK-PRIYAN-")  # ✅ Fixed: use uppercase
    assert schedule["priority"] == "Medium"

# -------------------- Week 3 Day 2: Test save_schedule --------------------
def test_save_schedule_adds_task():
    task_store.clear()

    parsed = {
        "assignee": "Priyan",
        "employee_id": "EMP001",
        "action": "call",
        "deadline": "2025-06-01T17:00"
    }
    schedule = create_schedule_entry(parsed)
    save_schedule(schedule)

    assert len(task_store) == 1
    assert task_store[0]["assigned_to"] == "Priyan"
    assert task_store[0]["title"] == "Call task for Priyan"

# -------------------- Week 3 Day 4: Test view_tasks_by_assignee --------------------
def test_view_tasks_by_assignee():
    task_store.clear()

    parsed = {
        "assignee": "Henali",
        "employee_id": "EMP002",
        "action": "email",
        "deadline": "2025-06-02T10:00"
    }
    schedule = create_schedule_entry(parsed)
    save_schedule(schedule)

    view_tasks_by_assignee("Henali")  # Should print task for Henali

# -------------------- Week 3 Day 5: Test delete_task_by_id --------------------
def test_delete_task_by_id():
    task_store.clear()

    parsed = {
        "assignee": "Anusri",
        "employee_id": "EMP003",
        "action": "remind",
        "deadline": "2025-06-03T09:00"
    }
    schedule = create_schedule_entry(parsed)
    save_schedule(schedule)

    task_id = schedule["task_id"]
    delete_task_by_id(task_id)

    assert len(task_store) == 0

# -------------------- Week 3 Day 5: Test prioritize_tasks --------------------
def test_prioritize_tasks():
    task_store.clear()

    parsed_high = {
        "assignee": "Priyan",
        "employee_id": "EMP001",
        "action": "submit",
        "deadline": "2025-06-02T10:00",
        "priority": "High"
    }

    parsed_low = {
        "assignee": "Henali",
        "employee_id": "EMP002",
        "action": "review",
        "deadline": "2025-06-01T10:00",
        "priority": "Low"
    }

    schedule_high = create_schedule_entry(parsed_high)
    schedule_low = create_schedule_entry(parsed_low)

    save_schedule(schedule_high)
    save_schedule(schedule_low)

    prioritize_tasks()
    assert task_store[0]["priority"] == "High"  # ✅ Optional: Confirm order

# -------------------- Week 4 Day 5: Test scheduling with conflict check --------------------
def test_schedule_with_conflict_check():
    task_store.clear()

    parsed = {
        "assignee": "Priyan",
        "employee_id": "EMP001",
        "action": "call",
        "deadline": "2025-06-01T15:00",
        "priority": "High"
    }
    schedule = create_schedule_entry(parsed)
    busy_times = get_busy_times()

    start_dt = parse(schedule["deadline"])
    end_dt = start_dt + timedelta(minutes=30)

    if is_conflict(start_dt.isoformat(), end_dt.isoformat(), busy_times):
        suggested = find_next_available_slot(busy_times, 30, start_dt.isoformat())
        assert suggested is not None  # ✅ Ensures suggestion exists
        print(f"[SUGGESTION] Consider rescheduling to start at: {suggested}")
    else:
        save_schedule(schedule)
        assert schedule in task_store
