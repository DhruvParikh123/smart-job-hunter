import sys
import os
import re
import time
from datetime import datetime

# Fix UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# PDF Generation imports
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# AI imports (Optional support)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# ============================================================
# CANDIDATE DEFAULT BASE DATA (DHRUV PARIKH)
# ============================================================
DEFAULT_CANDIDATE = {
    "name": "Dhruv Parikh",
    "title": "Python Django Developer",
    "experience_years": "3.0",
    "email": "parikhdhruv05@gmail.com",
    "phone": "+91 7600524348",
    "location": "Ahmedabad, Gujarat, India",
    "linkedin": "https://www.linkedin.com/in/parikh-dhruv-4089b9215/",
    "github": "https://github.com/DhruvParikh123",
    
    "summary": (
        "Results-driven Python Django Developer with 3.0 years of experience designing, "
        "developing, and deploying scalable web applications, RESTful APIs, and AI-assisted automation systems. "
        "Proficient in Python, Django REST Framework, PostgreSQL, MySQL, and modern front-end technologies. "
        "Proven track record of delivering robust back-end solutions and real-time computer vision applications."
    ),

    "skills": {
        "Languages & Frameworks": "Python, Django, Django REST Framework (DRF), Flask, Fast API",
        "Databases & Tools": "PostgreSQL, MySQL, Redis, Git, GitHub, Docker, Postman",
        "Web & APIs": "RESTful API Development, OAuth2, WebSockets, HTML5, CSS3, JavaScript, Bootstrap",
        "AI & Automation": "OpenCV, YOLOv8, PyWhatKit, Selenium, Automation Scripts, Data Scraping"
    },

    "experience": [
        {
            "role": "Python / Django Developer",
            "company": "Hexagon Infosoft",
            "period": "3.0 Years (Present)",
            "location": "Ahmedabad, India",
            "bullets": [
                "Developed scalable back-end services and RESTful APIs using Python, Django, and Django REST Framework.",
                "Engineered Visitor Management System (VMS) SaaS platform with secure authentication, role-based permissions, and automated notifications.",
                "Implemented AI & Computer Vision modules using OpenCV and YOLOv8 for face recognition and real-time safety detection.",
                "Optimized database queries and schema designs in PostgreSQL and MySQL, improving API response times by 30%.",
                "Automated email and messaging workflows using Python scripts and background schedulers for automated job & communication outreach."
            ]
        }
    ],

    "projects": [
        {
            "title": "Visitor Management System (VMS SaaS Platform)",
            "tech": "Python, Django REST Framework, PostgreSQL, SSL Security",
            "description": "Architected multi-tenant VMS platform enabling seamless visitor check-in, host notification, and badge generation with full SSL certificate integration."
        },
        {
            "title": "Automated Communication & Job Outreach System",
            "tech": "Python, SMTP Email, WhatsApp API, PyWhatKit, JSON Processing",
            "description": "Built automated job applicant matching and multi-channel outreach engine to parse employer leads and send tailored email and WhatsApp notifications."
        },
        {
            "title": "AI Computer Vision & PPE Detection",
            "tech": "Python, OpenCV, YOLOv8, Real-Time Video Stream Processing",
            "description": "Designed real-time safety equipment monitoring system processing live video streams to identify workplace compliance."
        }
    ],

    "education": [
        {
            "degree": "Bachelor of Engineering (B.E.) in Computer Engineering",
            "institution": "Gujarat Technological University (GTU)",
            "year": "Completed"
        }
    ]
}


# ============================================================
# STRICT EXPERIENCE ENFORCEMENT FUNCTION
# ============================================================
def enforce_strict_3_year_exp(text: str) -> str:
    """
    Scans any generated resume text or summary and strictly forces any experience 
    mentions to state '3.0 years' or '3.0 Years'.
    """
    if not text:
        return ""
    
    # Replace any year numbers like "3.5 years", "4 years", "2 years", etc. with "3.0 years"
    pattern = r'\b(\d+(\.\d+)?)\+?\s*(years?|yrs?)\b'
    
    def replacer(match):
        unit = match.group(3)
        return f"3.0 {unit}"

    cleaned_text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
    
    # Also explicitly ensure no text says anything other than 3.0 years
    cleaned_text = re.sub(r'3\.\d+\s*years?', '3.0 years', cleaned_text, flags=re.IGNORECASE)
    return cleaned_text


