# 🚀 Smart Job Hunter & Spatial Outreach Studio 🌀

> **An All-in-One Automated Job Search, LinkedIn Scraper, Cold Email Engine, and Candidate Outreach Suite**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)](https://www.selenium.dev/)
[![OpenPyXL](https://img.shields.io/badge/Excel-OpenPyXL-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)](https://openpyxl.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 🌟 Overview

**Smart Job Hunter** is a powerful Python & Streamlit application designed to streamline the job application and recruiters outreach workflow. It automates finding hiring posts on LinkedIn, parsing candidate requirements, extracting HR contact info (emails, mobile numbers, apply links), generating personalized resumes, and firing targeted cold emails or WhatsApp pitches—all from a sleek, interactive 3D spatial web dashboard.

---

## ✨ Key Features

### 🔍 1. Automated LinkedIn Job & Post Scraper
- **Automated Login & Search:** Log in to LinkedIn using Selenium WebDriver (supports headless execution) and search target keywords (e.g., `Python Django Developer`, `Backend Engineer`).
- **Post & Filter Automation:** Automatically navigates to the **Posts** tab and filters by **Latest** posts.
- **Smart Data Extraction Engine:**
  - 📧 **Emails:** Extracts direct HR / recruiter email addresses (handles normal text & bold unicode text).
  - 📞 **Phone Numbers:** Detects Indian mobile numbers (+91 / 10-digit formats).
  - 🔗 **Application Links:** Identifies links from Greenhouse, Lever, Workday, Naukri, Instahyre, Unstop, Google Forms, WhatsApp, etc.
  - 📌 **Post Metadata:** Captures Poster Name, Post Date, Job Title/Position, Required Experience, Location, and Post Image URL.
- **Excel & JSON Export:** Automatically formats output into clean `.xlsx` Excel spreadsheets with styled headers, active hyperlinks, and column auto-resizing, as well as structured `.json` logs.

---

### 📧 2. Multi-Template Cold Email Outreach Engine
- **Preset & Custom Templates:** Built-in outreach templates tailored for Python/Django, Microservices, and Full-Stack roles.
- **SMTP Auto-Sender:** Send personalized cold emails with custom attachments (resumes in PDF format).
- **Batch Processing:** Send emails to multiple recruiter addresses sequentially with full success/failure logging.

---

### 💬 3. WhatsApp Pitch Helper
- **Automated WhatsApp Formatting:** Generates clean, professional pitch messages formatted for WhatsApp sharing.
- **Direct Messaging Links:** Prepares quick `wa.me` links or automated browser sessions to contact recruiters directly on WhatsApp.

---

### 📄 4. Dynamic Resume Builder
- **Custom Resume Generator:** Python script (`generate_custom_resume.py`) to programmatically build and output tailored resume documents for specific job descriptions and roles.

---

### 🌀 5. Futuristic 3D Streamlit Web Dashboard
- **Interactive UI (`app.py`):** Built with custom CSS featuring glassmorphism, 3D spatial depth effects, glowing badges, live browser status preview, and tabbed workflow navigation.

---

## 📁 Repository Structure

```text
smart-job-hunter/
├── app.py                                    # Main Streamlit 3D Web Application & Dashboard
├── job_find.py                               # Core LinkedIn scraper logic (v1)
├── job_find_2.py                             # Advanced regex extraction & post scraper (v2)
├── email_sender.py                           # SMTP Email outreach engine
├── email_sender_backup.py                    # Legacy/Backup email script
├── send_email.py                             # Command-line email launcher
├── testing_send_email.py                     # Email configuration test script
├── generate_custom_resume.py                 # Dynamic resume generator script
├── whatsapp_sender.py                        # WhatsApp message formatter & sender tool
├── Dhruv_Resume_Python_Django_Developer.py   # Developer profile / resume builder data
├── requirements.txt                          # Project python dependencies
└── README.md                                 # Project documentation
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- **Python 3.10+** installed.
- **Google Chrome** browser installed.
- **ChromeDriver** (managed automatically by Selenium/webdriver-manager or system PATH).

### 2. Clone the Repository
```bash
git clone https://github.com/DhruvParikh123/smart-job-hunter.git
cd smart-job-hunter
```

### 3. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Linux/macOS:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Launch the Streamlit Web Application
Run the interactive 3D UI dashboard:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

### Command-Line Script Usage

#### 1. LinkedIn Job Scraper
To run the scraper directly via terminal:
```bash
python job_find_2.py
```

#### 2. Send Cold Emails
```bash
python send_email.py
```

#### 3. Test Email Configuration
```bash
python testing_send_email.py
```

#### 4. WhatsApp Outreach
```bash
python whatsapp_sender.py
```

---

## 🔐 Environment & Credentials Note
- Keep your SMTP credentials (email & app password) and LinkedIn login details secure.
- Avoid committing sensitive passwords or tokens to version control. Use `.env` files or Streamlit secrets for production deployments.

---

## 👨‍💻 Author

Developed with ❤️ by **Dhruv Parikh**
- **Role:** Python / Django / Full-Stack Developer
- **Email:** [parikhdhruv05@gmail.com](mailto:parikhdhruv05@gmail.com)
- **GitHub:** [@DhruvParikh123](https://github.com/DhruvParikh123)

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
