from datetime import datetime, timedelta
from notifier import send_email
import json

# ------------------ Email Directory ------------------
EMAILS = {
    "Priyan": "lakshmipriyan6666@gmail.com",
    "Henali": "lakshmipriyan6666@gmail.com",
    "Anusri": "lakshmipriyan6666@gmail.com"
}

# ------------------ Load Task Store ------------------
try:
    with open("tasks.json", "r") as f:
        task_store = json.load(f)
except FileNotFoundError:
    print("[ERROR] tasks.json not found.")
    task_store = []

# ------------------ Deadline Reminder ------------------
print("\n[INFO] Checking for upcoming task deadlines...")

today = datetime.now().date()
tomorrow = today + timedelta(days=1)

for task in task_store:
    try:
        deadline_date = datetime.fromisoformat(task["deadline"]).date()
    except Exception as e:
        print(f"[ERROR] Failed to parse deadline: {task.get('deadline')} — {e}")
        continue

    if deadline_date == today or deadline_date == tomorrow:
        assignee = task.get("assigned_to")
        to_email = EMAILS.get(assignee)

        if not to_email:
            print(f"[WARNING] No email found for {assignee}")
            continue

        subject = f"[Reminder] Task '{task['title']}' is due on {deadline_date}"
        message = f"""
Hi {assignee},

This is a reminder that your task is due soon.

Task: {task.get('full_task', 'No description')}
Deadline: {task['deadline']}
Task ID: {task['task_id']}

Please complete it before the deadline.

Thanks,
Agentic AI Task Scheduler
"""

        send_email(to_email, subject, message.strip())
        print(f"[INFO] Reminder sent to {assignee}")
