import os
import re
import time
import json
import smtplib
import subprocess
import urllib.parse
import webbrowser
import pyperclip
import pyautogui
import openpyxl
from openpyxl.styles import Font, Alignment
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# 🎨 PAGE CONFIGURATION - INTERACTIVE 3D SCROLL EDITION
# ============================================================
st.set_page_config(
    page_title="Spatial3D Outreach Studio 🌀 | Interactive 3D Perspective",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_width_arg(stretch=True):
    try:
        import inspect
        sig = inspect.signature(st.button)
        if "width" in sig.parameters:
            return {"width": "stretch" if stretch else "content"}
    except Exception:
        pass
    return {"use_container_width": stretch}


# ============================================================
# 🌀 INTERACTIVE 3D SCROLL & SPATIAL PERSPECTIVE STYLING
# ============================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
    /* 🌐 Global Typography & Smooth 3D Canvas Context */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        scroll-behavior: smooth;
    }

    h1, h2, h3, .heading-3d {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* 🌌 Interactive 3D Spatial Background Canvas */
    .stApp {
        background: #030712;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.18) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(14, 165, 233, 0.15) 0px, transparent 50%),
            linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        background-attachment: fixed;
    }

    /* 🌀 Floating 3D Spatial Hero Section with Parallax Perspective */
    .hero-3d-box {
        perspective: 1000px;
        margin-bottom: 1.5rem;
    }

    .hero-3d-card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(168, 85, 247, 0.4);
        border-radius: 1.8rem;
        padding: 2.2rem 2.8rem;
        position: relative;
        transform-style: preserve-3d;
        transform: rotateX(2deg) rotateY(-1deg);
        box-shadow: 
            0 25px 60px rgba(0, 0, 0, 0.7),
            0 0 50px rgba(99, 102, 241, 0.25),
            inset 0 1px 2px rgba(255, 255, 255, 0.25);
        transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.6s ease;
    }

    .hero-3d-card:hover {
        transform: rotateX(0deg) rotateY(0deg) translateZ(18px);
        box-shadow: 
            0 35px 80px rgba(0, 0, 0, 0.85),
            0 0 70px rgba(168, 85, 247, 0.4),
            inset 0 1px 3px rgba(255, 255, 255, 0.4);
    }

    .title-3d {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #C084FC 50%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 10px 30px rgba(168, 85, 247, 0.35);
        margin-bottom: 0.5rem;
    }

    .subtitle-3d {
        font-size: 1.15rem;
        color: #94A3B8;
        max-width: 850px;
        line-height: 1.6;
    }

    /* 💎 3D Tilt Cards with Depth Perspective */
    .card-3d {
        background: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.25rem;
        padding: 1.25rem 1.5rem;
        box-shadow: 
            0 10px 25px rgba(0, 0, 0, 0.5),
            0 1px 2px rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
        position: relative;
    }

    .card-3d:hover {
        transform: translateY(-6px) translateZ(12px) rotateX(-2deg);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 
            0 20px 45px rgba(0, 0, 0, 0.75),
            0 0 30px rgba(56, 189, 248, 0.3);
    }

    .val-3d {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .lbl-3d {
        font-size: 0.75rem;
        color: #C084FC;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        margin-bottom: 4px;
    }

    /* 🏷️ 3D Glowing Badges */
    .badge-3d-cyan {
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.15);
    }

    .badge-3d-purple {
        background: rgba(168, 85, 247, 0.12);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.35);
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.15);
    }

    /* 🎯 Section Headers */
    .header-3d {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    /* 🎛️ Form Controls with 3D Inset Depth */
    .stTextArea textarea, .stTextInput input, .stSelectbox > div > div {
        border-radius: 12px !important;
        background-color: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        color: #F8FAFC !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #A855F7 !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.3), inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
    }

    /* 🚀 3D Dynamic Launch Button */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #06B6D4 100%) !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.85rem 2rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 
            0 10px 25px rgba(99, 102, 241, 0.4),
            0 0 15px rgba(168, 85, 247, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        transform: translateZ(5px);
    }

    .stButton button[kind="primary"]:hover {
        transform: translateY(-3px) translateZ(15px) !important;
        box-shadow: 
            0 15px 35px rgba(99, 102, 241, 0.6),
            0 0 30px rgba(56, 189, 248, 0.5) !important;
    }

    code {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Streamlit Tabs 3D Upgrade */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.7);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 8px 18px;
        color: #94A3B8;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 📁 CONSTANTS & ENGINE HELPERS
# ============================================================
DEFAULT_RESUME = r'C:\Users\Admin\Downloads\Sending-Emails-With-Python-main\Sending-Emails-With-Python-main\Dhruv_Resume.pdf'

PRESET_TEMPLATES = {
    "🌀 Executive 3D Python Django Pitch": {
        "subject": "Application for Python Django Developer Position - Dhruv Parikh",
        "body": """Dear Hiring Manager,

I hope you are doing well. My name is Dhruv Parikh, and I am writing to express my interest in the Python Django Developer position. I have attached my resume to this email for your review.

I have 3+ years of hands-on experience in developing scalable web applications using Python, Django, and Django REST Framework, along with expertise in PostgreSQL database management, API integrations, and front-end technologies (HTML, CSS, JavaScript).

Please let me know if you need any additional information. I look forward to discussing how my experience aligns with your team's goals.

Thank you for your time and consideration.

Best regards,
Dhruv Parikh
📞 +91 7600524348
📧 parikhdhruv05@gmail.com"""
    },
    "🌌 Microservices & Spatial Cloud Architecture": {
        "subject": "Application for Backend Developer / REST API Specialist - Dhruv Parikh",
        "body": """Dear Hiring Team,

I am reaching out to submit my application for the Backend Engineer role. With extensive expertise in Python microservices, Django ORM optimization, and REST API development, I have successfully delivered high-performance web systems.

Key Technical Highlights:
• 3+ Years in Python & Django Architecture
• PostgreSQL & Query Optimization
• RESTful API Design & Integration
• Automation, Web Scraping & Scripting

I would welcome the opportunity to discuss how my skill set fits your requirements. Resume is attached for your reference.

Best regards,
Dhruv Parikh
📞 +91 7600524348"""
    },
    "⚡ Full-Stack Enterprise Systems": {
        "subject": "Application for Full-Stack Python Developer - Dhruv Parikh",
        "body": """Hello Hiring Manager,

I hope this email finds you well. I am excited to apply for the Full-Stack Python Developer position. My background encompasses full-lifecycle development using Django, Flask, HTML5, CSS3, JavaScript, and database management.

I take pride in writing clean, maintainable code and delivering user-focused software solutions. Please find my detailed resume attached to this email.

Looking forward to connecting soon!

Best regards,
Dhruv Parikh
+91 7600524348 | parikhdhruv05@gmail.com"""
    }
}

def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def copy_file_to_clipboard(file_path):
    if not os.path.exists(file_path):
        return False, f"File not found at: {file_path}"
    try:
        powershell_cmd = f'Set-Clipboard -Path "{file_path}"'
        subprocess.run(["powershell", "-command", powershell_cmd], check=True)
        return True, "Success"
    except Exception as e:
        return False, str(e)

def copy_text_to_clipboard(text):
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False

def get_saved_logs():
    logs = []
    base_dir = "email_logs"
    if os.path.exists(base_dir):
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".json"):
                    logs.append(os.path.join(root, file))
    return sorted(logs, reverse=True)


