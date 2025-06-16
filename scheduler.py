from typing import Dict, Optional
from datetime import datetime, timedelta
from dateutil.parser import parse
from google_calendar import get_busy_times, is_conflict, find_next_available_slot
from google.oauth2 import service_account
from googleapiclient.discovery import build
from notifier import send_email
from input_parser import parse_input
from task_store import task_store  # ✅ shared task list


# -------------------- Google Calendar Setup --------------------
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)
calendar_id = 'priyanmunirajan@gmail.com'

# -------------------- Calendar Event Creation --------------------
def add_event_to_calendar(summary: str, start_time: str, end_time: str):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'}
    }
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"[INFO] Calendar event created: {created_event['htmlLink']}")

# -------------------- Global Stores --------------------
task_store = []
task_id_counters = {}

# -------------------- ID Generation --------------------
def generate_task_id(assignee: Optional[str]) -> Optional[str]:
    if not assignee:
        return None
    name = assignee.upper()
    task_id_counters[name] = task_id_counters.get(name, 0) + 1
    return f"TASK-{name}-{task_id_counters[name]:03d}"

# -------------------- Create Schedule --------------------
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
        "task_id": generate_task_id(parsed.get("assignee")),
        "full_task": parsed.get("full_task", "")
    }

# -------------------- Save with Conflict Detection --------------------
def save_schedule(schedule: Dict[str, str]) -> None:
    if not schedule or "assigned_to" not in schedule:
        print("[WARNING] Invalid schedule. Missing required fields.")
        return

    deadline = schedule.get("deadline")
    start_dt = parse(deadline).astimezone()
    end_dt = (start_dt + timedelta(minutes=30)).astimezone()
    busy_times = get_busy_times()

    print("[INFO] Busy slots in the next 24 hours:")
    for slot in busy_times:
        print(slot)

    if is_conflict(start_dt.isoformat(), end_dt.isoformat(), busy_times):
        print(f"[WARNING] Conflict detected for {schedule['assigned_to']}. Finding next available slot...")
        duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
        start_dt = parse(find_next_available_slot(busy_times, duration_minutes, start_dt.isoformat())).astimezone()
        end_dt = (start_dt + timedelta(minutes=30)).astimezone()

    # Send assignment email
    try:
        to_email = "lakshmipriyan6666@gmail.com"  # demo for all
        message = f"Task: {schedule['full_task']}\nDeadline: {start_dt.isoformat()}\nTask ID: {schedule['task_id']}"
        send_email(to_email, f"[Task Assigned] {schedule['title']}", message)
        print(f"[INFO] Email sent to {to_email}")
        print(f"[INFO] Assignment email sent to {schedule['assigned_to']}")
    except Exception as e:
        print(f"[ERROR] Failed to send assignment email: {e}")

    # Save task and add event
    task_store.append(schedule)
    add_event_to_calendar(schedule["title"], start_dt.isoformat(), end_dt.isoformat())
    print(f"[DEBUG] Saved to calendar: {schedule['title']} at {start_dt.isoformat()}")
    print(f"[SUCCESS] Task saved successfully: {schedule['task_id']}")

    import json

    # Save task store to JSON
    with open("tasks.json", "w") as f:
        json.dump(task_store, f, indent=2, default=str)


# -------------------- View Tasks --------------------
def view_tasks_by_assignee(name: str) -> None:
    print(f"\n[TASKS FOR {name.upper()}]")
    found = False
    for task in task_store:
        if task.get("assigned_to", "").lower() == name.lower():
            print(task)
            found = True
    if not found:
        print("No tasks found for this assignee.")

def prioritize_tasks() -> None:
    def get_priority_score(priority: str) -> int:
        scores = {"High": 3, "Medium": 2, "Low": 1}
        return scores.get(priority, 2)

    print("\n[PRIORITIZED TASK LIST]")
    sorted_tasks = sorted(task_store, key=lambda x: (-get_priority_score(x.get("priority", "Medium")), x["deadline"]))
    for task in sorted_tasks:
        print(task)

# -------------------- Run Script --------------------
if __name__ == "__main__":
    mock_inputs = [
        ("Anusri should schedule the feedback meeting by  tomorrow 3 PM", "Low"),
        ("Henali should prepare the client presentation by next Monday", "Medium"),
        ("Priyan should submit the weekly status report by today", "High")
    ]

    for text, priority in mock_inputs:
        parsed = parse_input(text)
        parsed["priority"] = priority
        parsed["full_task"] = text
        schedule = create_schedule_entry(parsed)
        save_schedule(schedule)

    print("\n View schedules for each team member:")
    view_tasks_by_assignee("Priyan")
    view_tasks_by_assignee("Henali")
    view_tasks_by_assignee("Anusri")

    prioritize_tasks()

    # Overlapping test
    print("\n[TEST] Adding an overlapping task for Priyan at 3 PM (should conflict):")
    test_input = "Prepare report with Priyan at 3 PM tomorrow"
    test_priority = "High"
    parsed = parse_input(test_input)
    parsed["priority"] = test_priority
    parsed["full_task"] = test_input
    schedule = create_schedule_entry(parsed)
    save_schedule(schedule)
