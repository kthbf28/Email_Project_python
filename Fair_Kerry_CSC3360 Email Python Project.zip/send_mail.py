import os
import ssl
import smtplib
import logging
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM = os.getenv("FROM")

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Create logger
logger = logging.getLogger("email_logger")
logger.setLevel(logging.INFO)

# Remove old handlers (important!)
if logger.hasHandlers():
    logger.handlers.clear()

# Create file handler
file_handler = logging.FileHandler("logs/app.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add handler
logger.addHandler(file_handler)

logger.info("=== PROGRAM STARTED ===")

# Helper: Connect to SMTP
def _connect():
    logger.info("Attempting SMTP connection")
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        logger.info("SMTP connection established with STARTTLS")
        return server
    except Exception as e:
        logger.error(f"SMTP connection failed: {e}")
        raise

# Part A: Plain text email
def send_plain(to_email: str, subject: str, body: str) -> bool:
    logger.info(f"send_plain() called for {to_email}")
    
    try:
        server = _connect()
        msg = EmailMessage()
        msg["From"] = FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        server.send_message(msg)
        server.quit()

        logger.info(f"Plain email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send plain email to {to_email}: {e}")
        return False

# Part B: HTML email with attachments & inline images
def send_html(
    to_email: str,
    subject: str,
    html_body: str,
    attachments: list[str] | None = None,
    inline_images: dict[str,str] | None = None,
    cc: list[str] | None = None,
    bcc: list[str] | None = None
) -> bool:
    logger.info(f"send_html() called for {to_email}")

    """
    Send an HTML email with optional attachments and inline images.

    inline_images: dictionary of cid -> file path
    """
    try:
        server = _connect()

        msg = EmailMessage()
        msg["From"] = FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()
        if cc:
            msg["Cc"] = ", ".join(cc)

        # Plain text alternative
        msg.set_content("This is the plain-text fallback for email clients.")

        # HTML content
        if inline_images:
            # Create multipart/related
            msg.add_alternative(html_body, subtype='html')
            for cid, path in inline_images.items():
                with open(path, "rb") as img:
                    maintype, subtype = "image", os.path.splitext(path)[1][1:]
                    msg.get_payload()[-1].add_related(
                        img.read(),
                        maintype=maintype,
                        subtype=subtype,
                        cid=cid
                    )
        else:
            msg.add_alternative(html_body, subtype='html')

        # Attachments
        if attachments:
            for filepath in attachments:
                if not os.path.isfile(filepath):
                    logger.warning(f"Attachment not found: {filepath}")
                    continue
                with open(filepath, "rb") as f:
                    data = f.read()
                    filename = os.path.basename(filepath)
                    msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=filename)

        # Prepare recipients
        all_recipients = [to_email]
        if cc:
            all_recipients += cc
        if bcc:
            all_recipients += bcc

        # Send
        server.send_message(msg, from_addr=FROM, to_addrs=all_recipients)
        server.quit()
        logger.info(f"HTML email sent to {to_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send HTML email to {to_email}: {e}")
        return False