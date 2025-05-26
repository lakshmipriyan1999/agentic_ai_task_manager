from scheduler import create_schedule_entry

def test_create_schedule_entry_valid():
    parsed = {
        "assignee": "Alice",
        "employee_id": "EMP001",
        "action": "call",
        "deadline": "2025-06-01T17:00",
        "task_id": "TASK-ALICE-001"
    }
    schedule = create_schedule_entry(parsed)
    assert schedule["title"] == "Call task for Alice"
    assert schedule["assigned_to"] == "Alice"
    assert schedule["deadline"] == "2025-06-01T17:00"
