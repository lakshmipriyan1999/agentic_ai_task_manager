from deadline_reminder import send_deadline_reminders

def test_send_reminder():
    try:
        send_deadline_reminders()
        print("[TEST PASSED] Reminder function ran without errors.")
        assert True
    except Exception as e:
        print(f"[TEST FAILED] Error: {e}")
        assert False, f"Reminder failed: {e}"
