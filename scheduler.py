from typing import Dict, Optional

def create_schedule_entry(parsed: Dict[str, Optional[str]]) -> Optional[Dict[str, str]]:
    """
    Takes parsed task input and converts it into a structured schedule dictionary.
    Returns None if required fields are missing.
    """
    if not parsed.get("assignee") or not parsed.get("deadline") or not parsed.get("action"):
        return None  # Cannot create a schedule without key info

    return {
        "title": f"{parsed['action'].capitalize()} task for {parsed['assignee']}",
        "assigned_to": parsed["assignee"],
        "employee_id": parsed["employee_id"],
        "deadline": parsed["deadline"],
        "task_id": parsed["task_id"]
    }



if __name__ == "__main__":
    from input_parser import parse_input  # Import from your Week 2 work

    text = "Email Bob the report by Friday"
    parsed = parse_input(text)
    schedule = create_schedule_entry(parsed)

    print("Scheduled Entry:", schedule)
