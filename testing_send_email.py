import os
import re
import json
import time
import smtplib
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ============================================================
# CONFIGURATION
# ============================================================
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
JSON_FILE = r"linkedin_posts_output\2026-09-03\linkedin_posts_2026-09-03_14-12-13.json"

SENDER_EMAIL = "parikhdhruv05@gmail.com"

# Gmail App Password
SENDER_PASSWORD = "lkao mlwv hgle qvfr"

RESUME_PATH = r'C:\Users\Admin\Downloads\Sending-Emails-With-Python-main\Sending-Emails-With-Python-main\Dhruv_Resume.pdf'

DELAY_BETWEEN_EMAILS = 15

EMAIL_SUBJECT = "Application for Python Django Developer"

EMAIL_BODY = """
Hello Hiring Team,

I came across your opening for {position} and would like to apply.

I have 3.0+ years of experience in Python, Django, Django REST Framework,
PostgreSQL, REST APIs, Selenium, OpenCV and Web Application Development.

Please find my resume attached for your review.

Thank you for your time and consideration.

Best Regards,

Dhruv Parikh
+91 7600524348
Ahmedabad, Gujarat
"""

# ============================================================
# LOG FOLDER / FILE SETUP (date wise folder + date-time wise file)
# ============================================================

NOW = datetime.now()

DATE_STR = NOW.strftime("%Y-%m-%d")
DATETIME_STR = NOW.strftime("%Y-%m-%d_%H-%M-%S")

# Separate folder for each date
LOG_FOLDER = os.path.join("email_logs", DATE_STR)
os.makedirs(LOG_FOLDER, exist_ok=True)

# File name includes date + time
SENT_LOG_FILE = os.path.join(LOG_FOLDER, f"sent_emails_log_{DATETIME_STR}.json")
FAILED_LOG_FILE = os.path.join(LOG_FOLDER, f"failed_emails_log_{DATETIME_STR}.json")


# ============================================================
# EMAIL VALIDATION
# ============================================================

# Values jeni emails ne invalid / blank gani ne skip karva chh
INVALID_EMAIL_VALUES = {"", "none", "null", "n/a", "na", "nan"}


def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)


def is_blank_email(email):
    """
    Email '' (empty), None, 'None', 'null', 'NULL' etc hoy to True return kare.
    """
    if email is None:
        return True

    cleaned = str(email).strip().lower()

    return cleaned in INVALID_EMAIL_VALUES


# ============================================================
# LOG FILE FUNCTIONS
# ============================================================

def load_log_list(log_file):
    """
    Log file ma list of records (dict) hoy chh.
    File na hoy ya corrupt hoy to empty list return kare.
    """
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except:
            return []
    return []


def save_log(log_file, records):
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)


def load_today_sent_emails():
    """
    Aaj na DATE_STR folder ma jetla pan sent_emails_log_*.json files
    chhe, badhama thi records vanchine, emails (lowercase) nu
    combined set return kare. Jethi same din ma duplicate email na jaay.
    """
    combined = set()

    if not os.path.exists(LOG_FOLDER):
        return combined

    for file_name in os.listdir(LOG_FOLDER):
        if file_name.startswith("sent_emails_log_") and file_name.endswith(".json"):
            file_path = os.path.join(LOG_FOLDER, file_name)
            records = load_log_list(file_path)

            for rec in records:
                email = rec.get("email")
                if not is_blank_email(email):
                    combined.add(str(email).strip().lower())

    return combined


# ============================================================
# READ JSON FILE
# ============================================================

