import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from core.config import settings

def generate_otp(length=6):
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


def send_email(to_email: str, subject: str, otp: str):

    smtp_server = settings.EMAIL_HOST
    smtp_port = 587
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email

    html_content = f"""
    <html>
      <body>
        <p>Greetings,</p>
        <p>Your OTP code for email verification is: <strong>{otp}</strong></p>
        <p>This code is valid for 10 minutes.</p>
        <p>If you did not request this, please ignore this email.</p>
      </body>
    </html>"""

    mime_text = MIMEText(html_content, "html")
    message.attach(mime_text)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

