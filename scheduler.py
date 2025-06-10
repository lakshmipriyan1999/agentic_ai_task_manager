from typing import Dict, Optional
from datetime import datetime, timedelta
from dateutil.parser import parse

# -------------------- Week 4 Day 4: Google Calendar Conflict Detection --------------------
from google_calendar import get_busy_times, is_conflict, find_next_available_slot

# -------------------- Week 3 Day 1: Global Task Store --------------------
task_store = []

# -------------------- Week 3 Day 3: Global Task ID Counter --------------------
task_id_counters = {}

# -------------------- Week 3 Day 3: Generate Unique Task ID --------------------
def generate_task_id(assignee: Optional[str]) -> Optional[str]:
    if not assignee:
        return None

    name = assignee.upper()
    if name not in task_id_counters:
        task_id_counters[name] = 1
    else:
        task_id_counters[name] += 1

    return f"TASK-{name}-{task_id_counters[name]:03d}"

# -------------------- Week 3 Day 2: Create Schedule Entry --------------------
def create_schedule_entry(parsed: Dict[str, Optional[str]]) -> Optional[Dict[str, str]]:
    if not parsed.get("assignee") or not parsed.get("deadline") or not parsed.get("action"):
        return None

    print(f"[INFO] Creating task for {parsed['assignee']}")

    return {
        "title": f"{parsed['action'].capitalize()} task for {parsed['assignee']}",
        "assigned_to": parsed["assignee"],
        "employee_id": parsed["employee_id"],
        "deadline": parsed["deadline"],
        "priority": parsed.get("priority", "Medium"),
        "task_id": generate_task_id(parsed.get("assignee"))
    }

# -------------------- Week 3 Day 2 (Enhanced in Week 4 Day 4): Save Schedule with Conflict Detection --------------------

def save_schedule(schedule: Dict[str, str]) -> None:
    if not schedule:
        print("[WARNING] Empty or invalid schedule. Not saved.")
        return

    deadline = schedule.get("deadline")
    start_dt = parse(deadline)
    end_dt = start_dt + timedelta(minutes=30)  # Each task assumed to take 30 minutes

    busy_times = get_busy_times()

    if is_conflict(start_dt.isoformat(), end_dt.isoformat(), busy_times):
        print("[WARNING] Task time conflicts with a busy slot.")

        duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
        next_slot = find_next_available_slot(busy_times, duration_minutes, start_dt.isoformat())
        print(f"[SUGGESTION] Consider rescheduling to start at: {next_slot}")
    else:
        task_store.append(schedule)
        print(f"[SUCCESS] Task saved successfully: {schedule['task_id']}")

# -------------------- Week 3 Day 1: View All Schedules --------------------
def view_schedules() -> None:
    print("\n[ALL SAVED TASKS]")
    for task in task_store:
        print(task)

# -------------------- Week 3 Day 4: View Tasks by Assignee --------------------
def view_tasks_by_assignee(name: str) -> None:
    print(f"\n[TASKS FOR {name.upper()}]")
    found = False
    for task in task_store:
        if task["assigned_to"].lower() == name.lower():
            print(task)
            found = True
    if not found:
        print("No tasks found for this assignee.")

# -------------------- Week 3 Day 5: Delete Task by ID --------------------
def delete_task_by_id(task_id: str) -> None:
    for task in task_store:
        if task["task_id"] == task_id:
            task_store.remove(task)
            print(f"[INFO] Task {task_id} deleted successfully.")
            return
    print(f"[WARNING] Task ID {task_id} not found.")

# -------------------- Week 3 Day 5: Prioritize Tasks --------------------
def get_priority_score(priority: str) -> int:
    scores = {"High": 3, "Medium": 2, "Low": 1}
    return scores.get(priority, 2)

def prioritize_tasks() -> None:
    print("\n[PRIORITIZED TASK LIST]")
    sorted_tasks = sorted(
        task_store,
        key=lambda x: (
            -get_priority_score(x.get("priority", "Medium")),
            x["deadline"]
        )
    )
    for task in sorted_tasks:
        print(task)

# -------------------- Week 4 Day 5: Test with Mock Team --------------------
if __name__ == "__main__":
    from input_parser import parse_input

    mock_inputs = [
        ("Call Priyan tomorrow at 3 PM", "High"),
        ("Email Henali the file by Friday 2 PM", "Medium"),
        ("Schedule meeting with Anusri at 10 AM tomorrow", "Low")
    ]

    for text, priority in mock_inputs:
        parsed = parse_input(text)
        parsed["priority"] = priority
        schedule = create_schedule_entry(parsed)
        save_schedule(schedule)

    print("\n View schedules for each team member:")
    view_tasks_by_assignee("Priyan")
    view_tasks_by_assignee("Henali")
    view_tasks_by_assignee("Anusri")

    print("\ Prioritized task list:")
    prioritize_tasks()