# ============================================================
# 🔄 SESSION STATE INITIALIZATION FOR CROSS-TAB AUTOMATION
# ============================================================
if "target_emails" not in st.session_state:
    st.session_state["target_emails"] = "hr@mindlyticai.com, himanshu@moverrotechno.in"
if "target_phones" not in st.session_state:
    st.session_state["target_phones"] = "+919998244418"
if "scraped_data" not in st.session_state:
    st.session_state["scraped_data"] = []


# ============================================================
# 🔎 LINKEDIN EXTRACTION & SCRAPER ENGINE HELPERS (job_find_2.py)
# ============================================================
def build_bold_map():
    bold_map = {}
    for i in range(26):
        bold_map[chr(0x1D400 + i)] = chr(ord('A') + i)
        bold_map[chr(0x1D41A + i)] = chr(ord('a') + i)
    for i in range(10):
        bold_map[chr(0x1D7CE + i)] = chr(ord('0') + i)
    return bold_map

BOLD_MAP = build_bold_map()

def normalize_bold(text):
    return "".join(BOLD_MAP.get(ch, ch) for ch in text)

def extract_emails(text):
    normal_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    normalized_text = normalize_bold(text)
    bold_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', normalized_text)
    all_emails = list(set(normal_emails + bold_emails))
    return ", ".join(all_emails) if all_emails else ""

def extract_phone_numbers(text):
    normalized_text = normalize_bold(text)
    pattern = r'(?:\+?91[\s-]?)?[6-9]\d{9}'
    matches = re.findall(pattern, normalized_text)
    spaced_pattern = r'(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}'
    spaced_matches = re.findall(spaced_pattern, normalized_text)
    all_numbers = set()
    for m in matches + spaced_matches:
        cleaned = re.sub(r'[\s-]', '', m)
        if len(cleaned) >= 10:
            all_numbers.add(cleaned)
    return ", ".join(all_numbers) if all_numbers else ""

def extract_apply_links(text):
    normalized = normalize_bold(text)
    lnkd_pattern = r'https?://lnkd\.in/[^\s\)\]>\"\'<]+'
    lnkd_links = re.findall(lnkd_pattern, normalized)
    ats_pattern = (
        r'https?://(?:'
        r'(?:[\w-]+\.)?greenhouse\.io|'
        r'(?:[\w-]+\.)?lever\.co|'
        r'(?:[\w-]+\.)?workday\.com|'
        r'(?:[\w-]+\.)?naukri\.com|'
        r'(?:[\w-]+\.)?instahyre\.com|'
        r'(?:[\w-]+\.)?internshala\.com|'
        r'(?:[\w-]+\.)?unstop\.com|'
        r'(?:[\w-]+\.)?cutshort\.io|'
        r'(?:[\w-]+\.)?wellfound\.com|'
        r'(?:[\w-]+\.)?angellist\.com|'
        r'(?:[\w-]+\.)?indeed\.com|'
        r'(?:[\w-]+\.)?foundit\.in|'
        r'wa\.me|'
        r'chat\.whatsapp\.com|'
        r'forms\.gle|'
        r'docs\.google\.com/forms'
        r')[^\s\)\]>\"\'<]+'
    )
    ats_links = re.findall(ats_pattern, normalized)
    keyword_context = re.findall(
        r'(?:apply|Apply|APPLY|join|Join|career|Career|form|Form|link|Link|here|Here)'
        r'.{0,80}?(https?://[^\s\)\]>\"\'<]+)',
        normalized
    )
    all_links = []
    seen = set()
    for link in lnkd_links + ats_links + keyword_context:
        link = re.sub(r'[.,;:!?\)\]]+$', '', link)
        if link not in seen and len(link) > 10:
            seen.add(link)
            all_links.append(link)
    return ", ".join(all_links[:5]) if all_links else ""

def extract_position(text):
    patterns = [
        r'(?:Hiring for|Position|Role|Job Title|We are hiring|hiring)[:\-]?\s*([A-Za-z0-9 /&,\-\(\)]{3,60})',
        r'🔹\s*([A-Za-z0-9 /&,\-\(\)]{3,60})',
        r'(?:^|\n)([A-Za-z][A-Za-z0-9 /&,\-\(\)]{3,50}(?:Developer|Engineer|Manager|Executive|Designer|Analyst|Lead|Architect|Consultant|Intern|Specialist))',
    ]
    found_positions = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        for m in matches:
            cleaned = m.strip()
            if cleaned and len(cleaned) < 70:
                found_positions.append(cleaned)
    seen = set()
    unique_positions = []
    for p in found_positions:
        if p not in seen:
            seen.add(p)
            unique_positions.append(p)
    return " | ".join(unique_positions[:5]) if unique_positions else ""

def extract_location(text):
    patterns = [
        r'(?:Location|📍)\s*[:\-]?\s*([A-Za-z ,]{2,40})',
        r'(?:Work From Office|Work From Home|Remote|Hybrid)[^\n]*',
    ]
    found_locations = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            cleaned = m.strip()
            if cleaned and len(cleaned) < 60:
                found_locations.append(cleaned)
    seen = set()
    unique_locations = []
    for loc in found_locations:
        if loc not in seen:
            seen.add(loc)
            unique_locations.append(loc)
    return " | ".join(unique_locations[:5]) if unique_locations else ""