def get_email_position_pairs(json_file):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    pairs = []

    for item in data:

        raw_email = item.get("email")

        # email key j na hoy, None hoy, ya "" / "null" / "none" hoy to skip
        if is_blank_email(raw_email):
            continue

        email = str(raw_email).strip()

        position = (
            "Python Django Developer Position"
        )

        emails = [e.strip() for e in email.split(",") if e.strip()]

        for e in emails:

            # split thi aavela individual email ma pan blank check
            if is_blank_email(e):
                continue

            # original item nu full data copy karo, ane single
            # email + position set karo (record per email)
            record = dict(item)
            record["email"] = e
            record["position"] = position

            pairs.append((e, position, record))

    return pairs


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(server, recipient, position):

    msg = MIMEMultipart()

    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    msg["Subject"] = EMAIL_SUBJECT.format(position=position)

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333333;">

    <p>Dear Hiring Manager,</p>

    <p>
    I hope you are doing well. My name is <strong>Dhruv Parikh</strong>,
    and I am writing to express my interest in the
    <strong>{position}</strong>.
    I have attached my resume to this email for your review.
    </p>

    <p>
    I have <strong>3.0+ years of experience</strong> in developing web
    applications using Python and Django, along with expertise in creating
    RESTful APIs, managing PostgreSQL databases, and integrating front-end
    technologies such as HTML, CSS, and JavaScript.
    I am passionate about building efficient and scalable solutions and would
    be excited to contribute to your team.
    </p>

    <p>
    Please let me know if you need any additional information or documents.
    I look forward to the opportunity to discuss how my skills and experience
    align with your requirements.
    </p>

    <p>
    Thank you for your time and consideration.
    </p>

    <br>

    <p>
    Best regards,<br>
    <strong>Dhruv Parikh</strong><br>
    Python Django Developer<br>
    📞 +91 7600524348<br>
    📧 parikhdhruv05@gmail.com
    </p>

    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    if RESUME_PATH and os.path.exists(RESUME_PATH):

        with open(RESUME_PATH, "rb") as f:

            attachment = MIMEApplication(
                f.read(),
                _subtype="pdf"
            )

            attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(RESUME_PATH)
            )

            msg.attach(attachment)

    server.send_message(msg)


# ============================================================
# MAIN
# ============================================================

def main():

    if not os.path.exists(JSON_FILE):
        print(f"\n❌ JSON File Not Found:\n{JSON_FILE}")
        return

    print("\n📂 Loading JSON File...")

    pairs = get_email_position_pairs(JSON_FILE)

    print(f"📧 Total Emails Found: {len(pairs)}")

    # Remove duplicates (same email multiple posts ma hoy to ek j vaar)
    unique_pairs = []
    seen = set()

    for email, position, record in pairs:

        email_lower = email.lower()

        if email_lower not in seen:
            seen.add(email_lower)
            unique_pairs.append((email, position, record))

    print(f"📧 Unique Emails: {len(unique_pairs)}")

    # Aaj sudhi (aa folder na badha sent log files) ma je email send thay
    # gaya chhe te badha load karo -> duplicate avoid karva
    already_sent_emails = load_today_sent_emails()

    pending = []

    for email, position, record in unique_pairs:

        if email.lower() not in already_sent_emails:

            if valid_email(email):
                pending.append((email, position, record))
            else:
                print(f"⚠ Invalid Email Skipped: {email}")

    print(f"📤 Pending Emails: {len(pending)}")

    if not pending:
        print("\n✅ No Pending Emails Found")
        return

    print("\n🔌 Connecting Gmail SMTP...")

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        print("✅ Login Successful\n")

    except Exception as e:

        print("❌ Gmail Login Failed")
        print(e)
        return

    # Aa run na sent / failed records (full post data + status)
    sent_records = []
    failed_records = []

    total = len(pending)

    for index, (email, position, record) in enumerate(pending, start=1):

        try:

            print(
                f"[{index}/{total}] Sending -> {email}"
            )

            send_email(
                server,
                email,
                position
            )

            sent_record = dict(record)
            sent_record["email_sent"] = True
            sent_record["status"] = "Sent"
            sent_record["sent_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sent_records.append(sent_record)

            save_log(
                SENT_LOG_FILE,
                sent_records
            )

            print("   ✅ Success")

        except Exception as e:

            failed_record = dict(record)
            failed_record["email_sent"] = False
            failed_record["status"] = "Failed"
            failed_record["error"] = str(e)
            failed_record["failed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            failed_records.append(failed_record)

            save_log(
                FAILED_LOG_FILE,
                failed_records
            )

            print("   ❌ Failed")
            print(f"   Error: {e}")

        if index < total:

            print(
                f"   ⏳ Waiting {DELAY_BETWEEN_EMAILS} sec..."
            )

            time.sleep(
                DELAY_BETWEEN_EMAILS
            )

    server.quit()

    print("\n🎉 Process Completed")

    print(
        f"✅ Sent Emails: {len(sent_records)}"
    )

    print(
        f"❌ Failed Emails: {len(failed_records)}"
    )

    print(f"\n📁 Logs saved in: {LOG_FOLDER}")
    print(f"   Sent log:   {SENT_LOG_FILE}")
    print(f"   Failed log: {FAILED_LOG_FILE}")


if __name__ == "__main__":
    main()