from dateutil.parser import parse

# Copy your is_conflict function here if it's not imported from another file
def is_conflict(task_start, task_end, busy_slots):
    task_start_dt = parse(task_start)
    task_end_dt = parse(task_end)

    for slot in busy_slots:
        busy_start = parse(slot['start'])
        busy_end = parse(slot['end'])

        if (task_start_dt < busy_end and task_end_dt > busy_start):
            return True
    return False

# ------------------ Test Cases ------------------

def test_conflict_found():
    task_start = "2025-06-02T09:30:00+05:30"
    task_end = "2025-06-02T10:30:00+05:30"
    busy_slots = [
        {"start": "2025-06-02T09:00:00+05:30", "end": "2025-06-02T10:00:00+05:30"}
    ]
    assert is_conflict(task_start, task_end, busy_slots) == True

def test_no_conflict():
    task_start = "2025-06-02T11:30:00+05:30"
    task_end = "2025-06-02T12:30:00+05:30"
    busy_slots = [
        {"start": "2025-06-02T09:00:00+05:30", "end": "2025-06-02T10:00:00+05:30"}
    ]
    assert is_conflict(task_start, task_end, busy_slots) == False
