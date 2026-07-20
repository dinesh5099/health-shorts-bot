import smtplib
from email.mime.text import MIMEText
import os

def send_email(subject, body):
    sender = os.environ.get("ALERT_EMAIL_FROM")
    password = os.environ.get("ALERT_EMAIL_PASSWORD")
    recipient = os.environ.get("ALERT_EMAIL_TO")
    
    if not all([sender, password, recipient]):
        print("Email credentials not configured, skipping alert.")
        return
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
