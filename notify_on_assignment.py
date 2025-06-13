from input_parser import parse_input
from notifier import send_email

# All team members' emails go to your inbox for demo
EMAILS = {
    "Priyan": "lakshmipriyan6666@gmail.com",
    "Henali": "lakshmipriyan6666@gmail.com",
    "Anusri": "lakshmipriyan6666@gmail.com"
}

def notify_task(text):
    # Parse the input sentence
    data = parse_input(text)
    assignee = data["assignee"]

    # If no name found, skip
    if not assignee:
        print("[INFO] No assignee found.")
        return

    # Get the email for that person
    to_email = EMAILS.get(assignee)
    if not to_email:
        print(f"[WARNING] No email for {assignee}")
        return

    # Create email subject and message
    subject = f"[Task Assigned] {data['action'].capitalize()} Task"
    message = f"""
Hello {assignee},

You have been assigned a new task.

Task: {data['action'].capitalize()}
Deadline: {data['deadline'] or 'Not specified'}
Task ID: {data['task_id']}

Please complete it as soon as possible.

Thanks,
Agentic AI Task Scheduler
"""

    # Send the email
    send_email(to_email, subject, message.strip())

# --------- Test the function ---------
if __name__ == "__main__":
    notify_task("Email Henali the report by Friday")
