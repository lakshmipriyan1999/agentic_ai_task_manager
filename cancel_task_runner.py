import json
from scheduler import cancel_task, task_store

# Load tasks.json into task_store 
try:
    with open("tasks.json", "r") as f:
        loaded_tasks = json.load(f)
        task_store.extend(loaded_tasks)  # Load tasks into memory
        print("[INFO] Loaded tasks from tasks.json")
except FileNotFoundError:
    print("[ERROR] tasks.json not found. Run scheduler.py first.")

# Run cancellation 
print("\n[CANCEL TASK TEST]")
cancel_task("TASK-PRIYAN-002")
