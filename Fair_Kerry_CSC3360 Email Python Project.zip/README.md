# Python Email Sender Project

## SMTP Option Used

This project uses **Sandbox SMTP with STARTTLS authentication**.

- Does not send real mail
- Uses port 587 with TLS encryption

## Setup

1. Install dependencies:
   pip install python-dotenv

2. Copy .env.example → .env and fill in values.

## SMTP Options
- Recommended: Institutional SMTP
- Alternative: Mailtrap sandbox
- Local debug: python -m smtpd -c DebuggingServer -n localhost:1025

## Run

### Single Email
Use send_plain() or send_html() from send_mail.py

### Bulk Email
python bulk_mail.py

## Features
- STARTTLS secure connection
- HTML + plain-text fallback
- Attachments
- Inline images (CID)
- Rate limiting
- Logging

## Logs
Check logs/app.log for:
- Success messages
- Errors (at least one failure included)