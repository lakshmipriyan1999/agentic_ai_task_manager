from notify_on_assignment import notify_task

def test_notify_task_runs_without_error():
    try:
        notify_task("Email Henali the slides by next Monday")
        assert True
    except Exception as e:
        assert False, f"notify_task() failed: {e}"
