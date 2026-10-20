"""
build_presentation_pdf.py
Generates a 10-page, landscape A4, print-optimized PDF version of the presentation:
"APPS_Mini_Project_Presentation_Printout.pdf"
Allows Dharun to directly print slides from any device, mobile phone, or Xerox/print shop
without needing Microsoft PowerPoint.

Features:
- Pure white background (zero wasted ink/toner).
- High-contrast black/charcoal typography for razor-sharp paper printing.
- Clean box borders and explicit 'Slide X of 10' markers.
- Matching 10 slides in super simple English.
"""

import sys
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class LandscapeNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()
        print(f"Total printout PDF pages rendered: {num_pages}")

    def draw_decorations(self, total_pages):
        self.saveState()
        page_w, page_h = landscape(A4)

        # Outer clean border for print alignment
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.8)
        self.rect(24, 20, page_w - 48, page_h - 40, stroke=1, fill=0)

        # Running Footer on all pages
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 28, "APPS - Final Year Mini Project | DHARUN.M | Dept of Computer Science & Business Systems")
        page_str = f"Slide {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - 36, 28, page_str)

        self.restoreState()


def create_presentation_pdf(output_path="APPS_Mini_Project_Presentation_Printout.pdf"):
    # Landscape A4: 841.89 pt width, 595.27 pt height
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=36
    )

    printable_w = 841.89 - 72  # 769.89 pt

    c_primary = colors.HexColor("#0F172A")    # Deep Navy / Black
    c_blue = colors.HexColor("#1D4ED8")       # Royal Blue
    c_teal = colors.HexColor("#0F766E")       # Teal
    c_border = colors.HexColor("#94A3B8")     # Border gray
    c_bg_light = colors.HexColor("#F8FAFC")   # Ultra light tint

    styles = getSampleStyleSheet()

    tag_style = ParagraphStyle(
        'PillTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_blue
    )

    s1_title_style = ParagraphStyle(
        'S1Title',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=c_primary
    )

    s1_sub_style = ParagraphStyle(
        'S1Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_teal
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary
    )

    card_head_style = ParagraphStyle(
        'CardHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=c_primary
    )

    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1E293B")
    )

    num_style = ParagraphStyle(
        'BadgeNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=18,
        alignment=1,
        textColor=c_blue
    )

    story = []

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    tag_table = Table([[Paragraph("FINAL YEAR MINI PROJECT PRESENTATION", tag_style)]], colWidths=[270])
    tag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, c_blue),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(tag_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("AI PREDICTIVE PERSONNEL STRESS AND WELFARE MONITORING SYSTEMS", s1_title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A Smart Web Platform to Track, Predict, and Protect the Mental Health of Soldiers", s1_sub_style))
    story.append(Spacer(1, 18))

    cred_content = [
        [Paragraph("<b>STUDENT &amp; PROJECT CREDENTIALS</b>", ParagraphStyle('H', parent=tag_style, fontSize=11, leading=13))],
        [Spacer(1, 6)],
        [Paragraph("<b>NAME :</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>DHARUN.M</b>", card_head_style)],
        [Spacer(1, 4)],
        [Paragraph("<b>YEAR :</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>FINAL YEAR</b>", card_head_style)],
        [Spacer(1, 4)],
        [Paragraph("<b>DEPT :</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>COMPUTER SCIENCE AND BUSINESS SYSTEMS</b>", card_head_style)],
        [Spacer(1, 4)],
        [Paragraph("<b>PROJECT TITLE :</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>AI PREDICTIVE PERSONNEL STRESS AND WELFARE MONITORING SYSTEMS</b>", card_head_style)],
    ]
    t_cred = Table(cred_content, colWidths=[printable_w - 40])
    t_cred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1.2, c_border),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_cred)

    # Helper to add standard 3-card slide
    def make_slide(slide_num, category, title, points):
        story.append(PageBreak())

        # Top Tag
        t_tag = Table([[Paragraph(f"SLIDE {slide_num:02d} | {category.upper()}", tag_style)]], colWidths=[240])
        t_tag.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 0.8, c_border),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('PADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_tag)
        story.append(Spacer(1, 8))

        # Title
        story.append(Paragraph(title, slide_title_style))
        story.append(Spacer(1, 14))

        # 3 Structured Cards
        for i, (p_head, p_desc) in enumerate(points):
            badge_t = Table([[Paragraph(f"{i+1:02d}", num_style)]], colWidths=[42], rowHeights=[40])
            badge_t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
                ('BOX', (0,0), (-1,-1), 1.2, c_blue if i==0 else (c_teal if i==1 else c_primary)),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))

            content_cell = [
                Paragraph(f"<b>{p_head}</b>", card_head_style),
                Spacer(1, 3),
                Paragraph(p_desc, card_body_style)
            ]

            card_row = Table([[badge_t, content_cell]], colWidths=[55, printable_w - 55])
            card_row.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 0.8, c_border),
                ('PADDING', (0,0), (-1,-1), 9),
            ]))
            story.append(card_row)
            story.append(Spacer(1, 10))

    # SLIDES 2 to 10
    make_slide(
        2,
        "Problem Statement",
        "Why is This Project Needed? (Real Military Challenges)",
        [
            ("Hidden Stress in Field Duty", "Soldiers deployed in remote border areas face high mental pressure and very little sleep, but their daily stress goes unnoticed until it becomes severe."),
            ("Manual Check-ups are Too Late", "Existing psychological reviews happen only once in 3 or 6 months. This huge delay prevents officers from stopping critical mental breakdowns in time."),
            ("Soldiers Hesitate to Share Directly", "Due to fear and hesitation, soldiers do not talk about their sadness openly, and commanding officers have no digital tool to spot high-risk jawans early.")
        ]
    )

    make_slide(
        3,
        "Project Objectives",
        "What Did We Build to Solve This Problem?",
        [
            ("Easy Daily Health Tracking", "Build a simple website where every soldier can easily submit their daily sleep hours, duty stress, and heart rate in less than 30 seconds."),
            ("Automatic Color Alert (Triage System)", "Automatically categorize soldiers into Red (High Risk), Yellow (Medium Risk), and Green (Safe) based on their daily health scores."),
            ("Instant Emergency Help & Calming Tool", "Provide a 1-click Crisis SOS call button to Army Helplines and an interactive 4-7-8 breathing exercise to calm rapid heartbeats and panic.")
        ]
    )

    make_slide(
        4,
        "System Architecture",
        "How the System Works: 3 Roles & Cloud Setup",
        [
            ("Three Clear User Roles", "Strict division of duties: Soldiers log daily data; Welfare Officers monitor risk rosters and give counseling; Senior Admins manage overall Army stats."),
            ("Safe Cloud Database with Zero Data Loss", "Developed using Python Flask and SQLite, connected to private Vercel cloud storage so that database records are permanently saved without losing data."),
            ("Works Smoothly on Mobile & Laptop", "Designed with a clean mobile slide-out menu for smartphones and an executive two-column dashboard for laptops with zero horizontal scrolling.")
        ]
    )

    make_slide(
        5,
        "Personnel Module",
        "How a Soldier Uses the System Daily",
        [
            ("4 Quick Daily Health Inputs", "Soldier enters only four basic numbers: Sleep hours (0-12), Operational stress slider (1-10), Heart rate (bpm), and Squad morale (1-5)."),
            ("Smartwatch One-Click Sync", "A single 'Sync Smartwatch' button automatically fills sensor heart rate and sleep values so the soldier does not need to type manually."),
            ("Daily Streak & Achievement Badges", "App rewards consecutive daily entries with positive streak counts and military badges (like 'Iron Mind') to encourage daily self-care habits.")
        ]
    )

    make_slide(
        6,
        "Smart Health Logic",
        "Automated Risk Triage & 7-Day Sleep Loss Forecaster",
        [
            ("Automatic Red / Yellow / Green Tagging", "If sleep is under 5 hours or stress is 8 or above, the app immediately tags the soldier in RED (High Risk) so officers can help right away."),
            ("7-Day Sleep Debt Calculation", "App calculates total lost sleep compared to the 7-hour army baseline and creates a 0-100% Operational Fatigue Score."),
            ("Rest Alert to Prevent Duty Accidents", "If a soldier's fatigue score crosses 65%, the system immediately recommends mandatory rest to prevent weapon accidents and duty mistakes.")
        ]
    )

    make_slide(
        7,
        "Emergency Tools",
        "1-Click Crisis SOS & 4-7-8 Breathing Calmer",
        [
            ("1-Click Crisis SOS Button", "A prominent red SOS button allows soldiers in severe distress to immediately call the Army Helpline (1902) or Tele-MANAS (14416)."),
            ("Flashing Red Alert for Officers", "When a soldier taps the SOS button, a flashing crimson red alert banner immediately pops up on the commanding officer's computer screen."),
            ("Tactical 4-7-8 Breathing Stabilizer", "An animated circle guides the soldier: Inhale for 4s, Hold for 7s, and Exhale for 8s to quickly lower elevated heart rate and panic.")
        ]
    )

    make_slide(
        8,
        "Command Suite",
        "Supervision Tools for Welfare Officers & Admins",
        [
            ("Live Soldier Roster with Risk Filters", "Welfare Officers can view all soldiers in their unit, filter by Red, Yellow, or Green, and immediately help soldiers in danger."),
            ("Confidential Counseling Diary", "Officers can record private clinical counseling notes, save action steps, and schedule follow-up dates securely in the database."),
            ("Command Master PIN & Army Statistics", "Senior Admins can view army-wide risk charts, check tamper-proof activity logs, and change the 4-digit signup security PIN anytime.")
        ]
    )

    make_slide(
        9,
        "Tech Stack & Security",
        "Tools Used & Safety Mechanisms",
        [
            ("Reliable Modern Full-Stack", "Built using Python Flask, SQLite database, Vercel Cloud Serverless platform, ReportLab for PDF exports, and Vanilla HTML/CSS/JS."),
            ("Strong Password & Recovery Security", "Passwords are encrypted using PBKDF2 hashing. Soldiers can reset forgotten passwords using their Name and Service Unit without email/SMS."),
            ("Instant 3-Language Switcher", "One-click language dropdown allows soldiers to switch between English, Tamil, and Hindi instantly for barrier-free comfort.")
        ]
    )

    make_slide(
        10,
        "Conclusion & Future Scope",
        "Project Summary & Next Steps",
        [
            ("Successfully Tested & Live Online", "The project is 100% completed and deployed live on Vercel at https://apps-nu-henna.vercel.app for real-world testing."),
            ("Fast, Friction-Free Experience", "Removed all slow verification barriers so soldiers can log in directly and submit their health records in under 30 seconds."),
            ("Future Plans: Real Smartwatches & Voice AI", "Future upgrades include direct Bluetooth pairing with actual military smartwatches and AI voice sentiment analysis during counseling.")
        ]
    )

    doc.build(story, canvasmaker=LandscapeNumberedCanvas)
    print(f"Printout PDF successfully created with 10 landscape pages at: {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "APPS_Mini_Project_Presentation_Printout.pdf"
    create_presentation_pdf(out_file)
