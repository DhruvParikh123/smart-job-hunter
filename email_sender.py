import os
import re
import sys
import json
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Ensure Windows terminal handles UTF-8 emojis without encoding error
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


# ============================================================
# 📧 EMAIL CONFIGURATION
# ============================================================
email_sender = 'parikhdhruv05@gmail.com'
email_password = 'lkao mlwv hgle qvfr'  # Gmail App-specific password

# Target Email Recipients List
email_recipients = ["parikhdhruv05@gmail.com"]

# Path to PDF Resume
pdf_path = r'C:\Users\Admin\Downloads\Sending-Emails-With-Python-main\Sending-Emails-With-Python-main\Dhruv_Resume.pdf'

# Email Subject & Body
email_subject = 'Application for Python Django Developer Position - Dhruv Parikh'
email_body = '''Dear Hiring Manager,

I hope you are doing well. My name is Dhruv Parikh, and I am writing to let you know about my interest in the Python Django Developer position. I have attached my resume to this email for your review.

I have 3+ years of experience in developing web applications using Python and Django, along with expertise in creating RESTful APIs, managing PostgreSQL databases, and integrating front-end technologies like HTML, CSS, and JavaScript. I am passionate about building efficient and scalable solutions and would be excited to contribute to your team.

Please let me know if you need any additional information or documents. I look forward to the opportunity to discuss how my skills and experience align with your requirements.

Thank you for your time and consideration.

Best regards,
Dhruv Parikh
📞 +91 7600524348
📧 parikhdhruv05@gmail.com'''

HISTORY_FILE = "email_sent_history.json"
EMAIL_LOGS_DIR = "email_logs"
ONE_WEEK_DAYS = 7


# ============================================================
# 🔍 HISTORICAL SENT LOG & TIMESTAMPS PARSER
# ============================================================
def load_all_sent_history():
    """
    Scans persistent HISTORY_FILE and all JSON log files in email_logs/
    to build a dictionary mapping lowercased email -> latest datetime sent.
    """
    history = {}

    def update_history(email_str, timestamp_str):
        if not email_str or not timestamp_str:
            return
        # Split multiple emails if comma-separated
        emails = [e.strip().lower() for e in str(email_str).split(",") if e.strip()]
        dt = None
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d_%H-%M-%S", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(str(timestamp_str).strip(), fmt)
                break
            except ValueError:
                continue
        if dt:
            for email in emails:
                if email not in history or dt > history[email]:
                    history[email] = dt

    # 1. Read persistent JSON history file
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for email, info in data.items():
                        if isinstance(info, dict):
                            update_history(email, info.get("last_sent_at"))
                        elif isinstance(info, str):
                            update_history(email, info)
        except Exception as e:
            print(f"⚠️ Error reading history file {HISTORY_FILE}: {e}")

    # 2. Recursively scan all JSON log files in email_logs/ directory
    if os.path.exists(EMAIL_LOGS_DIR):
        for root, _, files in os.walk(EMAIL_LOGS_DIR):
            for file in files:
                if file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            records = json.load(f)
                            if isinstance(records, list):
                                for item in records:
                                    if isinstance(item, dict):
                                        if item.get("status") == "Sent" or item.get("email_sent"):
                                            email_val = item.get("email") or item.get("recipient")
                                            sent_time = item.get("sent_at") or item.get("timestamp")
                                            if not sent_time:
                                                # Try folder date e.g. email_logs/2026-09-03/
                                                folder_name = os.path.basename(root)
                                                if re.match(r'^\d{4}-\d{2}-\d{2}$', folder_name):
                                                    sent_time = f"{folder_name} 12:00:00"
                                            update_history(email_val, sent_time)
                    except Exception:
                        continue

    return history


def update_sent_history(email_sent_list):
    """
    Saves newly sent email timestamps into HISTORY_FILE and date-wise log folder.
    """
    history_data = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        except Exception:
            history_data = {}

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for email in email_sent_list:
        email_clean = email.strip().lower()
        history_data[email_clean] = {
            "last_sent_at": now_str,
            "status": "Sent",
            "subject": email_subject
        }

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)

    # Also save to email_logs/YYYY-MM-DD/ folder
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_log_dir = os.path.join(EMAIL_LOGS_DIR, today_str)
    os.makedirs(today_log_dir, exist_ok=True)

    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(today_log_dir, f"email_sender_log_{timestamp_str}.json")

    log_entries = [
        {
            "email": email,
            "status": "Sent",
            "sent_at": now_str,
            "subject": email_subject
        }
        for email in email_sent_list
    ]

    with open(log_filename, "w", encoding="utf-8") as f:
        json.dump(log_entries, f, ensure_ascii=False, indent=2)


