from typing import Dict, Optional
from datetime import datetime, timedelta

# -------------------- Week 3 Day 3: Global Task ID Counter --------------------
task_id_counters = {}

# -------------------- Week 3 Day 2: Global Task Store --------------------
task_store = []

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


# -------------------- Week 3 Day 4: Create Schedule Entry --------------------
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


# -------------------- Week 3 Day 2: Save Schedule Function --------------------
def save_schedule(schedule: Dict[str, str]) -> None:
    if schedule:
        task_store.append(schedule)
        print(f"[SUCCESS] Task saved successfully: {schedule['task_id']}")
    else:
        print("[WARNING] Empty or invalid schedule. Not saved.")


# -------------------- Week 3 Day 2: View All Schedules --------------------
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


# -------------------- Test the Full Flow --------------------
if __name__ == "__main__":
    from input_parser import parse_input

    text1 = "Call Alice tomorrow"
    text2 = "Email Alice the file by Friday"

    parsed1 = parse_input(text1)
    parsed1["priority"] = "High"

    parsed2 = parse_input(text2)
    parsed2["priority"] = "Low"

    schedule1 = create_schedule_entry(parsed1)
    schedule2 = create_schedule_entry(parsed2)

    save_schedule(schedule1)
    save_schedule(schedule2)

    view_schedules()
    view_tasks_by_assignee("Alice")
    prioritize_tasks()
    delete_task_by_id(schedule1["task_id"])
    view_schedules()