# ============================================================
# AI / SMART RESUME TAILORING ENGINE
# ============================================================
def tailor_resume_content(candidate_data: dict, job_description: str, gemini_api_key: str = None) -> dict:
    """
    Tailors candidate summary, skills, and bullet points to match the provided Job Description (JD).
    Always enforces strict 3.0 years of experience.
    """
    tailored = dict(candidate_data)
    
    # Check if Gemini API Key is available
    api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
    
    if GEMINI_AVAILABLE and api_key:
        try:
            print("[AI] Customizing resume content using Gemini AI...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
You are an expert resume optimizer and career coach.
Tailor the following candidate profile specifically for the target Job Description below.

CRITICAL MANDATORY INSTRUCTION:
- Total experience MUST BE STRICTLY 3.0 YEARS. Do NOT mention any experience other than 3.0 years.

CANDIDATE BASE PROFILE:
Name: {candidate_data['name']}
Target Title: {candidate_data['title']}
Current Summary: {candidate_data['summary']}
Skills: {candidate_data['skills']}

TARGET JOB DESCRIPTION:
{job_description}

Please output a tailored professional summary (3-4 sentences max) that highlights skills matching the JD.
Make sure to emphasize Python, Django, REST APIs, and matching keywords from the JD.
Make sure the summary explicitly mentions "3.0 years of experience".

Return ONLY the tailored summary text.
"""
            response = model.generate_content(prompt)
            if response and response.text:
                tailored['summary'] = enforce_strict_3_year_exp(response.text.strip())
                print("[SUCCESS] AI Customization Successful!")
        except Exception as e:
            print(f"[WARN] Gemini AI call failed ({e}). Falling back to Smart Rule-Based Customizer.")
            tailored['summary'] = fallback_tailor_summary(candidate_data['summary'], job_description)
    else:
        print("[INFO] Customizing resume content using Smart Keyword Tailoring...")
        tailored['summary'] = fallback_tailor_summary(candidate_data['summary'], job_description)
        
    # Ensure final summary strictly adheres to 3.0 years experience
    tailored['summary'] = enforce_strict_3_year_exp(tailored['summary'])
    return tailored



def fallback_tailor_summary(base_summary: str, job_description: str) -> str:
    """
    Extract key keywords from JD and optimize base summary without external API.
    """
    jd_lower = job_description.lower()
    highlighted_keywords = []
    
    keywords_to_check = [
        "django", "python", "rest api", "drf", "postgresql", "mysql", 
        "microservices", "docker", "redis", "celery", "aws", "git",
        "opencv", "yolo", "automation", "selenium", "javascript", "react"
    ]
    
    for kw in keywords_to_check:
        if kw in jd_lower:
            highlighted_keywords.append(kw.title() if len(kw) > 3 else kw.upper())
            
    if highlighted_keywords:
        top_kw = ", ".join(highlighted_keywords[:6])
        summary = (
            f"Results-oriented Python Django Developer with 3.0 years of experience specializing in {top_kw}. "
            f"Demonstrated success in building scalable back-end services, designing RESTful APIs, and implementing "
            f"efficient database solutions tailored to business requirements. Passionate about writing clean, maintainable code."
        )
    else:
        summary = base_summary
        
    return enforce_strict_3_year_exp(summary)


# ============================================================
# REPORTLAB PDF RESUME GENERATOR
# ============================================================
def generate_pdf_resume(candidate: dict, output_filename: str = "Dhruv_Parikh_Tailored_Resume.pdf") -> str:
    """
    Generates a beautifully styled, ATS-friendly PDF resume using ReportLab.
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("ReportLab is not installed. Please install it using 'pip install reportlab'.")
        
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY_COLOR = colors.HexColor("#1A365D")   # Deep Navy
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") # Slate Blue
    TEXT_COLOR = colors.HexColor("#2D3748")      # Charcoal
    LINE_COLOR = colors.HexColor("#CBD5E0")      # Soft Gray
    
    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY_COLOR,
        alignment=TA_CENTER
    )

    contact_style = ParagraphStyle(
        'ContactInfo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_COLOR,
        alignment=TA_CENTER
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_COLOR,
        alignment=TA_JUSTIFY,
        spaceAfter=4
    )

    bold_body_style = ParagraphStyle(
        'BoldBodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_COLOR,
        spaceAfter=2
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_COLOR,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    elements = []

    # ----------------------------------------------------
    # HEADER SECTION
    # ----------------------------------------------------
    elements.append(Paragraph(candidate['name'].upper(), title_style))
    elements.append(Spacer(1, 3))
    
    # Title with Experience
    title_exp_str = f"{candidate['title']} (Experience: {candidate['experience_years']} Years)"
    elements.append(Paragraph(title_exp_str, subtitle_style))
    elements.append(Spacer(1, 4))
    
    # Contact Info Line
    contact_line = f"📧 {candidate['email']}  |  📞 {candidate['phone']}  |  📍 {candidate['location']}"
    elements.append(Paragraph(contact_line, contact_style))
    
    links_line = f"LinkedIn: {candidate['linkedin']}  |  GitHub: {candidate['github']}"
    elements.append(Paragraph(links_line, contact_style))
    elements.append(Spacer(1, 8))
    
    # Divider
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceBefore=2, spaceAfter=8))

    # ----------------------------------------------------
    # PROFESSIONAL SUMMARY
    # ----------------------------------------------------
    elements.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR, spaceBefore=1, spaceAfter=4))
    
    summary_text = enforce_strict_3_year_exp(candidate['summary'])
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 6))

    # ----------------------------------------------------
    # TECHNICAL SKILLS
    # ----------------------------------------------------
    elements.append(Paragraph("TECHNICAL SKILLS", section_heading))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR, spaceBefore=1, spaceAfter=4))
    
    for category, skill_list in candidate['skills'].items():
        skill_para = f"<b>• {category}:</b> {skill_list}"
        elements.append(Paragraph(skill_para, body_style))
    elements.append(Spacer(1, 6))

    # ----------------------------------------------------
    # WORK EXPERIENCE
    # ----------------------------------------------------
    elements.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR, spaceBefore=1, spaceAfter=4))

    for exp in candidate['experience']:
        # Header table for Role & Date
        role_company = f"<b>{exp['role']}</b> – <i>{exp['company']}</i>"
        period_loc = f"<b>{exp['period']}</b> | {exp['location']}"
        
        header_table_data = [
            [Paragraph(role_company, bold_body_style), Paragraph(period_loc, ParagraphStyle('RightAlign', parent=bold_body_style, alignment=TA_RIGHT))]
        ]
        
        t = Table(header_table_data, colWidths=[360, 180])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        elements.append(t)
        
        for bullet in exp['bullets']:
            b_text = enforce_strict_3_year_exp(bullet)
            elements.append(Paragraph(f"• {b_text}", bullet_style))
        elements.append(Spacer(1, 4))

    elements.append(Spacer(1, 4))

    # ----------------------------------------------------
    # KEY PROJECTS
    # ----------------------------------------------------
    elements.append(Paragraph("KEY PROJECTS", section_heading))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR, spaceBefore=1, spaceAfter=4))

    for proj in candidate['projects']:
        proj_title_line = f"<b>{proj['title']}</b> (<i>{proj['tech']}</i>)"
        elements.append(Paragraph(proj_title_line, bold_body_style))
        elements.append(Paragraph(f"• {proj['description']}", bullet_style))
        elements.append(Spacer(1, 3))

    elements.append(Spacer(1, 4))

    # ----------------------------------------------------
    # EDUCATION
    # ----------------------------------------------------
    elements.append(Paragraph("EDUCATION", section_heading))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR, spaceBefore=1, spaceAfter=4))

    for edu in candidate['education']:
        edu_str = f"<b>{edu['degree']}</b> – {edu['institution']} ({edu['year']})"
        elements.append(Paragraph(edu_str, body_style))

    # Build Document
    doc.build(elements)
    print(f"[PDF] PDF Resume Generated Successfully: {output_filename}")
    return output_filename