# ============================================================
# 🚀 MAIN DISPATCH & STATUS CHECKER
# ============================================================
def main():
    print("=" * 70)
    print("📧 EMAIL DISPATCHER WITH 1-WEEK FREQUENCY CONTROL & STATUS AUDIT")
    print("=" * 70)

    now = datetime.now()
    sent_history = load_all_sent_history()

    eligible_recipients = []
    skipped_recipients = []

    print(f"\n🔍 Auditing {len(email_recipients)} recipient(s) against 1-Week ({ONE_WEEK_DAYS} Days) rule...\n")

    for idx, recipient in enumerate(email_recipients, start=1):
        clean_email = recipient.strip().lower()
        last_sent_dt = sent_history.get(clean_email)

        print(f"[{idx}/{len(email_recipients)}] 📬 {recipient}")

        if last_sent_dt is None:
            print(f"    ├─ Status   : 🆕 NEVER SENT BEFORE")
            print(f"    ├─ Last Sent: Never")
            print(f"    └─ Action   : ✅ ELIGIBLE (Will send email)")
            eligible_recipients.append((recipient, "Never Sent"))
        else:
            days_ago = (now - last_sent_dt).days
            last_sent_str = last_sent_dt.strftime("%Y-%m-%d %H:%M:%S")

            if days_ago >= ONE_WEEK_DAYS:
                print(f"    ├─ Status   : ✅ ELIGIBLE (More than 1 week ago)")
                print(f"    ├─ Last Sent: {last_sent_str} ({days_ago} days ago)")
                print(f"    └─ Action   : ✅ ELIGIBLE (Will send email)")
                eligible_recipients.append((recipient, f"{days_ago} days ago ({last_sent_str})"))
            else:
                days_remaining = ONE_WEEK_DAYS - days_ago
                print(f"    ├─ Status   : ⏭️ SKIPPED (Sent within 1 week)")
                print(f"    ├─ Last Sent: {last_sent_str} ({days_ago} day(s) ago)")
                print(f"    └─ Action   : ⏸️ SKIPPED (Must wait {days_remaining} more day(s))")
                skipped_recipients.append((recipient, last_sent_str, days_ago, days_remaining))

        print("-" * 70)

    print(f"\n📊 AUDIT SUMMARY:")
    print(f"   • Total Recipients : {len(email_recipients)}")
    print(f"   • Eligible to Send : {len(eligible_recipients)}")
    print(f"   • Skipped (< 1 Wk) : {len(skipped_recipients)}\n")

    if not eligible_recipients:
        print("✅ No emails to send today. All recipients received an email within the last 7 days.")
        return

    # Check PDF resume
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Resume PDF file not found at: {pdf_path}")
        return

    # Connect to Gmail SMTP
    print(f"🔌 Connecting to Gmail SMTP server (smtp.gmail.com:587)...")
    try:
        connection = smtplib.SMTP('smtp.gmail.com', 587)
        connection.ehlo()
        connection.starttls()
        connection.login(email_sender, email_password)
        print("✅ Logged in successfully!\n")
    except Exception as err:
        print(f"❌ Gmail Connection/Authentication Error: {err}")
        return

    successfully_sent = []
    failed_count = 0

    for idx, (recipient, last_info) in enumerate(eligible_recipients, start=1):
        print(f"[{idx}/{len(eligible_recipients)}] 📤 Sending email to `{recipient}` (Last sent: {last_info})...")
        try:
            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = recipient
            msg['Subject'] = email_subject
            msg.attach(MIMEText(email_body, 'plain'))

            with open(pdf_path, 'rb') as attachment:
                pdf_attachment = MIMEBase('application', 'octet-stream')
                pdf_attachment.set_payload(attachment.read())
            encoders.encode_base64(pdf_attachment)
            pdf_attachment.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(pdf_path)}'
            )
            msg.attach(pdf_attachment)

            connection.sendmail(email_sender, recipient, msg.as_string())
            successfully_sent.append(recipient)
            print(f"   ✅ Successfully delivered email to: {recipient}")

        except Exception as err:
            failed_count += 1
            print(f"   ❌ Failed to send email to {recipient}: {err}")

    connection.quit()

    if successfully_sent:
        update_sent_history(successfully_sent)

    print("\n" + "=" * 70)
    print(f"🎉 EXECUTION FINISHED! Total Sent: {len(successfully_sent)} | Skipped: {len(skipped_recipients)} | Failed: {failed_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()