def extract_experience(text):
    normalized_text = normalize_bold(text)
    patterns = [
        r'(?:Experience|Exp)[:\-]?\s*(\d+\+?\s*(?:-|–|to)?\s*\d*\+?\s*(?:Years|years|Yrs|yrs))',
        r'(\d+\+?\s*(?:-|–|to)\s*\d+\+?\s*(?:Years|years|Yrs|yrs))',
        r'(\d+\+\s*(?:Years|years|Yrs|yrs))',
        r'(\d+\s*(?:Years|years|Yrs|yrs)\s*(?:of\s*)?(?:experience|exp))',
    ]
    found = []
    for pattern in patterns:
        matches = re.findall(pattern, normalized_text, re.IGNORECASE)
        for m in matches:
            cleaned = m.strip()
            if cleaned:
                found.append(cleaned)
    seen = set()
    unique = []
    for e in found:
        if e.lower() not in seen:
            seen.add(e.lower())
            unique.append(e)
    return " | ".join(unique[:3]) if unique else ""

def extract_post_info(text):
    return {
        "email":       extract_emails(text),
        "mobile":      extract_phone_numbers(text),
        "apply_link":  extract_apply_links(text),
        "position":    extract_position(text),
        "location":    extract_location(text),
        "experience":  extract_experience(text),
    }

def get_poster_name_date_image(post_element, driver):
    poster_name, post_date, image_url = "", "", ""
    parent = None
    ancestor_xpaths = [
        "./ancestor::div[contains(@class,'feed-shared-update-v2')][1]",
        "./ancestor::div[contains(@data-urn,'urn:li:activity')][1]",
        "./ancestor::div[contains(@class,'d368900e')][1]",
        "./ancestor::div[@componentkey][1]",
    ]
    for xp in ancestor_xpaths:
        try:
            el = post_element.find_element(By.XPATH, xp)
            if el:
                parent = el
                break
        except Exception:
            continue
    if not parent:
        return poster_name, post_date, image_url

    name_selectors = [
        ".update-components-actor__name",
        ".update-components-actor__title",
        "span.feed-shared-actor__name",
    ]
    for sel in name_selectors:
        try:
            el = parent.find_element(By.CSS_SELECTOR, sel)
            if el.text.strip():
                poster_name = el.text.strip().split("\n")[0]
                break
        except Exception:
            continue

    date_selectors = [
        ".update-components-actor__sub-description",
        "span.feed-shared-actor__sub-description",
        "time",
    ]
    for sel in date_selectors:
        try:
            el = parent.find_element(By.CSS_SELECTOR, sel)
            if el.text.strip():
                post_date = el.text.strip().split("\n")[0]
                break
        except Exception:
            continue

    try:
        all_imgs = parent.find_elements(By.TAG_NAME, "img")
        for img in all_imgs:
            src = img.get_attribute("src") or ""
            if "media.licdn.com" in src and (
                "feedshare-shrink" in src
                or "feedshare-image" in src
                or "feedshare-shrink_800" in src
                or "feedshare-shrink_1280" in src
            ):
                image_url = src
                break
    except Exception:
        pass

    return poster_name, post_date, image_url

def click_all_see_more_buttons(driver):
    clicked = 0
    try:
        see_more_selectors = [
            "button[data-testid='expandable-text-button']",
            "button.feed-shared-inline-show-more-text__see-more-less-toggle",
            "span.feed-shared-inline-show-more-text__see-more-less-toggle",
            ".see-more",
            "button[aria-label='see more']",
        ]
        for selector in see_more_selectors:
            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
            for btn in buttons:
                try:
                    if btn.is_displayed():
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                        time.sleep(0.2)
                        driver.execute_script("arguments[0].click();", btn)
                        clicked += 1
                except Exception:
                    continue
    except Exception:
        pass
    return clicked

def get_full_post_text(post_element, driver):
    try:
        see_more_btns = post_element.find_elements(
            By.CSS_SELECTOR, "button[data-testid='expandable-text-button']"
        )
        for btn in see_more_btns:
            try:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", btn)
            except Exception:
                pass
        text = post_element.text.strip()
        if text.endswith("… more"):
            text = text[:-6].strip()
        if text.endswith("…more"):
            text = text[:-5].strip()
        return text
    except Exception:
        return ""