# ============================================================
# MAIN INTERACTIVE / SCRIPT ENTRY POINT
# ============================================================
def main():
    print("=" * 60)
    print("[+] TAILORED AI RESUME GENERATOR (Strict 3.0 Years Experience)")
    print("=" * 60)
    
    # 1. Output directory
    output_dir = "tailored_resumes"
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. Get Job Description from CLI arguments, input file, or prompt
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        print(f"[FILE] Reading Job Description from file: {sys.argv[1]}")
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            job_description = f.read()
    else:
        print("\n[INFO] Sample Job Description loaded for Python Django Developer.")
        job_description = """
Position: Python Django Developer
Requirements:
✅ Strong Python development experience
 ✅ AI/ML & GenAI knowledge
 ✅ Experience with FastAPI / Flask & REST APIs
 ✅ Experience with AI/ML frameworks
 ✅ Knowledge of AWS / GCP / Azure is a plus
 ✅ Strong problem-solving & analytical skills
"""
    
    print("\n--- JOB DESCRIPTION ---")
    print(job_description.strip())
    print("------------------------\n")
    
    # 3. Tailor Candidate Data
    tailored_candidate = tailor_resume_content(DEFAULT_CANDIDATE, job_description)
    
    # 4. Generate Output Filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"Dhruv_Parikh_Tailored_Resume_{timestamp}.pdf")
    
    # 5. Build PDF
    pdf_path = generate_pdf_resume(tailored_candidate, output_filename)
    
    print("\n" + "=" * 60)
    print(f"[SUCCESS] PROCESS COMPLETE!")
    print(f"[OUTPUT] New Resume PDF: {os.path.abspath(pdf_path)}")
    print(f"[EXPERIENCE] Experience Shown: {tailored_candidate['experience_years']} Years (Strict)")
    print("=" * 60)



if __name__ == "__main__":
    main()
