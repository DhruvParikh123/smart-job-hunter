import os
import sys
import warnings
from datetime import datetime

# Suppress deprecation warnings
warnings.filterwarnings("ignore")

# Fix stdout encoding for Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ReportLab imports
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("[ERROR] ReportLab library is required. Please install via 'pip install reportlab'.")
    sys.exit(1)


# ============================================================
# CONFIGURATION & CONSTANTS
# ============================================================
ORIGINAL_RESUME_PATH = r'C:\Users\Admin\Downloads\Sending-Emails-With-Python-main\Sending-Emails-With-Python-main\Dhruv_Resume.pdf'

OUTPUT_PDF_NAME = "Dhruv_Parikh_Python_Django_Developer_Resume.pdf"
OUTPUT_DIR = "tailored_resumes"


# ============================================================
# TARGET JOB DESCRIPTION
# ============================================================
JOB_DESCRIPTION = """
Position: 𝐏𝐲𝐭𝐡𝐨𝐧 𝐀𝐈/𝐌𝐋 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫

Requirements:
Python • AI/ML • LLMs • Generative AI • RAG • AI Agents • LangChain • PyTorch/TensorFlow
"""


# ============================================================
# CANDIDATE RESUME DATA (TAILORED FOR PYTHON DJANGO DEVELOPER)
# ============================================================
RESUME_DATA = {
    "header": {
        "name": "DHRUV PARIKH",
        "title": "PYTHON DJANGO DEVELOPER",
        "experience": "3.0 Years of Experience",
        "email": "parikhdhruv05@gmail.com",
        "phone": "+91 7600524348",
        "location": "Ahmedabad, Gujarat",
        "linkedin": "https://www.linkedin.com/in/parikh-dhruv-4089b9215/"
    },
    
    "summary": (
        "Results-driven Python Django Developer with <b>3.0 years of experience</b> building scalable web applications, "
        "robust RESTful APIs, and backend services using <b>Python, Django, FastAPI, and Flask</b>. Strong expertise in database management "
        "(MySQL, PostgreSQL), microservices, and automated data pipelines. Hands-on experience with <b>AI/ML frameworks</b> (OpenCV, YOLOv8), "
        "computer vision systems, and practical <b>GenAI knowledge</b> (LLM API integrations & AI workflow automation). Familiar with cloud deployment "
        "concepts on <b>AWS</b>. Possesses strong problem-solving and analytical skills to design efficient, secure, and maintainable software solutions."
    ),

    "skills": [
        ("Programming Languages", "Python (Advanced), SQL, JavaScript, HTML5, CSS3, AJAX, Bootstrap"),
        ("Backend Frameworks", "Django (MVT, ORM, Admin), Django REST Framework (DRF), FastAPI, Flask"),
        ("API Development", "RESTful APIs, Serialization, Authentication, OAuth, JWT, Postman, WebSockets"),
        ("AI / ML & GenAI Knowledge", "OpenCV, YOLOv8, PPE Detection, Face Recognition, GenAI API Integrations, Prompt Engineering"),
        ("Database Management", "MySQL, PostgreSQL, SQLite, Redis"),
        ("Cloud & DevOps", "AWS (EC2, S3 concepts), Docker basics, Git, GitHub, GitLab"),
        ("Web Scraping & Automation", "BeautifulSoup, Scrapy, Selenium, PyWhatKit, Data Mining & Analysis")
    ],

    "experience": [
        {
            "role": "JUNIOR PYTHON DEVELOPER",
            "company": "Hexagon Infosoft",
            "location": "AHMEDABAD, GUJARAT",
            "period": "AUGUST 2023 – PRESENT (3.0 Years)",
            "bullets": [
                "Developed scalable web applications and back-end services using Python and Django following MVT architecture.",
                "Designed, built, and maintained RESTful APIs using Django REST Framework and FastAPI/Flask for seamless mobile and web integrations.",
                "Optimized database schemas, indexing, and CRUD operations in MySQL and PostgreSQL, significantly reducing query response latency.",
                "Implemented AI/ML-based computer vision solutions using OpenCV and YOLOv8 for real-time face recognition and attendance logging.",
                "Customized datasets and fine-tuned YOLOv8 models for PPE safety detection (helmets, masks, gloves, vests) in live camera streams.",
                "Explored and integrated GenAI / AI-assisted automation techniques to process unstructured data and automate workflow pipelines.",
                "Collaborated with front-end developers to integrate APIs, implement authentication (OAuth/JWT), and optimize user interfaces.",
                "Applied strong problem-solving and analytical skills to debug complex back-end issues and streamline software performance.",
                "Managed code repositories using Git, executing branch strategies, pull requests, and continuous code integration."
            ]
        }
    ],

    "projects": [
        {
            "name": "BWC Deals Website & REST API System",
            "environment": "Python, Django, Django REST Framework, FastAPI, MySQL, Firebase FCM",
            "bullets": [
                "Developed a scalable Django web application and Django REST Framework APIs for deal aggregation, affiliate marketing, and store management.",
                "Built microservice endpoints using FastAPI for fast data exchange and real-time deal comparison across multiple vendor platforms.",
                "Engineered admin panel with custom CRUD operations to manage deals, categories, stores, and website settings.",
                "Implemented automated data extraction scripts using BeautifulSoup & Selenium to gather deals data and generate structured CSV reports.",
                "Integrated Firebase Cloud Messaging (FCM) for targeted notifications and built user profile interaction features (likes, comments, saved deals)."
            ]
        },
        {
            "name": "Visitor Management System (VMS SaaS Platform)",
            "environment": "Python, Django, Django REST Framework, MySQL, PyWhatKit, SMTP",
            "bullets": [
                "Designed and implemented a digital VMS platform to manage visitor registration, appointment scheduling, and access control.",
                "Developed REST APIs using DRF for real-time communication between web and mobile frontend applications.",
                "Integrated automated notification modules sending instant email and WhatsApp alerts to hosts via Python SMTP and PyWhatKit.",
                "Implemented camera tracking integrations, visitor badge generation, and analytical reporting for facility management."
            ]
        },
        {
            "name": "Automated Attendance & AI PPE Detection System",
            "environment": "Python, OpenCV, YOLOv8, FastAPI, MySQL",
            "bullets": [
                "Developed an automated attendance marking system utilizing real-time face recognition with OpenCV and YOLOv8.",
                "Fine-tuned deep learning detection models for real-time PPE compliance tracking (helmets, gloves, masks, vests).",
                "Designed FastAPI micro-endpoints for instant attendance logging, camera feed ingestion, and verification matching.",
                "Structured MySQL database schema for storing face vectors, attendance records, and automated attendance reports."
            ]
        }
    ],

    "certifications": [
        "Advanced Python with DJANGO at Logic Rays Academy, Ahmedabad"
    ],

    "education": [
        {
            "institution": "SILVER OAK COLLEGE OF ENGINEERING AND TECHNOLOGY",
            "location": "AHMEDABAD, GUJARAT",
            "degree": "B.E. in Mechanical Engineering",
            "period": "Aug 2018 – May 2021"
        },
        {
            "institution": "C.U. SHAH UNIVERSITY",
            "location": "SURENDRANAGAR, GUJARAT",
            "degree": "Diploma in Mechanical Engineering",
            "period": "Aug 2015 – May 2018"
        }
    ]
}