def save_to_excel(all_posts_data, filename="linkedin_posts.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "LinkedIn Posts"
    headers = [
        "Post #", "Poster Name", "Post Date", "Position",
        "Experience", "Location", "Email", "Mobile Number",
        "Apply Link", "Image URL", "Full Post Text"
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for data in all_posts_data:
        row = [
            data.get("post_number", ""),
            data.get("poster_name", ""),
            data.get("post_date", ""),
            data.get("position", ""),
            data.get("experience", ""),
            data.get("location", ""),
            data.get("email", ""),
            data.get("mobile", ""),
            data.get("apply_link", ""),
            data.get("image_url", ""),
            data.get("full_text", ""),
        ]
        ws.append(row)
        current_row = ws.max_row
        apply_val = data.get("apply_link", "")
        if apply_val:
            first_link = apply_val.split(",")[0].strip()
            cell = ws.cell(row=current_row, column=9)
            cell.hyperlink = first_link
            cell.style = "Hyperlink"
        if data.get("image_url", ""):
            cell = ws.cell(row=current_row, column=10)
            cell.hyperlink = data.get("image_url", "")
            cell.style = "Hyperlink"

    col_widths = [8, 25, 15, 35, 15, 25, 35, 20, 60, 50, 80]
    for i, width in enumerate(col_widths, 1):
        col_letter = openpyxl.utils.get_column_letter(i)
        ws.column_dimensions[col_letter].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(filename)

def get_saved_linkedin_outputs():
    outputs = []
    base_dir = "linkedin_posts_output"
    if os.path.exists(base_dir):
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".json") or file.endswith(".xlsx"):
                    outputs.append(os.path.join(root, file))
    return sorted(outputs, reverse=True)

def run_linkedin_job_scraper(query, email, password, max_posts=50, max_no_change=4, headless=True, status_box=None, prog_bar=None, log_container=None, preview_container=None):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    def update_preview(stage_name=""):
        try:
            img_data = driver.get_screenshot_as_png()
            st.session_state["last_browser_screenshot"] = img_data
            if preview_container is not None:
                preview_container.image(
                    img_data,
                    caption=f"🌐 Live Embedded LinkedIn Browser Frame — {stage_name}",
                    use_container_width=True
                )
        except Exception:
            pass


    today_str = datetime.now().strftime("%Y-%m-%d")
    BASE_OUTPUT_DIR = "linkedin_posts_output"
    OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, today_str)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_posts = []
    all_posts_data = []
    seen_texts = set()
    no_change_count = 0
    last_post_count = 0

    try:
        if status_box: status_box.markdown("⏳ **[1/5] Logging in to LinkedIn...**")
        driver.get("https://www.linkedin.com/jobs/")
        update_preview("Opening LinkedIn Jobs Login Page")

        email_input = wait.until(EC.presence_of_element_located((By.ID, "session_key")))
        email_input.send_keys(email)
        update_preview(f"Typed Email: {email}")

        password_input = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
        password_input.send_keys(password)
        update_preview("Typed LinkedIn Password")

        sign_in_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        sign_in_btn.click()
        update_preview("Submitting Login Form...")
        time.sleep(4)
        update_preview("LinkedIn Dashboard / Search Page Loaded")

        if status_box: status_box.markdown(f"⏳ **[2/5] Searching query: `{query}`...**")
        job_search = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='typeahead-input']"))
        )
        job_search.clear()
        job_search.send_keys(query)
        update_preview(f"Typed Search Query: '{query}'")
        job_search.send_keys(Keys.ENTER)
        update_preview("Submitted Search Query")
        time.sleep(4)

        if status_box: status_box.markdown("⏳ **[3/5] Navigating to Posts tab...**")
        jobs_dropdown = wait.until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(.,'Jobs')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", jobs_dropdown)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", jobs_dropdown)
        update_preview("Opened Jobs Filter Dropdown")
        time.sleep(2)

        posts_option = wait.until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='Posts']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", posts_option)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", posts_option)
        update_preview("Selected 'Posts' Filter Option")
        time.sleep(2)

        if status_box: status_box.markdown("⏳ **[4/5] Filtering by Latest Posts...**")
        sort_by = wait.until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(.,'Sort by')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sort_by)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", sort_by)
        update_preview("Opened 'Sort By' Dropdown")
        time.sleep(2)

        latest_option = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Latest']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", latest_option)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", latest_option)
        update_preview("Selected 'Latest' Sort Filter")
        time.sleep(2)

        show_results = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Show results']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", show_results)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", show_results)
        update_preview("Clicked 'Show Results'")

        wait.until(EC.url_contains("/search/results/content/"))
        time.sleep(3)
        update_preview("LinkedIn Posts Search Results Ready")

        if status_box: status_box.markdown("⏳ **[5/5] Extracting posts & contacts...**")

        while True:
            click_all_see_more_buttons(driver)
            update_preview(f"Expanded Truncated Posts ('See More') — {len(all_posts)} collected")
            time.sleep(1)

            post_elements = driver.find_elements(
                By.CSS_SELECTOR, "[data-testid='expandable-text-box']"
            )

            for post in post_elements:
                try:
                    full_text = get_full_post_text(post, driver)
                    if full_text and full_text not in seen_texts and len(full_text) > 30:
                        seen_texts.add(full_text)
                        all_posts.append(full_text)

                        poster_name, post_date, image_url = get_poster_name_date_image(post, driver)
                        info = extract_post_info(full_text)

                        post_data = {
                            "post_number":  len(all_posts),
                            "poster_name":  poster_name,
                            "post_date":    post_date,
                            "position":     info["position"],
                            "experience":   info["experience"],
                            "location":     info["location"],
                            "email":        info["email"],
                            "mobile":       info["mobile"],
                            "apply_link":   info["apply_link"],
                            "image_url":    image_url,
                            "full_text":    full_text,
                        }
                        all_posts_data.append(post_data)

                        if log_container:
                            log_container.text(f"✅ #{len(all_posts)} | {poster_name} | Exp: {info['experience'] or '-'} | 📧 {info['email'] or '-'} | 📱 {info['mobile'] or '-'}")
                except Exception:
                    continue

            if prog_bar:
                prog_bar.progress(min(len(all_posts) / max_posts, 1.0))

            if status_box:
                status_box.markdown(f"⏳ **Collected {len(all_posts)} / {max_posts} LinkedIn Job Posts...**")

            if len(all_posts) >= max_posts:
                break

            if len(all_posts) == last_post_count:
                no_change_count += 1
                if no_change_count >= max_no_change:
                    break
            else:
                no_change_count = 0

            last_post_count = len(all_posts)

            if post_elements:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", post_elements[-1])
                    time.sleep(1.5)
                except Exception:
                    pass

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            driver.execute_script("window.scrollBy(0, -400);")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            update_preview(f"Scrolling down for new posts ({len(all_posts)} collected)")
            time.sleep(2)


            if len(all_posts) == last_post_count:
                no_change_count += 1
                if no_change_count >= max_no_change:
                    break
            else:
                no_change_count = 0

            last_post_count = len(all_posts)

            if post_elements:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", post_elements[-1])
                    time.sleep(1.5)
                except Exception:
                    pass

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            driver.execute_script("window.scrollBy(0, -400);")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)

        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        txt_path  = os.path.join(OUTPUT_DIR, f"linkedin_posts_{timestamp_str}.txt")
        json_path = os.path.join(OUTPUT_DIR, f"linkedin_posts_{timestamp_str}.json")
        xlsx_path = os.path.join(OUTPUT_DIR, f"linkedin_posts_{timestamp_str}.xlsx")

        with open(txt_path, "w", encoding="utf-8") as f:
            for i, data in enumerate(all_posts_data, 1):
                f.write(f"{'=' * 60}\nPOST #{i}\n{'=' * 60}\n")
                f.write(f"Poster  : {data['poster_name']}\nDate    : {data['post_date']}\nPosition: {data['position']}\nExp     : {data['experience']}\nLocation: {data['location']}\nEmail   : {data['email']}\nMobile  : {data['mobile']}\nApply   : {data['apply_link']}\nImage   : {data['image_url']}\n\n{data['full_text']}\n\n")

        save_to_excel(all_posts_data, xlsx_path)

        if preview_container is not None:
            preview_container.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid rgba(16, 185, 129, 0.5); border-radius: 18px; padding: 20px; text-align: center; margin-top: 10px; margin-bottom: 10px;">
                <div style="font-size: 2.8rem; margin-bottom: 5px;">🎉</div>
                <h3 style="color: #10B981; font-family: 'Space Grotesk', sans-serif; margin: 0; font-size: 1.4rem;">Scraping Completed Successfully!</h3>
                <p style="color: #F8FAFC; margin-top: 6px; font-size: 0.95rem;">Extracted <b>{len(all_posts)}</b> LinkedIn posts & contacts. Embedded browser window closed cleanly.</p>
            </div>
            """, unsafe_allow_html=True)

        return all_posts_data, txt_path, json_path, xlsx_path

    finally:
        driver.quit()




# ============================================================
# 👤 SIDEBAR - CONTROL CENTER (3D DESIGN)
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(168, 85, 247, 0.35); padding: 22px; border-radius: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div style="font-size: 3.5rem; margin-bottom: 5px;">🌌</div>
        <h3 style="margin: 0; font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 700; color: #F8FAFC;">Dhruv Parikh</h3>
        <p style="margin: 3px 0 12px 0; color: #38BDF8; font-size: 0.85rem; font-weight: 600;">Python Django Engineer</p>
        <span class="badge-3d-purple">3D PERSPECTIVE EDITION</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔐 Credentials Configuration")
    sender_email = st.text_input("Sender Gmail", value="parikhdhruv05@gmail.com")
    sender_password = st.text_input("Gmail App Password", value="lkao mlwv hgle qvfr", type="password")

    st.markdown("---")
    st.markdown("### 📄 Resume File Manager")
    
    resume_source = st.radio("PDF Source", ["Local System File", "Upload Custom PDF"])
    pdf_path_to_use = DEFAULT_RESUME

    if resume_source == "Upload Custom PDF":
        up_file = st.file_uploader("Upload Resume (.pdf)", type=["pdf"])
        if up_file is not None:
            os.makedirs("temp_resumes", exist_ok=True)
            t_path = os.path.join("temp_resumes", up_file.name)
            with open(t_path, "wb") as f:
                f.write(up_file.getbuffer())
            pdf_path_to_use = t_path
            st.sidebar.success(f"Uploaded: {up_file.name}")
    else:
        pdf_path_to_use = st.sidebar.text_input("Local File Path", value=DEFAULT_RESUME)

    if os.path.exists(pdf_path_to_use):
        file_size_kb = round(os.path.getsize(pdf_path_to_use) / 1024, 1)
        st.markdown(f"""
        <div class="badge-3d-cyan" style="width: 100%; justify-content: center; margin-top: 6px; display: flex; text-align: center;">
            📄 {os.path.basename(pdf_path_to_use)} ({file_size_kb} KB)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ PDF File Not Found!")

    st.markdown("---")
    st.caption("Spatial3D Outreach v10.0 • 3D Interactive Perspective")


