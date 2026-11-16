import csv
import time
import os
from send_mail import send_html
from dotenv import load_dotenv

load_dotenv()

RATE_PER_MIN = int(os.getenv("RATE_PER_MIN", 30))


def load_template():
    with open("pythonemails/templates/email.html") as f:
        return f.read()


def personalize(template, row):
    return template.replace("{{name}}", row["name"])


def send_bulk():
    template = load_template()
    delay = 60 / RATE_PER_MIN

    with open("pythonemails/recipients.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            html = personalize(template, row)

            success = send_html(
                to_email=row["email"],
                subject="Hello from Python Mailer",
                html_body=html,
                attachments=[],
                inline_images={"logo": "pythonemails/files/GIthub.jpg"}
            )

            print(f"Sent to {row['email']} -> {success}")
            time.sleep(delay)


if __name__ == "__main__":
    send_bulk()