# ============================================================
# REPORTLAB RESUME STYLES SETUP (MATCHING DHRUV_RESUME.PDF)
# ============================================================
def get_custom_resume_styles():
    styles = getSampleStyleSheet()

    # Exact palette from original resume
    COLOR_PRIMARY = colors.HexColor("#004880")     # Deep Blue (Title)
    COLOR_SECONDARY = colors.HexColor("#0070c0")   # Medium Blue (Subtitles/Links)
    COLOR_HEADING = colors.HexColor("#262626")     # Dark Charcoal (Section Headings)
    COLOR_TEXT = colors.HexColor("#404040")        # Medium Charcoal (Body Text)
    COLOR_LINE = colors.HexColor("#0070c0")        # Accent Line

    styles.add(ParagraphStyle(
        'HeaderTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=COLOR_PRIMARY,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'HeaderSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=COLOR_SECONDARY,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'HeaderContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=COLOR_SECONDARY,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12.5,
        leading=15,
        textColor=COLOR_HEADING,
        spaceBefore=10,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=COLOR_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        'BoldSubHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=COLOR_HEADING,
        spaceBefore=2,
        spaceAfter=2
    ))

    styles.add(ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12,
        textColor=COLOR_TEXT,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    ))

    return styles, COLOR_PRIMARY, COLOR_LINE


# ============================================================
# MODULAR SECTION BUILDERS
# ============================================================
def build_header(header_data: dict, styles: dict) -> list:
    elements = []
    elements.append(Paragraph(header_data['name'].upper(), styles['HeaderTitle']))
    elements.append(Spacer(1, 3))
    
    sub_title = f"{header_data['title']} ({header_data['experience']})"
    elements.append(Paragraph(sub_title, styles['HeaderSubTitle']))
    elements.append(Spacer(1, 3))
    
    contact_str = f"{header_data['email']}  ·  {header_data['phone']}  ·  {header_data['location']}"
    elements.append(Paragraph(contact_str, styles['HeaderContact']))
    
    linkedin_str = f"LinkedIn Profile: <font color='#0070c0'><u>{header_data['linkedin']}</u></font>"
    elements.append(Paragraph(linkedin_str, styles['HeaderContact']))
    elements.append(Spacer(1, 6))
    
    elements.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#0070c0"), spaceBefore=2, spaceAfter=8))
    return elements


def build_summary(summary_text: str, styles: dict, line_color) -> list:
    elements = []
    elements.append(Paragraph("PROFESSIONAL SUMMARY", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceBefore=1, spaceAfter=4))
    elements.append(Paragraph(summary_text, styles['BodyCustom']))
    elements.append(Spacer(1, 4))
    return elements


