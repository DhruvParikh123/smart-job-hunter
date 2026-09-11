from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
import os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

email = "parikhdhruv05@gmail.com"
password = "dhruvparikh@1234"


# ============================================================
# 🆕 DATE-WISE OUTPUT FOLDER SETUP
# ============================================================

# Folder name based on today's date, e.g. "2026-06-15"
today_str = datetime.now().strftime("%Y-%m-%d")

# Base folder where all date folders will be created
BASE_OUTPUT_DIR = "linkedin_posts_output"

# Final folder path -> linkedin_posts_output/2026-06-15
OUTPUT_DIR = os.path.join(BASE_OUTPUT_DIR, today_str)

# Create folder if it doesn't exist (creates nested folders too)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"📁 Output folder ready: {OUTPUT_DIR}")


# ============================================================
# BOLD UNICODE NORMALIZATION
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


# ============================================================
# EXTRACTION FUNCTIONS
# ============================================================

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
        "email": extract_emails(text),
        "mobile": extract_phone_numbers(text),
        "position": extract_position(text),
        "location": extract_location(text),
        "experience": extract_experience(text),
    }


# ============================================================
# POSTER NAME / DATE / IMAGE EXTRACTION
# ============================================================

def get_poster_name_date_image(post_element, driver):
    """
    Returns (poster_name, post_date, image_url)
    Works with the newer LinkedIn feed structure shown in the
    'd368900e ... a1b81b9c' container HTML.
    """
    poster_name = ""
    post_date = ""
    image_url = ""

    # ---- find the parent feed-update container ----
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

    # ---- Poster Name ----
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

    if not poster_name:
        try:
            els = parent.find_elements(
                By.XPATH,
                ".//div[contains(@aria-label,'Verified Profile')]//span"
            )
            for el in els:
                t = el.text.strip()
                if t and "•" not in t:
                    poster_name = t
                    break
        except Exception:
            pass

    if not poster_name:
        try:
            img_alt_el = parent.find_element(
                By.XPATH, ".//*[@aria-label[contains(.,\"profile\")]]"
            )
            alt = img_alt_el.get_attribute("aria-label") or ""
            m = re.search(r"View (.+?)['’]s profile", alt)
            if m:
                poster_name = m.group(1).strip()
        except Exception:
            pass

    # ---- Post Date ----
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

    if not post_date:
        try:
            spans = parent.find_elements(By.XPATH, ".//p//span")
            for sp in spans:
                t = sp.text.strip()
                if re.match(r'^\d+[smhdw]\s*•', t) or re.match(r'^\d+\s*(min|hr|day|week|month)s?\s*•', t, re.IGNORECASE):
                    post_date = t.split("•")[0].strip()
                    break
        except Exception:
            pass

    # ---- Post Image (if any) ----
    img_selectors = [
        "div.update-components-image img",
        ".feed-shared-image__container img",
        "div.update-components-article img",
        "li.update-components-image img",
    ]
    for sel in img_selectors:
        try:
            el = parent.find_element(By.CSS_SELECTOR, sel)
            src = el.get_attribute("src")
            if src and "media.licdn.com" in src:
                image_url = src
                break
        except Exception:
            continue

    if not image_url:
        try:
            imgs = parent.find_elements(By.TAG_NAME, "img")
            for img in imgs:
                src = img.get_attribute("src") or ""
                alt = (img.get_attribute("alt") or "").lower()
                if "media.licdn.com" in src and "profile" not in alt:
                    image_url = src
                    break
        except Exception:
            pass

    return poster_name, post_date, image_url


# ============================================================
# SEE MORE / SCROLL FUNCTIONS
# ============================================================

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
                        time.sleep(0.3)
                        driver.execute_script("arguments[0].click();", btn)
                        clicked += 1
                        time.sleep(0.2)
                except Exception:
                    continue

        xpath_buttons = driver.find_elements(
            By.XPATH,
            "//button[contains(@class,'expandable-text-button')]"
            " | //span[contains(text(),'more')][@role='button']"
            " | //button[@data-testid='expandable-text-button']"
        )
        for btn in xpath_buttons:
            try:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", btn)
                    clicked += 1
                    time.sleep(0.2)
            except Exception:
                continue
    except Exception as e:
        print(f"  ⚠️ See more click error: {e}")

    if clicked > 0:
        print(f"  🔓 {clicked} 'see more' buttons clicked")
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
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.5)
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


