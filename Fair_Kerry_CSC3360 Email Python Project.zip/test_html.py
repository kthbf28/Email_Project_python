from send_mail import send_html
import logging

html_content = """
<h1>Hello!</h1>
<p>This is a test HTML email with inline image.</p>
<img src="cid:pythonemails/files/GitHub.jpg">
"""

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

result = send_html(
    to_email="your_mailtrap_inbox_email@example.com",
    subject="HTML Email Test",
    html_body=html_content,
    attachments=["pythonemails/files/GitHub.jpg"],
    inline_images={"logo_image":"pythonemails/files/GitHub.jpg"},
    cc=["cc_email@example.com"],
    bcc=["bcc_email@example.com"]
)

print("HTML email sent:", result)