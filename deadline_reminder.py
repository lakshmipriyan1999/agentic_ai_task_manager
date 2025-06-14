# -------------------- deadline_reminder.py --------------------
from datetime import datetime, timedelta
from notifier import send_email                # from Day 1
from task_store import task_store              # this file
from email_ids import EMAILS                   # from Day 2

def send_deadline_reminders():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    for task in task_store:
        assignee = task.get("assignee")
        deadline = task.get("deadline")
        action = task.get("action")
        task_id = task.get("task_id")

        if not assignee or not deadline:
            continue  # skip if missing

        try:
            deadline_date = datetime.fromisoformat(deadline).date()
        except:
            print(f"[ERROR] Can't read deadline: {deadline}")
            continue

        if deadline_date == today or deadline_date == tomorrow:
            to_email = EMAILS.get(assignee)
            if not to_email:
                print(f"[WARNING] No email found for {assignee}")
                continue

            subject = f"[Reminder] Task '{action}' is due on {deadline_date}"
            message = f"""
Hi {assignee},

This is a reminder that your task is due soon.

Task: {action}
Deadline: {deadline_date}
Task ID: {task_id}

Please complete it before the deadline.

Thanks,
Agentic AI Task Scheduler
"""

            send_email(to_email, subject, message.strip())
            print(f"[INFO] Reminder sent to {assignee}")



if __name__ == "__main__":
    send_deadline_reminders()
