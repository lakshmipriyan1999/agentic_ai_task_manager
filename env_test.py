# env_test.py
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env
creds_path = os.getenv("GOOGLE_CREDENTIALS")
print("GOOGLE_CREDENTIALS points to:", creds_path)
