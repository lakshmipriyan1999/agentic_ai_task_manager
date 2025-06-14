# -------------------- task_store.py --------------------
from datetime import datetime

# Task list with one task
task_store = []

# Add a task with today's deadline
task_store.append({
    "task_id": "TASK-PRIYAN-005",
    "assignee": "Priyan",
    "action": "submit report",
    "deadline": (datetime.now().date()).isoformat(),  # deadline = today
    "employee_id": "EMP-PRIYAN"
})
