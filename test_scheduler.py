# -------------------- Imports --------------------
from scheduler import (
    create_schedule_entry,
    save_schedule,
    task_store,
    view_tasks_by_assignee,
    delete_task_by_id,
    prioritize_tasks
)

# -------------------- Week 3 Day 2: Test create_schedule_entry --------------------
def test_create_schedule_entry_valid():
    parsed = {
        "assignee": "Alice",
        "employee_id": "EMP001",
        "action": "call",
        "deadline": "2025-06-01T17:00"
    }

    schedule = create_schedule_entry(parsed)

    assert schedule["title"] == "Call task for Alice"
    assert schedule["assigned_to"] == "Alice"
    assert schedule["deadline"] == "2025-06-01T17:00"
    assert schedule["task_id"].startswith("TASK-ALICE-")
    assert schedule["priority"] == "Medium"  # Default priority

# -------------------- Week 3 Day 2: Test save_schedule --------------------
def test_save_schedule_adds_task():
    task_store.clear()

    parsed = {
        "assignee": "Alice",
        "employee_id": "EMP001",
        "action": "call",
        "deadline": "2025-06-01T17:00"
    }
    schedule = create_schedule_entry(parsed)
    save_schedule(schedule)

    assert len(task_store) == 1
    assert task_store[0]["assigned_to"] == "Alice"
    assert task_store[0]["title"] == "Call task for Alice"

# -------------------- Week 3 Day 4: Test view_tasks_by_assignee --------------------
def test_view_tasks_by_assignee():
    task_store.clear()

    parsed = {
        "assignee": "Bob",
        "employee_id": "EMP002",
        "action": "email",
        "deadline": "2025-06-02T10:00"
    }
    schedule = create_schedule_entry(parsed)
    save_schedule(schedule)

    # Function doesn't return anything, so we just make sure it runs
    view_tasks_by_assignee("Bob")

# -------------------- Week 3 Day 5: Test delete_task_by_id --------------------
def test_delete_task_by_id():
    task_store.clear()

    parsed = {
        "assignee": "Carol",
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
        "assignee": "Alice",
        "employee_id": "EMP001",
        "action": "submit",
        "deadline": "2025-06-02T10:00",
        "priority": "High"
    }

    parsed_low = {
        "assignee": "Bob",
        "employee_id": "EMP002",
        "action": "review",
        "deadline": "2025-06-01T10:00",
        "priority": "Low"
    }

    schedule_high = create_schedule_entry(parsed_high)
    schedule_low = create_schedule_entry(parsed_low)

    save_schedule(schedule_high)
    save_schedule(schedule_low)

    prioritize_tasks()  # Output is printed, so no assert here
