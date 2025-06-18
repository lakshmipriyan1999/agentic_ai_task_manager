from typing import Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil.parser import parse
from datetime import datetime, timedelta, timezone

# -------------------- Setup --------------------
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = 'priyanmunirajan@gmail.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

# -------------------- Get Busy Times --------------------
def get_busy_times():
    now = datetime.now(timezone.utc).isoformat()
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

    events_result = service.freebusy().query(
        body={
            "timeMin": now,
            "timeMax": tomorrow,
            "timeZone": "Asia/Kolkata",
            "items": [{"id": calendar_id}]
        }
    ).execute()

    busy_slots = events_result['calendars'][calendar_id]['busy']
    print("[INFO] Busy slots in the next 24 hours:")
    for b in busy_slots:
        print(b)
    return busy_slots

# -------------------- Check Conflicts --------------------
def is_conflict(start: str, end: str, busy_times: list) -> bool:
    start_dt = parse(start)
    end_dt = parse(end)

    for slot in busy_times:
        busy_start = parse(slot["start"])
        busy_end = parse(slot["end"])
        if start_dt < busy_end and end_dt > busy_start:
            return True
    return False

# -------------------- Find Free Slot --------------------
def find_next_available_slot(busy_times: list, task_duration_minutes: int, preferred_start: str) -> str:
    # Ensure preferred_start is timezone-aware
    search_time = parse(preferred_start)
    if search_time.tzinfo is None:
        search_time = search_time.replace(tzinfo=timezone.utc)

    sorted_busy = sorted(busy_times, key=lambda x: x["start"])

    for i in range(len(sorted_busy)):
        busy_start = parse(sorted_busy[i]["start"])
        if busy_start.tzinfo is None:
            busy_start = busy_start.replace(tzinfo=timezone.utc)

        if search_time < busy_start:
            gap_minutes = (busy_start - search_time).total_seconds() / 60
            if gap_minutes >= task_duration_minutes:
                return search_time.isoformat()

        search_time = max(search_time, parse(sorted_busy[i]["end"]).astimezone(search_time.tzinfo))

    return search_time.isoformat()


# -------------------- Create Calendar Event --------------------
def create_event(assignee: str, action: str, slot: Dict) -> Dict:
    """
    Create a calendar event for the given assignee and slot.
    """
    summary = f"{action.capitalize()} - {assignee}"
    start_time = slot["start"]
    end_time = slot["end"]

    event_body = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }

    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()

    print(f"[INFO] Created event for {assignee}: {summary} ({start_time} → {end_time})")
    return {"start": start_time, "end": end_time, "id": event["id"]}