# ============================================================
# 🌌 3D SCROLL FLOATING HERO BANNER WITH THREE.JS CANVAS
# ============================================================
st.markdown("""
<div class="hero-3d-box">
    <div class="hero-3d-card">
        <div class="title-3d">Spatial3D Outreach Studio 🌌</div>
        <div class="subtitle-3d">Next-generation 3D spatial job search automation platform. Multi-channel resume dispatch powered by Gmail SMTP & automated WhatsApp Web engine.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 🌐 Embedded Three.js 3D Interactive WebGL Canvas Component
components.html("""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: transparent; overflow: hidden; }
        #canvas-container { 
            width: 100%; 
            height: 220px; 
            border-radius: 20px; 
            overflow: hidden; 
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(168, 85, 247, 0.3);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(99, 102, 241, 0.2);
        }
    </style>
</head>
<body>
    <div id="canvas-container"></div>
    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 4.0;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        // 3D Torus Knot Geometry
        const geometry = new THREE.TorusKnotGeometry(1.0, 0.3, 100, 16);
        const material = new THREE.MeshStandardMaterial({
            color: 0xA855F7,
            emissive: 0x4F46E5,
            wireframe: true,
            roughness: 0.2,
            metalness: 0.8
        });
        const torusKnot = new THREE.Mesh(geometry, material);
        scene.add(torusKnot);

        // 3D Particle Cloud
        const particlesGeo = new THREE.BufferGeometry();
        const count = 350;
        const posArray = new Float32Array(count * 3);
        for(let i = 0; i < count * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 12;
        }
        particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particlesMat = new THREE.PointsMaterial({
            size: 0.035,
            color: 0x38BDF8,
            transparent: true,
            opacity: 0.85
        });
        const particlesMesh = new THREE.Points(particlesGeo, particlesMat);
        scene.add(particlesMesh);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0x38BDF8, 2.5);
        pointLight.position.set(5, 5, 5);
        scene.add(pointLight);

        // Mouse interaction
        let mouseX = 0, mouseY = 0;
        window.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth - 0.5) * 1.2;
            mouseY = (e.clientY / window.innerHeight - 0.5) * 1.2;
        });

        function animate() {
            requestAnimationFrame(animate);
            torusKnot.rotation.x += 0.008;
            torusKnot.rotation.y += 0.012;
            torusKnot.rotation.x += mouseY * 0.03;
            torusKnot.rotation.y += mouseX * 0.03;
            particlesMesh.rotation.y -= 0.0015;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    </script>
</body>
</html>
""", height=230)

st.markdown("<br>", unsafe_allow_html=True)

# 3D PERSPECTIVE STAT CARDS
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="card-3d">
        <div class="lbl-3d">Primary Dispatch</div>
        <div class="val-3d">GMAIL SMTP</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card-3d">
        <div class="lbl-3d">Secondary Engine</div>
        <div class="val-3d">WHATSAPP WEB</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card-3d">
        <div class="lbl-3d">PDF Status</div>
        <div class="val-3d">VERIFIED 3D</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="card-3d">
        <div class="lbl-3d">Spatial Engine</div>
        <div class="val-3d">ACTIVE 3D</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# 🗂️ MAIN TABS SYSTEM
# ============================================================
tab_email, tab_whatsapp, tab_scraper, tab_logs = st.tabs([
    "✉️ Email Dispatch Studio",
    "💬 WhatsApp Web Engine",
    "🔎 LinkedIn Job Finder Engine",
    "📊 Historic Logs & Analytics"
])


# ============================================================
# ✉️ TAB 1: EMAIL DISPATCH STUDIO
# ============================================================
with tab_email:
    c_left, c_right = st.columns([1.1, 0.9])

    with c_left:
        st.markdown('<div class="header-3d">🎯 Recipient Target List</div>', unsafe_allow_html=True)

        recipients_input = st.text_area(
            "Target Recipient Emails (Comma or newline separated)",
            value=st.session_state.get("target_emails", "hr@mindlyticai.com, himanshu@moverrotechno.in"),
            height=120
        )
        st.session_state["target_emails"] = recipients_input


        raw_list = re.split(r'[,\n\s]+', recipients_input)
        valid_recipients = [e.strip() for e in raw_list if e.strip() and valid_email(e.strip())]
        invalid_recipients = [e.strip() for e in raw_list if e.strip() and not valid_email(e.strip())]

        st.markdown(f"""
        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
            <span class="badge-3d-cyan">✓ Valid Emails: {len(valid_recipients)}</span>
            {'<span class="badge-3d-purple" style="color:#F87171; border-color: rgba(248,113,113,0.4);">⚠️ Invalid: ' + str(len(invalid_recipients)) + '</span>' if invalid_recipients else ''}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        selected_template_name = st.selectbox(
            "Choose Message Preset Template",
            list(PRESET_TEMPLATES.keys())
        )
        
        current_preset = PRESET_TEMPLATES[selected_template_name]

        subject_line = st.text_input("Email Subject Line", value=current_preset["subject"])
        delay_sec = st.slider("Pause Between Emails (Seconds)", min_value=1, max_value=30, value=5)

    with c_right:
        st.markdown('<div class="header-3d">📝 Content Editor & 3D Live Preview</div>', unsafe_allow_html=True)

        email_body = st.text_area(
            "Email Body Template",
            value=current_preset["body"],
            height=250
        )

        # Word Count & Formatting Character Gauge
        words_cnt = len(email_body.split())
        chars_cnt = len(email_body)
        st.markdown(f"""
        <div style="display: flex; gap: 14px; margin-top: 6px; font-size: 0.85rem; color: #94A3B8; margin-bottom: 10px;">
            <span>📊 Words: <b style="color: #38BDF8;">{words_cnt}</b></span>
            <span>|</span>
            <span>🔤 Characters: <b style="color: #C084FC;">{chars_cnt}</b></span>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("👁️ Click to View Live Rendered Application Email"):
            st.markdown(f"**From:** `{sender_email}`")
            st.markdown(f"**To:** `{valid_recipients[0] if valid_recipients else 'target_hr@company.com'}`")
            st.markdown(f"**Subject:** `{subject_line}`")
            st.markdown(f"**Attachment:** 📎 `{os.path.basename(pdf_path_to_use)}`")
            st.markdown("---")
            st.text(email_body)

    st.markdown("---")

    if st.button("🚀 LAUNCH SPATIAL 3D EMAIL CAMPAIGN", type="primary", **get_width_arg(True)):
        if not valid_recipients:
            st.error("❌ No valid recipient emails found!")
        elif not os.path.exists(pdf_path_to_use):
            st.error(f"❌ PDF Resume file missing at path: `{pdf_path_to_use}`")
        elif not sender_email or not sender_password:
            st.error("❌ Please provide Gmail Address and App Password in Sidebar.")
        else:
            st.info(f"Connecting to Gmail SMTP server... Dispatching to {len(valid_recipients)} recipient(s).")
            
            prog_bar = st.progress(0)
            status_box = st.empty()
            log_container = st.container()

            sent_ok = 0
            fail_cnt = 0

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(sender_email, sender_password)

                for idx, recipient in enumerate(valid_recipients, start=1):
                    status_box.markdown(f"⏳ **[{idx}/{len(valid_recipients)}]** Dispatching email to `{recipient}`...")
                    
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = recipient
                        msg['Subject'] = subject_line
                        msg.attach(MIMEText(email_body, 'plain'))

                        with open(pdf_path_to_use, 'rb') as attachment:
                            pdf_attachment = MIMEBase('application', 'octet-stream')
                            pdf_attachment.set_payload(attachment.read())
                        encoders.encode_base64(pdf_attachment)
                        pdf_attachment.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(pdf_path_to_use)}'
                        )
                        msg.attach(pdf_attachment)

                        server.sendmail(sender_email, recipient, msg.as_string())
                        sent_ok += 1
                        log_container.success(f"✅ Email delivered to: `{recipient}`")
                    except Exception as err:
                        fail_cnt += 1
                        log_container.error(f"❌ Failed to deliver to `{recipient}`: {err}")

                    prog_bar.progress(idx / len(valid_recipients))
                    if idx < len(valid_recipients):
                        time.sleep(delay_sec)

                server.quit()
                status_box.empty()
                st.balloons()
                st.success(f"🎉 **Campaign Finished!** Sent: **{sent_ok}** | Failed: **{fail_cnt}**")

            except Exception as login_err:
                st.error(f"❌ Gmail Connection/Authentication Error: {login_err}")


# ============================================================
# 💬 TAB 2: WHATSAPP WEB AUTOMATION ENGINE
# ============================================================
with tab_whatsapp:
    st.markdown('<div class="header-3d">💬 Automated WhatsApp Web Engine</div>', unsafe_allow_html=True)
    col_wa1, col_wa2 = st.columns([1, 1])

    with col_wa1:
        phone_input = st.text_area(
            "Target Phone Numbers (With Country Code e.g. +919998244418)",
            value=st.session_state.get("target_phones", "+919998244418"),
            height=140
        )
        st.session_state["target_phones"] = phone_input


        raw_phones = re.split(r'[,\n\s]+', phone_input)
        formatted_phones = []
        for p in raw_phones:
            p_clean = p.strip()
            if p_clean:
                if not p_clean.startswith("+"):
                    p_clean = "+" + p_clean
                formatted_phones.append(p_clean)

        st.markdown(f'<span class="badge-3d-cyan">📲 Target Contacts: {len(formatted_phones)}</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        wa_load_delay = st.slider("WhatsApp Web Page Load Timeout (Seconds)", min_value=5, max_value=30, value=12)
        wa_pause_delay = st.slider("Pause Between Phone Numbers (Seconds)", min_value=2, max_value=20, value=5)

    with col_wa2:
        default_wa_body = """Dear Hiring Manager,

I hope you are doing well. My name is Dhruv Parikh, and I am writing to express my interest in the *Python Django Developer* position.

I have 3 years of experience in developing web applications using Python and Django, along with expertise in creating RESTful APIs, managing PostgreSQL databases, and integrating front-end technologies like HTML, CSS, and JavaScript. I am passionate about building efficient and scalable solutions and would be excited to contribute to your team.

Please let me know if you need any additional information or documents. I look forward to the opportunity to discuss how my skills and experience align with your requirements.

Thank you for your time and consideration.

Best regards,
*Dhruv Parikh*
📞 +91 7600524348
📧 parikhdhruv05@gmail.com"""

        wa_body = st.text_area("Message Content", value=default_wa_body, height=240)
        
        if st.button("📋 Copy Message Text to Clipboard"):
            copy_text_to_clipboard(wa_body)
            st.success("✅ Message text copied to clipboard!")

    st.markdown("---")

    if st.button("⚡ EXECUTE SPATIAL 3D WHATSAPP AUTOMATION", type="primary", **get_width_arg(True)):
        if not formatted_phones:
            st.error("❌ Please provide at least one target WhatsApp phone number.")
        elif not os.path.exists(pdf_path_to_use):
            st.error(f"❌ PDF Resume file missing at: `{pdf_path_to_use}`")
        else:
            st.info(f"🚀 Initializing WhatsApp Web Automation for {len(formatted_phones)} target number(s)...")
            wa_prog = st.progress(0)
            wa_status = st.empty()

            for idx, phone in enumerate(formatted_phones, start=1):
                wa_status.markdown(f"⏳ **[{idx}/{len(formatted_phones)}]** Opening WhatsApp Web chat for `{phone}`...")

                try:
                    whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}"
                    webbrowser.open(whatsapp_url)

                    wa_status.markdown(f"⏳ Waiting {wa_load_delay}s for WhatsApp Web chat page to load...")
                    time.sleep(wa_load_delay)

                    copied_file, file_err = copy_file_to_clipboard(pdf_path_to_use)
                    if not copied_file:
                        st.error(f"❌ Failed copying PDF to clipboard for `{phone}`: {file_err}")
                        continue

                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(3)

                    copy_text_to_clipboard(wa_body)
                    time.sleep(0.5)

                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(1.5)

                    pyautogui.press('enter')
                    time.sleep(1)

                    st.success(f"✅ Automatically attached PDF and sent message to `{phone}`")

                except Exception as err:
                    st.error(f"❌ Error processing `{phone}`: {err}")

                wa_prog.progress(idx / len(formatted_phones))
                if idx < len(formatted_phones):
                    time.sleep(wa_pause_delay)

            wa_status.empty()
            st.balloons()
            st.success("🎉 **WhatsApp Automation Completed!**")

    if formatted_phones:
        st.markdown("---")
        st.markdown("### 💬 Direct 1-Click WhatsApp Web Chat Launcher")
        cols_wa_grid = st.columns(min(len(formatted_phones), 3))
        for idx, phone in enumerate(formatted_phones):
            col_idx = idx % min(len(formatted_phones), 3)
            encoded_text = urllib.parse.quote(wa_body)
            chat_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_text}"
            cols_wa_grid[col_idx].markdown(
                f'<a href="{chat_url}" target="_blank" style="text-decoration:none;">'
                f'<div class="card-3d" style="text-align:center; padding:12px; margin-bottom:10px; border-color:rgba(56,189,248,0.4);">'
                f'<span style="color:#38BDF8; font-weight:700;">💬 Open WhatsApp Chat ({phone})</span>'
                f'</div></a>',
                unsafe_allow_html=True
            )



# ============================================================
# 🔎 TAB 3: LINKEDIN JOB FINDER ENGINE (job_find_2.py)
# ============================================================
with tab_scraper:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.95); border: 2px solid rgba(168, 85, 247, 0.45); border-radius: 24px; padding: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.6); margin-bottom: 25px;">
        <div class="header-3d" style="font-size: 1.5rem; margin-bottom: 15px;">📦 LinkedIn Job Search Engine Frame Box</div>
        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 20px;">All LinkedIn search, post extraction, contact parsing, and live logging run inside this unified frame box in background mode without opening external tabs.</p>
    """, unsafe_allow_html=True)

    col_sc1, col_sc2 = st.columns([1.1, 0.9])

    with col_sc1:
        st.markdown("### ⚙️ Search Configuration")
        sc_query = st.text_input(
            "Job Search Query",
            value="python developer 3 years experience and Ahmedabad"
        )

        col_cred1, col_cred2 = st.columns(2)
        with col_cred1:
            li_email = st.text_input("LinkedIn Email", value="parikhdhruv05@gmail.com")
        with col_cred2:
            li_pass = st.text_input("LinkedIn Password", value="dhruvparikh@1234", type="password")

        max_posts_input = st.slider("Max Posts to Scrape", min_value=10, max_value=200, value=50, step=10)
        headless_mode = st.checkbox("Run in Background Mode (No external browser tab/window opened)", value=True)


    with col_sc2:
        st.markdown("### 📊 Extracted Summary & Actions")

        current_scraped = st.session_state.get("scraped_data", [])

        extracted_emails = []
        extracted_phones = []
        extracted_links = []

        for item in current_scraped:
            if item.get("email"):
                for e in item["email"].split(","):
                    if e.strip() and e.strip() not in extracted_emails:
                        extracted_emails.append(e.strip())
            if item.get("mobile"):
                for p in item["mobile"].split(","):
                    if p.strip() and p.strip() not in extracted_phones:
                        extracted_phones.append(p.strip())
            if item.get("apply_link"):
                for l in item["apply_link"].split(","):
                    if l.strip() and l.strip() not in extracted_links:
                        extracted_links.append(l.strip())

        c_sc1, c_sc2, c_sc3, c_sc4 = st.columns(4)
        c_sc1.metric("Posts", len(current_scraped))
        c_sc2.metric("Emails", len(extracted_emails))
        c_sc3.metric("Mobiles", len(extracted_phones))
        c_sc4.metric("Apply Links", len(extracted_links))

        st.markdown("<br>", unsafe_allow_html=True)

        if extracted_emails:
            if st.button(f"✉️ Push {len(extracted_emails)} Extracted Emails to Email Studio", **get_width_arg(True)):
                existing = [e.strip() for e in st.session_state.get("target_emails", "").split(",") if e.strip()]
                combined = list(dict.fromkeys(existing + extracted_emails))
                st.session_state["target_emails"] = ", ".join(combined)
                st.success(f"✅ Added {len(extracted_emails)} emails to Email Dispatch Studio!")

        if extracted_phones:
            if st.button(f"💬 Push {len(extracted_phones)} Extracted Numbers to WhatsApp Engine", **get_width_arg(True)):
                existing = [p.strip() for p in st.session_state.get("target_phones", "").split(",") if p.strip()]
                combined = list(dict.fromkeys(existing + extracted_phones))
                st.session_state["target_phones"] = ", ".join(combined)
                st.success(f"✅ Added {len(extracted_phones)} numbers to WhatsApp Web Engine!")

    st.markdown("---")

    # Persistent Live Browser View Container
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.5); border-radius: 18px; padding: 18px; margin-bottom: 20px; box-shadow: inset 0 0 15px rgba(56, 189, 248, 0.1);">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.15rem; font-weight: 700; color: #38BDF8; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
            📺 LIVE EMBEDDED LINKEDIN BROWSER BOX (Live Scraper Window)
        </div>
        <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 12px;">Watch live real-time screen updates of LinkedIn login, job search navigation, filtering, and post scraping inside this frame box.</p>
    """, unsafe_allow_html=True)
    sc_preview = st.empty()
    if st.session_state.get("last_browser_screenshot"):
        sc_preview.image(
            st.session_state["last_browser_screenshot"],
            caption="🌐 Last Captured LinkedIn Browser Frame Box",
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 LAUNCH LINKEDIN JOB SCRAPER", type="primary", **get_width_arg(True)):
        if not sc_query.strip():
            st.error("❌ Please specify a job search query.")
        elif not li_email or not li_pass:
            st.error("❌ Please provide LinkedIn credentials.")
        else:
            st.info(f"Initializing Selenium ChromeDriver and starting scrape for '{sc_query}'...")
            sc_status = st.empty()
            sc_prog = st.progress(0)
            sc_logs = st.empty()

            try:
                posts_data, txt_file, json_file, xlsx_file = run_linkedin_job_scraper(
                    query=sc_query,
                    email=li_email,
                    password=li_pass,
                    max_posts=max_posts_input,
                    headless=headless_mode,
                    status_box=sc_status,
                    prog_bar=sc_prog,
                    log_container=sc_logs,
                    preview_container=sc_preview
                )

                st.session_state["scraped_data"] = posts_data

                st.session_state["last_xlsx"] = xlsx_file
                st.session_state["last_json"] = json_file
                st.session_state["last_txt"] = txt_file

                sc_status.empty()
                st.balloons()
                st.success(f"🎉 **Scraping Complete!** Collected **{len(posts_data)}** posts.")
                st.rerun()
            except Exception as err:
                st.error(f"❌ Scraper error: {err}")

    # Display Scraped Data Table
    current_data = st.session_state.get("scraped_data", [])
    if current_data:
        st.markdown("---")
        st.markdown('<div class="header-3d">📋 Scraped Job Posts & Extracted Contacts</div>', unsafe_allow_html=True)

        df_display = pd.DataFrame(current_data)

        search_filter = st.text_input("🔍 Filter Scraped Posts by Keyword / Skill / Role", "")
        if search_filter:
            df_filtered = df_display[df_display.astype(str).apply(lambda x: x.str.contains(search_filter, case=False)).any(axis=1)]
            st.dataframe(df_filtered, **get_width_arg(True))
        else:
            st.dataframe(df_display, **get_width_arg(True))

        col_d1, col_d2, col_d3 = st.columns(3)

        last_xlsx = st.session_state.get("last_xlsx")
        last_json = st.session_state.get("last_json")
        last_txt = st.session_state.get("last_txt")

        if last_xlsx and os.path.exists(last_xlsx):
            with open(last_xlsx, "rb") as f:
                col_d1.download_button(
                    "📥 Download Excel (.xlsx)",
                    data=f.read(),
                    file_name=os.path.basename(last_xlsx),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        if last_json and os.path.exists(last_json):
            with open(last_json, "rb") as f:
                col_d2.download_button(
                    "📥 Download JSON (.json)",
                    data=f.read(),
                    file_name=os.path.basename(last_json),
                    mime="application/json"
                )
        if last_txt and os.path.exists(last_txt):
            with open(last_txt, "rb") as f:
                col_d3.download_button(
                    "📥 Download Text (.txt)",
                    data=f.read(),
                    file_name=os.path.basename(last_txt),
                    mime="text/plain"
                )

    # Saved Scraped Output Browser
    st.markdown("---")
    with st.expander("📁 Browse Historical Scraped Datasets"):
        saved_outputs = get_saved_linkedin_outputs()
        if saved_outputs:
            selected_output = st.selectbox("Select Historical LinkedIn Dataset", saved_outputs)
            if selected_output:
                if selected_output.endswith(".json"):
                    with open(selected_output, "r", encoding="utf-8") as f:
                        hist_data = json.load(f)
                    st.dataframe(pd.DataFrame(hist_data), **get_width_arg(True))
                    if st.button("🔄 Load Dataset as Active Data in App"):
                        st.session_state["scraped_data"] = hist_data
                        st.success("Loaded dataset into active session!")
                        st.rerun()
                elif selected_output.endswith(".xlsx"):
                    hist_df = pd.read_excel(selected_output)
                    st.dataframe(hist_df, **get_width_arg(True))
        else:
            st.info("No historical LinkedIn datasets found in `linkedin_posts_output/`.")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# 📊 TAB 4: LOGS & ANALYTICS
# ============================================================

with tab_logs:
    st.markdown('<div class="header-3d">📊 Historic Application Analytics & Logs</div>', unsafe_allow_html=True)


    log_files = get_saved_logs()

    if log_files:
        selected_log = st.selectbox("Select Log File", log_files)
        if selected_log:
            try:
                df = pd.read_json(selected_log)
                
                t_count = len(df)
                s_count = len(df[df['status'] == 'Sent']) if 'status' in df.columns else t_count
                f_count = t_count - s_count

                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric("Total Records", t_count)
                col_m2.metric("Successfully Sent", s_count, delta=f"{round((s_count/t_count)*100, 1)}%" if t_count > 0 else "0%")
                col_m3.metric("Failed Attempts", f_count)

                st.markdown("---")
                
                search_query = st.text_input("🔍 Search Logs by Email / Keyword", "")
                if search_query:
                    df_filtered = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
                    st.dataframe(df_filtered, **get_width_arg(True))
                else:
                    st.dataframe(df, **get_width_arg(True))

                st.markdown("<br>", unsafe_allow_html=True)
                
                csv_bytes = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Log Report (CSV)",
                    data=csv_bytes,
                    file_name=f"Spatial3D_Log_{os.path.basename(selected_log)}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error loading log file: {e}")
    else:
        st.info("ℹ️ No historical log JSON files found in `email_logs/` folder yet.")
