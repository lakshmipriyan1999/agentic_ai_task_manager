import spacy
import dateparser
import re
from typing import Optional, Dict
from datetime import datetime, timedelta

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Team members
TEAM = ['Priyan', 'Henali', 'Anusri']

# -------------------- Week 2 Day 4: Fixed Employee ID Mapping --------------------
EMP_IDS = {
    "Priyan": "EMP001",
    "Henali": "EMP002",
    "Anusri": "EMP003"
}

# -------------------- Week 2 Day 4: Global Task ID tracker per team member --------------------
task_id_counters = {}

# -------------------- Week 2 Day 4: Generate Unique Task ID per Assignee --------------------
def generate_task_id(assignee: Optional[str]) -> Optional[str]:
    """
    Generates a unique task ID for each assignee like TASK-BOB-001.
    If assignee is None, returns None.
    """
    if not assignee:
        return None
    name = assignee.upper()
    if name not in task_id_counters:    
        task_id_counters[name] = 1
    else:
        task_id_counters[name] += 1
    return f"TASK-{name}-{task_id_counters[name]:03d}"

# -------------------- Day 1: Deadline Parsing --------------------
def parse_deadline(text: str) -> Optional[str]:
    """
    Extracts a DATE from text using spaCy and dateparser.
    If dateparser fails, handles specific patterns like 'next Monday' manually.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            parsed_date = dateparser.parse(
                ent.text,   
                settings={
                    'PREFER_DATES_FROM': 'future',
                    'RELATIVE_BASE': datetime.now()
                }
            )
            if parsed_date:
                return parsed_date.isoformat()

            # Handle pattern like "next Monday"
            match = re.search(r'next (\w+)', ent.text.lower())
            if match:
                weekday_str = match.group(1)
                try:
                    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                    today = datetime.now()
                    today_weekday = today.weekday()
                    target_weekday = weekdays.index(weekday_str.lower())

                    days_ahead = (target_weekday - today_weekday + 7) % 7
                    days_ahead = days_ahead + 7 if days_ahead == 0 else days_ahead  # ensure it's next week
                    next_day = today + timedelta(days=days_ahead)
                    return next_day.isoformat()
                except ValueError:
                    pass
    return None
    
# -------------------- Day 2: Action Extraction --------------------
def parse_action(text: str) -> str: 
    """
    Extracts the main verb from the sentence.
    If no verb is found, checks for known action keywords.
    """
    doc = nlp(text)
    for token in doc:
        if token.pos_ == "VERB" and token.lemma_.lower() not in ["be", "verb", "have"]:
            return token.lemma_.lower()

    # Fallback keywords
    keywords = ["email", "call", "remind", "schedule", "send", "finish", "prepare"]
    for word in text.lower().split():
        if word in keywords:
            return word
    return ""

# -------------------- Day 3: Assignee Extraction --------------------
def parse_assignee(text: str, team: list = TEAM) -> Optional[str]:
    """
    Extracts a PERSON name from text that matches the team list.
    Falls back to manual matching if NER fails.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text in team:
            return ent.text

    # Fallback if spaCy misses it
    for name in team:
        if name in text:
            return name
    return None

# -------------------- Combined Parser --------------------
def parse_input(text: str) -> Dict:
    """
    Returns a dictionary with deadline, action, assignee, task ID and employee ID.
    Only generates IDs if assignee is recognized.
    """
    assignee = parse_assignee(text)
    employee_id = EMP_IDS.get(assignee) if assignee else None
    task_id = generate_task_id(assignee) if assignee else None

    return {
        'employee_id': employee_id,
        'task_id': task_id,
        'assignee': assignee,
        'action': parse_action(text),
        'deadline': parse_deadline(text)
    }

# -------------------- Sample Run --------------------
if __name__ == "__main__":
    sample = "Email Priyan the report by Friday"
    result = parse_input(sample)
    print("Parsed Result:", result)
