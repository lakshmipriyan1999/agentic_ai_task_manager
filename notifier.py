import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    # Your original Gmail and app password
    from_email = "priyanmunirajan@gmail.com"
    password = "fxhoubkjnzywpbcb"  # App password (no spaces)

    # Create the email content
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()                      # Start TLS encryption
        server.login(from_email, password)     # Login using app password
        server.sendmail(from_email, to_email, msg.as_string())  # Send the email
        server.quit()

        print(f"[INFO] Email sent to {to_email}")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

# -------------------- Test Email Trigger --------------------
if __name__ == "__main__":
    send_email(
        to_email="lakshmipriyan6666@gmail.com",  # ✅ Your second email
        subject="Test Email from TaskBot",
        message="Hello Priyan,\n\nThis is a test email from your Python TaskBot project!"
    )
