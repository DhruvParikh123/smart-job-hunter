import os
import time
import subprocess
import urllib.parse
import webbrowser
import pyperclip
import pyautogui

# ============================================================
# 📱 WHATSAPP SETUP & RECIPIENTS
# ============================================================

# WhatsApp recipients list (Must include country code e.g. +919664755493)
whatsapp_recipients = [
    "+919998244418",  # Add recipient WhatsApp phone numbers here
]

# Path to the PDF resume file
pdf_path = r'C:\Users\Admin\Downloads\Sending-Emails-With-Python-main\Sending-Emails-With-Python-main\Dhruv_Resume.pdf'

# WhatsApp Body Message
body = '''Dear Hiring Manager,

I hope you are doing well. My name is Dhruv Parikh, and I am writing to express my interest in the *Python Django Developer* position.

I have 3 years of experience in developing web applications using Python and Django, along with expertise in creating RESTful APIs, managing PostgreSQL databases, and integrating front-end technologies like HTML, CSS, and JavaScript. I am passionate about building efficient and scalable solutions and would be excited to contribute to your team.

Please let me know if you need any additional information or documents. I look forward to the opportunity to discuss how my skills and experience align with your requirements.

Thank you for your time and consideration.

Best regards,
*Dhruv Parikh*
📞 +91 7600524348
📧 parikhdhruv05@gmail.com'''


def copy_file_to_clipboard(file_path):
    """
    Copies a file to Windows Clipboard as a File object so Ctrl+V in WhatsApp Web attaches it.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: PDF file not found at: {file_path}")
        return False
    try:
        powershell_cmd = f'Set-Clipboard -Path "{file_path}"'
        subprocess.run(["powershell", "-command", powershell_cmd], check=True)
        print(f"📎 Copied PDF file to Clipboard: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print(f"⚠️ Failed to copy PDF to clipboard: {e}")
        return False


def copy_text_to_clipboard(text):
    """
    Copies text message body to clipboard.
    """
    try:
        pyperclip.copy(text)
        print("📝 Copied message text to Clipboard")
        return True
    except Exception as e:
        print(f"⚠️ Failed to copy text to clipboard: {e}")
        return False


def send_whatsapp_messages():
    print("🚀 Starting WhatsApp Sender (PDF Attachment + Caption Message)...\n")

    # Verify PDF exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF File does not exist at {pdf_path}")
        return

    for phone in whatsapp_recipients:
        # Sanitize phone number string
        clean_phone = phone.strip()
        if not clean_phone.startswith("+"):
            clean_phone = "+" + clean_phone

        print(f"📱 Opening WhatsApp Web for {clean_phone}...")

        try:
            # 1. Open WhatsApp Web for target phone number
            whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_phone}"
            webbrowser.open(whatsapp_url)

            # Wait for WhatsApp Web to load the chat page
            print("⏳ Waiting 12 seconds for WhatsApp Web chat page to load...")
            time.sleep(12)

            # 2. Copy PDF file to Clipboard
            if not copy_file_to_clipboard(pdf_path):
                continue

            # 3. Paste PDF file into WhatsApp Web chat
            print("📎 Attaching PDF (Ctrl + V)...")
            pyautogui.hotkey('ctrl', 'v')

            # Wait 3 seconds for PDF Attachment Preview modal to open
            time.sleep(3)

            # Focus on "Type a message" caption box in Preview Modal
            sw, sh = pyautogui.size()
            pyautogui.click(int(sw * 0.55), int(sh * 0.92))
            time.sleep(0.5)

            # 4. Copy message body to Clipboard
            copy_text_to_clipboard(body)

            # 5. Paste message body into the PDF caption text box
            print("📝 Pasting message body into PDF caption (Ctrl + V)...")
            pyautogui.hotkey('ctrl', 'v')

            # Wait 1.5 seconds before pressing Send
            time.sleep(1.5)

            # 6. Press Enter and Click Send button
            print("📤 Pressing Enter & Clicking Send button...")
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.click(int(sw * 0.96), int(sh * 0.93))

            print(f"✅ PDF Resume with application message successfully sent to {clean_phone}!")

        except Exception as e:
            print(f"❌ Error sending to {clean_phone}: {e}")

        # Pause between recipients
        time.sleep(5)

    print("\n🎉 WhatsApp process completed successfully!")


if __name__ == "__main__":
    send_whatsapp_messages()