def scroll_and_collect_posts(driver, max_posts=100, max_no_change=5):
    all_posts = []
    all_posts_data = []
    seen_texts = set()
    no_change_count = 0
    last_post_count = 0

    print("🔍 Starting post collection with proper scroll...\n")

    while True:
        print("  🔄 Expanding all truncated posts...")
        click_all_see_more_buttons(driver)
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
                        "post_number": len(all_posts),
                        "poster_name": poster_name,
                        "post_date": post_date,
                        "position": info["position"],
                        "experience": info["experience"],
                        "location": info["location"],
                        "email": info["email"],
                        "mobile": info["mobile"],
                        "image_url": image_url,
                        "full_text": full_text,
                    }
                    all_posts_data.append(post_data)

                    print(f"  ✅ Post #{len(all_posts)}: {full_text[:80]}...")
                    print(f"     👤 {poster_name} | 🕒 {post_date} | 💼 {info['experience']} | 📧 {info['email']} | 📱 {info['mobile']} | 🖼️ {'Yes' if image_url else 'No'}")
            except Exception:
                continue

        print(f"\n📊 Total posts collected: {len(all_posts)}")

        if len(all_posts) >= max_posts:
            print(f"✅ Reached max posts limit: {max_posts}")
            break

        if len(all_posts) == last_post_count:
            no_change_count += 1
            print(f"⚠️  No new posts (attempt {no_change_count}/{max_no_change})")
            if no_change_count >= max_no_change:
                print("✅ No more posts to load. Stopping.")
                break
        else:
            no_change_count = 0

        last_post_count = len(all_posts)

        if post_elements:
            try:
                last_post = post_elements[-1]
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", last_post
                )
                time.sleep(2)
            except Exception:
                pass

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        driver.execute_script("window.scrollBy(0, -400);")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        print(f"📜 Scrolled | Loading new posts...")

    return all_posts, all_posts_data


# ============================================================
# EXCEL EXPORT (with clickable Image URL + embedded preview)
# ============================================================

def save_to_excel(all_posts_data, filename="linkedin_posts_3.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "LinkedIn Posts"

    headers = [
        "Post #", "Poster Name", "Post Date", "Position",
        "Experience", "Location", "Email", "Mobile Number",
        "Image URL", "Full Post Text"
    ]
    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for data in all_posts_data:
        row = [
            data["post_number"],
            data["poster_name"],
            data["post_date"],
            data["position"],
            data["experience"],
            data["location"],
            data["email"],
            data["mobile"],
            data["image_url"],
            data["full_text"],
        ]
        ws.append(row)

        if data["image_url"]:
            cell = ws.cell(row=ws.max_row, column=9)
            cell.hyperlink = data["image_url"]
            cell.style = "Hyperlink"

    col_widths = [8, 25, 15, 35, 15, 25, 35, 20, 50, 80]
    for i, width in enumerate(col_widths, 1):
        ws.column_dimensions[chr(64 + i)].width = width

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    wb.save(filename)
    print(f"📊 Excel file saved: {filename}")


# ============================================================
# MAIN SCRIPT
# ============================================================

try:
    driver.get("https://www.linkedin.com/jobs/")

    email_input = wait.until(EC.presence_of_element_located((By.ID, "session_key")))
    email_input.send_keys(email)

    password_input = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
    password_input.send_keys(password)

    sign_in_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    sign_in_btn.click()
    print("✅ Login successful")
    time.sleep(5)

    job_search = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='typeahead-input']"))
    )
    job_search.clear()
    job_search.send_keys("python developer 3 years experience and Ahmedabad")
    job_search.send_keys(Keys.ENTER)
    print("✅ Job search executed")
    time.sleep(5)

    jobs_dropdown = wait.until(
        EC.presence_of_element_located((By.XPATH, "//label[contains(.,'Jobs')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", jobs_dropdown)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", jobs_dropdown)
    print("✅ Jobs dropdown opened")
    time.sleep(2)

    posts_option = wait.until(
        EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='Posts']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", posts_option)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", posts_option)
    print("✅ Posts selected")
    time.sleep(2)

    sort_by = wait.until(
        EC.presence_of_element_located((By.XPATH, "//label[contains(.,'Sort by')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sort_by)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", sort_by)
    print("✅ Sort By opened")
    time.sleep(2)

    latest_option = wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Latest']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", latest_option)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", latest_option)
    print("✅ Latest selected")
    time.sleep(2)

    show_results = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Show results']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", show_results)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", show_results)
    print("✅ Show Results clicked")

    wait.until(EC.url_contains("/search/results/content/"))
    print("✅ Content results page loaded")
    print("Current URL:", driver.current_url)
    time.sleep(4)

    all_posts, all_posts_data = scroll_and_collect_posts(driver, max_posts=100, max_no_change=5)

    # 🆕 Build full file paths inside the date-wise folder, with date+time in filename
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    txt_path = os.path.join(OUTPUT_DIR, f"linkedin_posts_{timestamp_str}.txt")
    json_path = os.path.join(OUTPUT_DIR, f"linkedin_posts_{timestamp_str}.json")
    xlsx_path = os.path.join(OUTPUT_DIR, f"linkedin_posts_{timestamp_str}.xlsx")

    with open(txt_path, "w", encoding="utf-8") as f:
        for i, post in enumerate(all_posts, 1):
            f.write(f"{'=' * 60}\n")
            f.write(f"POST #{i}\n")
            f.write(f"{'=' * 60}\n")
            f.write(post + "\n\n")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_posts_data, f, ensure_ascii=False, indent=2)

    save_to_excel(all_posts_data, xlsx_path)

    print(f"\n🎉 Done! Total {len(all_posts)} posts saved.")
    print(f"📁 Folder: {OUTPUT_DIR}")
    print(f"📄 {txt_path}")
    print(f"📄 {json_path}")
    print(f"📊 {xlsx_path}")

    time.sleep(3)

except Exception as e:
    print("❌ Error:", e)
    import traceback
    traceback.print_exc()

finally:
    driver.quit()