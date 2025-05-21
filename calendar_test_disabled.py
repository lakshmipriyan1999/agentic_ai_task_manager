import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Debug: show where the script is running and what files are in that folder
cwd = os.getcwd()
print("CURRENT WORKING DIR:", cwd)
print("FILES HERE:", os.listdir(cwd))

# Load .env
load_dotenv()
creds_path = os.getenv("GOOGLE_CREDENTIALS")
print("GOOGLE_CREDENTIALS from .env:", creds_path)

# Attempt to open the credentials file
full_path = os.path.join(cwd, creds_path)
print("Full path to credentials.json:", full_path)
print("Exists?", os.path.exists(full_path))

# If it exists, proceed
creds = service_account.Credentials.from_service_account_file(
    full_path,
    scopes=["https://www.googleapis.com/auth/calendar.readonly"]
)
service = build("calendar", "v3", credentials=creds)
calendars = service.calendarList().list().execute()
print("Calendars:", [c["summary"] for c in calendars.get("items", [])])
