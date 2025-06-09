from input_parser import parse_input
from scheduler import create_schedule_entry, save_schedule, view_tasks_by_assignee, task_store

# -------------------- Week 4 Day 5: End-to-End Scheduling Flow --------------------
def test_full_schedule_flow():
    task_store.clear()  # Reset task list before test

    mock_inputs = [
        ("Call Alice tomorrow at 3 PM", "High"),
        ("Email Bob the file by Friday 2 PM", "Medium"),
        ("Schedule meeting with Carol at 10 AM tomorrow", "Low")
    ]

    for text, priority in mock_inputs:
        parsed = parse_input(text)          # Step 1: Extract task info
        parsed["priority"] = priority       # Step 2: Assign priority manually
        schedule = create_schedule_entry(parsed)  # Step 3: Build task dict
        save_schedule(schedule)             # Step 4: Save with conflict check

    assert len(task_store) == 3  # Ensure 3 tasks are saved

    # Optional display check (no assert needed, just verify prints)
    view_tasks_by_assignee("Alice")
    view_tasks_by_assignee("Bob")
    view_tasks_by_assignee("Carol")
