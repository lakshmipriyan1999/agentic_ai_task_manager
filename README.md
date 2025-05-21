# Agentic AI Task Manager

## Project Overview
The Agentic AI Task Manager is an automated system that:
1. Parses natural-language task requests (action, deadline, assignee, priority).  
2. Prioritizes tasks based on urgency and due date.  
3. Schedules tasks on a Google Calendar, finding free slots before their deadlines.  
4. Sends notifications and reminders via email or Slack.  
5. Supports dynamic re-planning (cancel, reschedule) and logs every step.

This tool demonstrates the end-to-end construction of an “agentic” assistant that can manage, schedule, and notify about tasks.

## Tech Stack
- **Python 3.9+**  
- **NLP**: spaCy (with optional fall-back stub), dateparser  
- **Calendar Integration**: Google Calendar API (`google-api-python-client`)  
- **Notifications**: SMTP (`smtplib`) & Slack SDK (`slack-sdk`)  
- **Config & Secrets**: `python-dotenv` (.env)  
- **Testing**: pytest  
- **Version Control**: Git

## Getting Started
1. Clone the repo and enter its folder:
   ```bash
   git clone <repo-url>
   cd agentic_ai_task_manager
