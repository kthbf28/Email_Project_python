from send_mail import send_plain
import logging

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

result = send_plain(
    "your_mailtrap_inbox_email@example.com",
    "Test Email",
    "This is a test message"
)

print("Email sent:", result)