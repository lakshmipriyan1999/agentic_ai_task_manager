from scheduler import task_store, replan_tasks
import json

# Load tasks.json 
try:
    with open("tasks.json", "r") as f:
        loaded_tasks = json.load(f)
        task_store.clear()
        task_store.extend(loaded_tasks)
        print("[INFO] Loaded tasks from tasks.json")
except FileNotFoundError:
    print("[ERROR] tasks.json not found.")
    exit()

# Run re-planning 
print("\n[REPLAN TASKS TEST]")
replan_tasks()
