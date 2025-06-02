from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil.parser import parse  # ✅ For converting string time to datetime
import datetime

# -------------------- Setup --------------------

# Path to your credentials file
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Authenticate with Google
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Connect to Google Calendar API
service = build('calendar', 'v3', credentials=credentials)

# Use primary calendar
calendar_id = 'primary'

# Set time range: now to 24 hours later
now = datetime.datetime.utcnow().isoformat() + 'Z'
tomorrow = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'

# -------------------- Fetch Busy Slots --------------------

events_result = service.freebusy().query(
    body={
        "timeMin": now,
        "timeMax": tomorrow,
        "timeZone": "Asia/Kolkata",
        "items": [{"id": calendar_id}]
    }
).execute()

# Extract busy slots
busy_times = events_result['calendars'][calendar_id]['busy']

# Show busy times
print("[INFO] Busy slots in the next 24 hours:")
for time_range in busy_times:
    print(f"- From: {time_range['start']} To: {time_range['end']}")

# -------------------- Week 4 Day 2: Conflict Checking --------------------

# Sample task to check (can be dynamic later)
task_start = '2025-06-02T09:30:00+05:30'
task_end = '2025-06-02T10:30:00+05:30'

def is_conflict(task_start, task_end, busy_slots):
    task_start_dt = parse(task_start)
    task_end_dt = parse(task_end)

    for slot in busy_slots:
        busy_start = parse(slot['start'])
        busy_end = parse(slot['end'])

        if (task_start_dt < busy_end and task_end_dt > busy_start):
            return True  # Overlaps
    return False  # No overlap

# -------------------- Week 4 Day 3: Suggest Next Available Slot --------------------

def find_next_available_slot(busy_slots, task_duration_minutes, search_start):
    search_time = parse(search_start)
    sorted_busy = sorted(busy_slots, key=lambda x: parse(x['start']))

    for i in range(len(sorted_busy)):
        current_start = parse(sorted_busy[i]['start'])

        # Check if there's a free gap long enough
        gap_minutes = (current_start - search_time).total_seconds() / 60

        if gap_minutes >= task_duration_minutes:
            return search_time.isoformat()

        # Move search_time forward to the end of current busy slot
        search_time = max(search_time, parse(sorted_busy[i]['end']))

    # If nothing fits in between, suggest time after last busy slot
    return search_time.isoformat()

# -------------------- Conflict Check with Reschedule Suggestion --------------------

if is_conflict(task_start, task_end, busy_times):
    print("[WARNING] Task time conflicts with a busy slot.")

    # Calculate task duration
    start_dt = parse(task_start)
    end_dt = parse(task_end)
    duration_minutes = int((end_dt - start_dt).total_seconds() / 60)

    # Find next available slot
    next_slot = find_next_available_slot(busy_times, duration_minutes, task_start)
    print(f"[SUGGESTION] Reschedule task to start at: {next_slot}")
else:
    print("[OK] Task time is free. You can schedule it.")
