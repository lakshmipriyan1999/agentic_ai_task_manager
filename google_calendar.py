from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil.parser import parse
from datetime import datetime, timedelta, timezone

# -------------------- Setup --------------------
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)
calendar_id = 'primary'

# -------------------- Week 4 Day 1: Get Busy Times from Google Calendar --------------------
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

# -------------------- Week 4 Day 2: Detect Conflict with Busy Slots --------------------
def is_conflict(start: str, end: str, busy_times: list) -> bool:
    start_dt = parse(start)
    end_dt = parse(end)

    for slot in busy_times:
        busy_start = parse(slot["start"])
        busy_end = parse(slot["end"])
        if start_dt < busy_end and end_dt > busy_start:
            return True
    return False

# -------------------- Week 4 Day 3: Suggest Next Available Free Slot --------------------
def find_next_available_slot(busy_times: list, task_duration_minutes: int, preferred_start: str) -> str:
    search_time = parse(preferred_start)
    sorted_busy = sorted(busy_times, key=lambda x: x["start"])

    for i in range(len(sorted_busy)):
        if search_time < parse(sorted_busy[i]["start"]):
            gap_minutes = (parse(sorted_busy[i]["start"]) - search_time).total_seconds() / 60
            if gap_minutes >= task_duration_minutes:
                return search_time.isoformat()
        search_time = max(search_time, parse(sorted_busy[i]["end"]))

    return search_time.isoformat()

# -------------------- Week 4 Day 5: Manual Testing (Optional) --------------------
if __name__ == "__main__":
    busy_slots = get_busy_times()
    print("\n[TEST] Fetched busy slots:")
    for slot in busy_slots:
        print(slot)
