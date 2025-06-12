from notifier import send_email

def test_send_email_success():
    """
    Test if the email function runs without error.
    This will send a real email to your second email.
    """
    try:
        send_email(
            to_email="lakshmipriyan6666@gmail.com",
            subject="Test Email (from test_notifier)",
            message="This is a test email from Week 5 Day 1 test file."
        )
        assert True  # Email sent successfully
    except Exception as e:
        assert False, f"Email sending failed: {e}"