def build_skills(skills_data: list, styles: dict, line_color) -> list:
    elements = []
    elements.append(Paragraph("SKILLS", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceBefore=1, spaceAfter=4))
    
    for category, skill_str in skills_data:
        skill_para = f"• <b>{category}:</b> {skill_str}"
        elements.append(Paragraph(skill_para, styles['BodyCustom']))
    elements.append(Spacer(1, 4))
    return elements


def build_experience(exp_data: list, styles: dict, line_color) -> list:
    elements = []
    elements.append(Paragraph("EXPERIENCE", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceBefore=1, spaceAfter=4))

    for exp in exp_data:
        head_para = f"<b>{exp['role']}</b>, {exp['company']} | {exp['location']}"
        date_para = f"<b>{exp['period']}</b>"
        
        t = Table(
            [[Paragraph(head_para, styles['BoldSubHeader']), Paragraph(date_para, ParagraphStyle('RightDate', parent=styles['BoldSubHeader'], alignment=TA_RIGHT))]],
            colWidths=[380, 160]
        )
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        elements.append(t)
        
        for bullet in exp['bullets']:
            elements.append(Paragraph(f"• {bullet}", styles['BulletCustom']))
        elements.append(Spacer(1, 4))

    return elements


def build_projects(projects_data: list, styles: dict, line_color) -> list:
    elements = []
    elements.append(Paragraph("PROJECTS", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceBefore=1, spaceAfter=4))

    for proj in projects_data:
        proj_head = f"<b>Project Name :</b> {proj['name']}"
        elements.append(Paragraph(proj_head, styles['BoldSubHeader']))
        
        env_para = f"<b>Environment :</b> {proj['environment']}"
        elements.append(Paragraph(env_para, styles['BodyCustom']))
        
        elements.append(Paragraph("<b>Responsibilities & Key Contributions :</b>", styles['BodyCustom']))
        for bullet in proj['bullets']:
            elements.append(Paragraph(f"• {bullet}", styles['BulletCustom']))
        elements.append(Spacer(1, 4))

    return elements


def build_education_certifications(edu_data: list, cert_data: list, styles: dict, line_color) -> list:
    elements = []
    
    # Certifications
    if cert_data:
        elements.append(Paragraph("CERTIFICATIONS", styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceBefore=1, spaceAfter=4))
        for cert in cert_data:
            elements.append(Paragraph(f"• {cert}", styles['BodyCustom']))
        elements.append(Spacer(1, 4))

    # Education
    if edu_data:
        elements.append(Paragraph("EDUCATION", styles['SectionHeader']))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=line_color, spaceBefore=1, spaceAfter=4))
        for edu in edu_data:
            inst_para = f"<b>{edu['institution']}</b> - {edu['location']}"
            deg_para = f"{edu['degree']} ({edu['period']})"
            
            t = Table(
                [[Paragraph(inst_para, styles['BoldSubHeader']), Paragraph(deg_para, ParagraphStyle('RightEdu', parent=styles['BodyCustom'], alignment=TA_RIGHT))]],
                colWidths=[350, 190]
            )
            t.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            elements.append(t)
        elements.append(Spacer(1, 4))

    return elements


# ============================================================
# PDF GENERATOR MAIN FUNCTION
# ============================================================
def generate_custom_pdf_resume(resume_data: dict, output_filepath: str) -> str:
    """
    Generates a high quality PDF resume tailored for Python Django Developer.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles, primary_color, line_color = get_custom_resume_styles()
    story = []

    # 1. Header
    story.extend(build_header(resume_data['header'], styles))

    # 2. Professional Summary
    story.extend(build_summary(resume_data['summary'], styles, line_color))

    # 3. Technical Skills
    story.extend(build_skills(resume_data['skills'], styles, line_color))

    # 4. Professional Experience
    story.extend(build_experience(resume_data['experience'], styles, line_color))

    # 5. Key Projects
    story.extend(build_projects(resume_data['projects'], styles, line_color))

    # 6. Education & Certifications
    story.extend(build_education_certifications(resume_data['education'], resume_data['certifications'], styles, line_color))

    # Build PDF Document
    doc.build(story)
    return output_filepath


# ============================================================
# MAIN ENTRY POINT
# ============================================================
def main():
    print("=" * 60)
    print("[+] PYTHON DJANGO DEVELOPER RESUME GENERATOR")
    print("=" * 60)
    
    print("\n[JOB DESCRIPTION]")
    print(JOB_DESCRIPTION.strip())
    print("-" * 60)

    # Output path setup
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_PDF_NAME)
    
    print(f"\n[INFO] Generating tailored PDF resume...")
    pdf_file = generate_custom_pdf_resume(RESUME_DATA, output_path)
    
    print("\n" + "=" * 60)
    print("[SUCCESS] NEW TAILORED RESUME CREATED!")
    print(f"[PDF OUTPUT] {os.path.abspath(pdf_file)}")
    print(f"[ORIGINAL RESUME] Untouched at: {ORIGINAL_RESUME_PATH}")
    print("[EXPERIENCE STRICT] 3.0 Years of Experience")
    print("=" * 60)


if __name__ == "__main__":
    main()
