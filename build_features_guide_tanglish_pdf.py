"""
build_features_guide_tanglish_pdf.py
Generates a comprehensive, professional, publication-quality technical PDF guide
in Tanglish (Tamil in English script) documenting every single feature built into
the APPS (AI Predictive Personnel Stress and Welfare Monitoring System) platform,
how each feature works, and how personnel/officers/admins should use them.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from xml.sax.saxutils import escape as xml_escape

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to calculate total page count and render running headers,
    footers, border rules, and dynamic 'Page X of Y' pagination.
    """
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()
        print(f"Total pages rendered in Tanglish Guide: {num_pages}")

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_w, page_h = A4

        # Skip headers and footers on Cover Page (Page 1)
        if self._pageNumber > 1:
            # Header text
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0F172A"))
            self.drawString(36, page_h - 26, "APPS PLATFORM - COMPLETE FEATURES & USAGE MANUAL (TANGLISH)")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(page_w - 36, page_h - 26, "ARMED FORCES DEFENSE SYSTEM")

            # Header rule
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(36, page_h - 30, page_w - 36, page_h - 30)

            # Footer rule
            self.line(36, 36, page_w - 36, 36)

            # Footer text
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 24, "APPS Technical & Operational User Guide | Tanglish Edition")
            page_str = f"Pakkam {self._pageNumber} of {page_count}"
            self.drawRightString(page_w - 36, 24, page_str)

        self.restoreState()


def create_tanglish_guide_pdf(output_path="APPS_Features_Guide_Tanglish.pdf"):
    # Margins: 36pt (0.5 in) left/right, 40pt top/bottom
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=40
    )

    page_width, page_height = A4
    printable_width = page_width - 72  # 523.27 pt

    styles = getSampleStyleSheet()

    # Color Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Navy
    c_accent = colors.HexColor("#1E40AF")     # Royal Blue
    c_teal = colors.HexColor("#0D9488")       # Deep Teal
    c_body = colors.HexColor("#1E293B")       # Dark Slate
    c_muted = colors.HexColor("#64748B")      # Slate Gray
    c_border = colors.HexColor("#CBD5E1")     # Border
    c_bg_light = colors.HexColor("#F8FAFC")   # Background light
    c_card_bg = colors.HexColor("#F1F5F9")    # Card background
    c_danger = colors.HexColor("#DC2626")     # Crimson
    c_success = colors.HexColor("#16A34A")    # Green
    c_amber = colors.HexColor("#D97706")      # Amber

    # Custom Typography Styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=27,
        textColor=c_primary,
        alignment=0
    )

    cover_sub_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        alignment=0
    )

    cover_desc_style = ParagraphStyle(
        'CoverDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_body,
        alignment=0
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=c_body,
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.8,
        textColor=c_body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.0,
        leading=10.5,
        textColor=colors.white
    )

    tc_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.0,
        textColor=c_body
    )

    tc_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.2,
        textColor=c_primary
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.0,
        textColor=c_body
    )

    def callout(text, bg=c_bg_light, border_color=c_accent, left_bar_width=3):
        t = Table(
            [[Paragraph(text, callout_text)]],
            colWidths=[printable_width]
        )
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 0.5, c_border),
            ('LINEBEFORE', (0,0), (0,-1), left_bar_width, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = []

    # =========================================================================
    # COVER PAGE (PAGE 1)
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(callout("<b>MILITARY CLASSIFICATION: ARMED FORCES INTERNAL USE ONLY</b> &bull; Confidential Welfare Engineering Guide", bg=colors.HexColor("#FEF2F2"), border_color=c_danger))
    story.append(Spacer(1, 14))

    story.append(Paragraph("APPS Platform - Muzhu Features &amp; Usage Manual", cover_title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("AI Predictive Personnel Stress &amp; Welfare Monitoring System (Tanglish Edition)", cover_sub_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Indha official technical document-la namma APPS system start panna naal-la irundhu ippo varaikkum build panna "
        "<b>ellaa features, tools, clinical algorithms, security mechanisms, matrum UI components</b> patri detailed-ah Tanglish-la "
        "vilakkapattulladhu. Indha platform soldier psychological health-ai early-stage-la analyze panni, severe burnout, depression, "
        "matrum PTSD issues-ai prevent panna design panna pattu irukku. Ovvoru feature-um epadi work aagudhu, adhai epadi use pannanum, "
        "yaaru use pannanum enbadhai keezhe detailed-ah paarkkalaam.",
        cover_desc_style
    ))
    story.append(Spacer(1, 12))

    # Meta Info Card
    meta_data = [
        [Paragraph("<b>Document Title:</b>", tc_bold), Paragraph("APPS Complete System Features &amp; User Manual (Tanglish)", tc_style)],
        [Paragraph("<b>Target Audience:</b>", tc_bold), Paragraph("Soldiers (Personnel), Welfare Officers, Senior Command Admins, Developers", tc_style)],
        [Paragraph("<b>System Core Engine:</b>", tc_bold), Paragraph("Python Flask, SQLite3, Vercel Blob Persistent Snapshot Engine, CSS3 Flex/Grid", tc_style)],
        [Paragraph("<b>Security Baseline:</b>", tc_bold), Paragraph("PBKDF2 Password Salting, Command PIN Gating, Immutable Activity Audit Trail", tc_style)],
        [Paragraph("<b>Live Production URL:</b>", tc_bold), Paragraph("<code>https://apps-nu-henna.vercel.app</code> (Deployed on Vercel)", tc_style)],
        [Paragraph("<b>Repository:</b>", tc_bold), Paragraph("<code>https://github.com/dharuntech275/APPS-</code> (Dual tracked: <code>main</code> &amp; <code>master</code>)", tc_style)],
    ]
    t_meta = Table(meta_data, colWidths=[120, printable_width - 120])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # Executive Overview
    story.append(Paragraph("1. System Overview &amp; 3-Tier Command Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_primary, spaceBefore=2, spaceAfter=5))
    story.append(Paragraph(
        "APPS platform armed forces jawan-galukku matrum welfare officers-kku oru reliable digital bridge-ah vela seiyudhu. "
        "System-la motham <b>3 mukkiya roles</b> irukku:",
        body_style
    ))

    story.append(Paragraph("&bull; <b>1. Personnel (Soldier / Jawan):</b> Dhinamum thanga stress, thoongum neram (sleep hours), heart rate, matrum family morale status-ai log panni thanga mental fitness-ai track pannalaam. Instant panic relief-ku 4-7-8 breathing exercise matrum emergency 1-click Crisis SOS call seiyalaam.", bullet_style))
    story.append(Paragraph("&bull; <b>2. Welfare Officer:</b> Thanga command unit-la irukkum anaithu jawans-oda health status-ai live-ah monitor pannalaam. High-risk red alert jawans-ai prioritize panni clinical counseling notes add panni suicide prevention actions edukalaam.", bullet_style))
    story.append(Paragraph("&bull; <b>3. Senior Admin (HQ Command):</b> Unit-level statistics (High, Medium, Low risk counts), comprehensive risk analytics, audit trail activity logs, matrum overall system oversight control seiyalaam.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(callout("<b>Mukkiya Kurippu:</b> Starting-la login issue irundhadhu, adhai streamline panni login direct aakkiyom. Pinnar 2FA shield kooda thevai illai enbadhaal UI, database, matrum backend flow-la irundhu clean-ah remove panni friction-free direct login ready panniyom.", bg=c_bg_light, border_color=c_teal))

    # =========================================================================
    # SECTION 2: AUTHENTICATION, PIN & ACCOUNT SECURITY
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Authentication, Account Management &amp; Security Features", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_primary, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("2.1 Direct Secure Login &amp; Session Management", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> User thanga username matrum password enter panni direct-ah thanga dashboard-kku login seiyyum system. "
        "2FA TOTP shield thevai illai endru sonnadhukku apparam, 6-digit authenticator code thevai illamal direct single-step login create panni irukkom.<br/>"
        "<b>Epadi Work Aagudhu:</b> User credentials enter pannumpodhu, backend-la SQLite database query panni password verify aagum. "
        "Password match aana udane HTTP-only permanent signed session create aagi, user-oda role-kku thagundha dashboard-kku redirect aagum (`/dashboard`, `/officer/personnel`, or `/admin_dashboard`).<br/>"
        "<b>Benefit:</b> Field-la network speed kuraivaaga irukkum podhum jawan-gal friction illamal 2 seconds-la login panni daily log submit panna mudiyum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.2 Frictionless Multi-Role Direct Registration", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> User request-kku inanga Command Security PIN-ai neekki, Personnel, Welfare Officer, matrum Senior Admin aana yaarum direct-ah thanga role-ai select panni register seiyyum instant onboarding system.<br/>"
        "<b>Epadi Work Aagudhu:</b> Signup screen-la 'Personnel', 'Officer', alladhu 'Admin' tab-ai click panni, Name, Unit, and Password enter panninaale podhum. "
        "Zero delay-la account create aagi respective dashboard-kku login panna mudiyum.<br/>"
        "<b>Benefit:</b> Onboarding speed adhigam aagividum, network illaatha idathilum staff PIN authentication error illamal account create seiyalaam.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.3 Cryptographic PBKDF2 Password Hashing &amp; Weak Password Upgrade", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Security upgrade feature. Pazhaiya plain-text alladhu weak passwords-ai defense-grade PBKDF2-HMAC-SHA256 salting-kku automatic-ah upgrade seiyyum mechanism.<br/>"
        "<b>Epadi Work Aagudhu:</b> User login pannumpodhu password weak-aga irundhaalo alladhu unhashed-aga irundhaalo, system udane `/upgrade_password` modal popup kaattum. "
        "User 8+ characters strong password set panniyavudan cryptographically hash aagi database-la update aagividum.<br/>"
        "<b>Benefit:</b> Military staff accounts brute-force attacks matrum credential theft-la irundhu safe-ah irukkum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.4 Self-Service Password Recovery (/forgot_password)", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Soldier password marandhu poitaal, external email alladhu SMS OTP thevai illamal thanga unit verification moolam password-ai reset pannum defense self-service tool.<br/>"
        "<b>Epadi Work Aagudhu:</b> Login screen-la 'Forgot Password?' click panni, Registered Name matrum Service Unit (e.g. 15 Rajputana Rifles) submit pannanum. "
        "Record match aana udane puthiya password set panna allow pannum.<br/>"
        "<b>Benefit:</b> Remote border outpost-la phone network / OTP service illadhavargalukku indha unit-verified recovery migavum help-ah irukku.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.5 Login Page Streamlining &amp; Cleanup", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Neenga ketta maadhiri login page-la irundha thevai illadha banners, unnecessary test links, matrum clutter-ai remove panni clean executive login card-ah maathiyadhu.<br/>"
        "<b>Epadi Work Aagudhu:</b> Clean card layout, direct username/password fields, role-based registration link, matrum emergency hotline reference mattum display aagum.<br/>"
        "<b>Benefit:</b> User confuse aagaamal fast-ah login seiyalaam.",
        body_style
    ))

    # =========================================================================
    # SECTION 3: PERSONNEL (SOLDIER) CORE FEATURES
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Personnel (Soldier / Jawan) Features &amp; Detailed Usage", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_primary, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("3.1 Daily Mental Health &amp; Wellness Assessment Survey", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Jawan thanga daily psychological and physical health telemetry-ai submit pannum core assessment form. "
        "Idhula 4 clinical metrics irukku:<br/>"
        "&bull; <b>1. Sleep Duration (Hours):</b> 0 mudhal 12 mani neram varai thoongiya alavu.<br/>"
        "&bull; <b>2. Operational Stress Level (1 - 10 Slider):</b> Interactive slider. Move pannumpodhu Dynamic Qualitative Badges marum: "
        "1-3 (Calm &amp; Focused - Green), 4-5 (Manageable Duty Load - Slate), 6-7 (Elevated Tension - Amber), 8-10 (Critical Combat Stress / High Risk - Red).<br/>"
        "&bull; <b>3. Heart Rate / Pulse (BPM):</b> 40 mudhal 180 bpm varai physical exertion alavu.<br/>"
        "&bull; <b>4. Social / Family Morale Connection (1 - 5 Stars):</b> Family and squad support level.<br/>"
        "&bull; <b>Field Operational Notes:</b> Thangalukku irukkum bayam, thoongamai, alladhu duty shramathai pathi ezhuthalaam.<br/>"
        "<b>Epadi Use Pannanum:</b> Personnel dashboard-kku vandhu sliders-ai adjust panni, 'Log Daily Wellness Entry' button-ai click pannanum.<br/>"
        "<b>Benefit:</b> Jawan-oda daily mental status continuous-ah track aagum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.2 Automated Psychological Triage Scoring Algorithm", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Jawan log submit panna udane, AI clinical heuristic algorithm automatic-ah triage level-ai calculate pannum:<br/>"
        "&bull; <b>High Risk (Urgent Action Required - Red):</b> Sleep &lt; 5 hours, Stress &gt;= 8, Heart Rate &gt; 100 bpm, alladhu Social Connection == 1.<br/>"
        "&bull; <b>Medium Risk (Moderate Caution - Amber):</b> Sleep 5-6 hours, Stress 5-7, alladhu Heart Rate 90-100 bpm.<br/>"
        "&bull; <b>Low Risk (Stable Mental State - Green):</b> Adequate sleep (&gt;= 7h), Stress &lt; 5, normal heart rate.<br/>"
        "<b>Benefit:</b> Welfare officers immediate-ah yaara contact pannanum-nu automated-ah theriyum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.3 Tactical 4-7-8 Breathing &amp; Relaxation Stabilizer", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Jawan-galukku panic attack, battle stress, alladhu sleeplessness varumpodhu parasympathetic nervous system-ai activate seiyyum breathing tool.<br/>"
        "<b>Epadi Work Aagudhu:</b> Dashboard-la '4-7-8 Relax' quick action button alladhu full card irukku. 'Start Session' click panninaal:<br/>"
        "1. <b>Inhale (4s):</b> Animated circle expand aagum, mooku valiyaaga moochu ulle edukka vendum.<br/>"
        "2. <b>Hold (7s):</b> Circle steady-ah irukkum, moochai adakki vaikka vendum.<br/>"
        "3. <b>Exhale (8s):</b> Circle shrink aagi moochai vaai valiyaaga methuvaaga veliye vida vendum.<br/>"
        "Dynamic cycle counter (Cycle 1 of 4) matrum animated progress bar display aagum.<br/>"
        "<b>Benefit:</b> 2 minutes-kulle heart rate kuraithu instant mental calmness kidaikkum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.4 Simulated Smartwatch / BLE Telemetry Sync", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Wearable fitness bands alladhu army smartwatches (BLE) illadha idathil kooda, telemetry sensor-ai simulate panni single click-la realistic sleep and heart rate data-vai fill pannum tool.<br/>"
        "<b>Epadi Use Pannanum:</b> Daily survey form-la irukkum 'Sync Smartwatch Data' button-ai click seiyyum podhu, realistic military biometrics (Sleep: 6.8h, Heart Rate: 72 bpm) automatic-ah form fields-la load aagividum.<br/>"
        "<b>Benefit:</b> Form fill seiyyum neram kuraivadhaal jawans regular-ah entry poduvargal.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.5 1-Click Crisis SOS Emergency Beacon", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Soldier extreme mental breakdown, suicidal thoughts, alladhu severe panic situation-la irukkumpodhu 1-click-la emergency help kidaikkum defense beacon.<br/>"
        "<b>Epadi Work Aagudhu:</b> Header-lum dashboard banner-lum prominent RED SOS button irukku. Click panninaal:<br/>"
        "1. Army Emergency Helpline (<b>1902</b>) &amp; National Tele-MANAS (<b>14416</b>) direct call modal open aagum.<br/>"
        "2. Welfare Officer matrum Admin screen-la urgent red pulsing banner alert dispatch aagum.<br/>"
        "<b>Benefit:</b> Life-saving crisis intervention immediate-ah kidaikkum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.6 Cumulative Fatigue Forecaster &amp; 7-Day Sleep Debt Engine", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Soldier kadandha 7 naatkalaga evvalavu thookkam izhanthirukirar (sleep debt) enbadhai calculate seiyyum clinical algorithm.<br/>"
        "<b>Epadi Work Aagudhu:</b> Baseline military requirement 7 hours daily sleep. Daily sleep deficit-ai kooti <b>Operational Strain Index (0 - 100%)</b> calculate seiyudhu. "
        "Strain index 65%-kku mela ponaal, 'Severe Sleep Debt Alert - Mandatory Rest Required' endru recommendation kaattum.<br/>"
        "<b>Benefit:</b> Prolonged fatigue aala varum weapon handling accidents matrum guard duty lapses-ai thadukkum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.7 Gamified Morale Badges &amp; Daily Streak Tracking", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Jawans thodarndhu daily entry pottu thanga health-ai track panna motivate pannum gamification system.<br/>"
        "<b>Epadi Work Aagudhu:</b> Consecutive days entry pottaal streak increase aagum (e.g. 5-Day Streak 🔥). "
        "Athil 'Mental Resilience Sentinel', 'Sleep Master', 'Iron Mind' pontra military achievement badges unlock aagum.<br/>"
        "<b>Benefit:</b> Mental health entry oru duty-ah feel aagaamal positive habit-ah maarrum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3.8 Soldier Personal Health Dossier PDF Export (/my/export_pdf)", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Jawan thanga mudiyatha health history, past surveys, triage levels, matrum fatigue index-ai professional medical PDF report-ah download seiyyum feature.<br/>"
        "<b>Benefit:</b> Base medical officer-kku physical check-up panna poga podhu indha PDF report-ai katti consultation edukalaam.",
        body_style
    ))

    # =========================================================================
    # SECTION 4: WELFARE OFFICER COMMAND SUITE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Welfare Officer Command Suite &amp; Clinical Management", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_primary, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("4.1 Personnel Live Monitoring Roster &amp; Triage Filter", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Officer thanga command unit-la irukkum anaithu jawans-oda current psychological triage status-ai live-ah paarkkum central dashboard.<br/>"
        "<b>Epadi Work Aagudhu:</b> Personnel list table-la ovvoru jawan-oda Name, Service Unit, Latest Sleep, Stress Level, Heart Rate, Triage Tag (High/Medium/Low), matrum Action link display aagum. "
        "Search bar matrum filter moolam High Risk jawans-ai mattum instant-ah isolate panni paarkkalaam.<br/>"
        "<b>Benefit:</b> 100+ jawans irundhalum, risk-la irukkum 3 jawan-ai 2 seconds-la identify panna mudiyum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4.2 Soldier Longitudinal Clinical Dossier", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Oru specific jawan-oda complete past records, date-wise mental trends, sleep debt graph, matrum biometric changes-ai kaattum detailed profile.<br/>"
        "<b>Epadi Use Pannanum:</b> Personnel list-la jawan name pakkathula 'View Dossier' click seiyya vendum.<br/>"
        "<b>Benefit:</b> Sudden mood drop alladhu prolonged combat fatigue eppo start aanadhu endru accurate-ah track panna mudiyum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4.3 Confidential Clinical Counseling Notes Engine", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Welfare Officer jawan-kku 1-on-1 counseling kuduthu vittu, thanga clinical findings, action steps, matrum next review date-ai confidential-ah log pannum tool.<br/>"
        "<b>Epadi Work Aagudhu:</b> Dossier page-la 'Add Clinical Counseling Note' form irukku. Officer note type (General Counseling, PTSD Intervention, Family Stress) select panni text submit panninaal, "
        "athu encrypted SQLite `CounselingNotes` table-la save aagum matrum `ActivityLog`-lum immutable audit entry vizhum.<br/>"
        "<b>Benefit:</b> Medically structured record maintain aagum; soldier transfer aanaalum new officer-kku past background theriyum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4.4 Emergency SOS Alert Banner Intercept", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Jawan SOS button-ai trigger panninaal, officer-oda screen-la top position-la pulsing crimson RED banner display aagum.<br/>"
        "<b>Benefit:</b> Officer vera edhavathu page-la irundhaalum, emergency case-ai miss panna maattaargal.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4.5 Unit Welfare Assessment Report PDF Export (/officer/export_report)", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Motha unit-oda triage distribution, high-risk case summary, matrum counseling follow-up details-ai formal military briefing PDF document-ah export seiyyum tool.<br/>"
        "<b>Benefit:</b> Commanding Brigade alladhu Battalion Headquarters-kku weekly welfare status report submit panna idhu direct-ah use aagum.",
        body_style
    ))

    # =========================================================================
    # SECTION 5: SENIOR ADMIN COMMAND HEADQUARTERS
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("5. Senior Admin Command Headquarters &amp; Operations", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_primary, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("5.1 Real-Time Executive Command Analytics Dashboard", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Headquarters Admin-kku armed forces units-oda overall mental readiness-ai bird's-eye view-la kaattum analytics overview.<br/>"
        "<b>Epadi Work Aagudhu:</b> Total Registered Personnel count, High Risk Soldiers count (Red Card), Medium Risk count (Yellow Card), and Stable Low Risk count (Green Card) live metric cards-ah display aagum. "
        "Unit-wise summary table-la ovvoru regiment/battalion-la evvalavu per risk-la irukkanga endra data varum.<br/>"
        "<b>Benefit:</b> Top brass commanders endha unit-la operational stress adhigama irukku-nu therindhu squad rotation alladhu leave sanction seiyalaam.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5.2 Mobile Responsive Drawer & Touch Layout System", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Smartphone-la view pannum podhu elements olunga theriyadha prachanai-ai fix panna build panna mobile-first responsive layout.<br/>"
        "<b>Epadi Use Pannanum:</b> Mobile phone-la open pannumpodhu slide-out drawer menu, side-by-side equal height quick action buttons (`Crisis SOS` and `4-7-8 Relax`), 5-column mood selector, and zero horizontal scroll automatically fit aagum.<br/>"
        "<b>Benefit:</b> Field-la chinna screen phone-la use pannaalum perfect alignment and touch accessibility kidaikkum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5.3 Immutable Operational Audit Trail (ActivityLog)", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> System-la nadakkum anaithu critical actions-aiyum timestamp, actor ID, target soldier, matrum action type-udan record pannum defense audit trail.<br/>"
        "<b>Epadi Work Aagudhu:</b> Login, counseling note entry, PIN change, triage status transition ellaame append-only table-la save aagum. Yaarume indha logs-ai edit alladhu delete panna mudiyadhu.<br/>"
        "<b>Benefit:</b> Military security compliance matrum complete operational accountability urudhi aagum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5.4 Senior Command Summary PDF Export (/admin/export_report)", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Top-level military executive report ready pannum generator.<br/>"
        "<b>Benefit:</b> Monthly readiness briefings-kku presentation-ready formatted report kidaikkum.",
        body_style
    ))

    # =========================================================================
    # SECTION 6: UI/UX, LOCALIZATION & CLOUD ARCHITECTURE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. UI/UX Layout, Localization &amp; Cloud Infrastructure", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_primary, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("6.1 Multi-Language Vernacular Switcher (English, தமிழ், हिंदी)", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Soldier thanga thaa mozhiyil (Tamil, Hindi, alladhu English) system-ai use seiyyum client-side instant language toggle.<br/>"
        "<b>Epadi Work Aagudhu:</b> Header-la dropdown select box irukku. Language choose panninaal zero-latency-la page-la irukkum ellaa text-um instant-ah switch aagum. "
        "Indha preference browser-oda `localStorage`-la save aavadhaal, adutha murai open pannumpothum avargalukku thaa mozhiyileye varum.<br/>"
        "<b>Benefit:</b> English theriyadha jawans kooda easy-ah survey fill panni mental health assistance pera mudiyum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6.2 Laptop Executive 2-Column Grid &amp; Mobile Responsive Drawer Layout", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Neenga ketta laptop view and mobile alignment request-kku yetharpola build panna responsive design system.<br/>"
        "<b>Epadi Work Aagudhu:</b><br/>"
        "&bull; <b>Laptop Screens (&gt;= 992px):</b> Modern 2-column executive grid (`1.15fr 0.85fr`). Left column-la survey card, right column-la fatigue forecaster matrum gamified morale badges pakkam pakkamaaga clean-ah render aagum. Horizontal scroll illamal compact executive presentation kidaikkum.<br/>"
        "&bull; <b>Mobile Screens (&lt; 768px):</b> Touch-friendly single column vertical flow. Navigation bar hamburger icon moolam slide-out drawer menu-ah maarrum. "
        "Quick action buttons (`Crisis SOS` and `4-7-8 Relax`) side-by-side equal height wrap aagi touch panna comfortable-ah irukkum. Page-la horizontal overflow (`overflow-x: hidden`) completely zero aakki irukkom.<br/>"
        "<b>Benefit:</b> Soldier smartphone-la use panninaalum, Welfare Officer laptop-la use panninaalum flawless layout kidaikkum.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6.3 Vercel Serverless Architecture &amp; Private Vercel Blob Persistence Engine", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Cloud-la deployment panna podhu, serverless container shut down aanaalum database alindhu pogamal thadukkum zero-data-loss synchronization engine.<br/>"
        "<b>Epadi Work Aagudhu:</b> Vercel-la standard container ephemeral (temporary) aagum. Idhai solve panna custom `sync_db_to_blob()` matrum `sync_db_from_blob()` engine build panniyom. "
        "Ovvoru murai survey, note, alladhu PIN update pannumpothum, backend database SQLite file snapshot private Vercel Blob store (`apps-data` store ID: `store_eS9r7map43Dx32yX`)-kku instant-ah upload aagum. "
        "Pudhiya container wake up aagumpodhu blob store-la irundhu restored database automatic-ah hydrate aagividum.<br/>"
        "<b>Benefit:</b> Free cloud hosting-la kooda 100% persistent defense database guarantee kidaikkudhu.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6.4 2FA Shield Removal &amp; Login Streamlining Refactor", h2_style))
    story.append(Paragraph(
        "<b>Enna Feature:</b> Starting-la build panna Google Authenticator (RFC 6238 TOTP) shield-ai, user request-kku inanga complete-ah remove panniyom.<br/>"
        "<b>Enna Maathinom:</b><br/>"
        "1. Desktop header matrum mobile drawer-la irundha '2FA Shield' links anaithum neekkiyom.<br/>"
        "2. Admin Dashboard-la irundha '2FA Security Roster Card' matrum reset buttons neekkiyom.<br/>"
        "3. Login challenge intercept (`/login/2fa`) remove panni direct single-step login create panniyom.<br/>"
        "4. Database-la irundha `totp_enabled` flags reset panni Vercel Blob cloud store-lum sync panniyom.<br/>"
        "<b>Benefit:</b> Login process speed adhigamaagi, zero unnecessary verification step-la soldiers access panna mudiyudhu.",
        body_style
    ))

    # =========================================================================
    # SECTION 7: SUMMARY FEATURE MATRIX & USAGE CHEATSHEET
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("7. Comprehensive Feature Matrix &amp; Usage Cheatsheet", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_primary, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph("Keezhe kanda table-la namma platform-oda anaithu features, athai yar yaaru use pannalaam, matrum adhan primary use case quick reference summary-ah kudukappattulladhu:", body_style))
    story.append(Spacer(1, 4))

    matrix_data = [
        [
            Paragraph("<b>Feature Name</b>", table_header),
            Paragraph("<b>Access Role</b>", table_header),
            Paragraph("<b>Enna Purpose &amp; Epadi Use Aagum (Tanglish Summary)</b>", table_header),
            Paragraph("<b>Status</b>", table_header)
        ],
        [
            Paragraph("<b>Daily Assessment Survey</b>", tc_bold),
            Paragraph("Personnel", tc_style),
            Paragraph("Sleep (0-12h), Stress slider (1-10), Heart rate, Social connection log panna.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Triage Scoring Algorithm</b>", tc_bold),
            Paragraph("System / All", tc_style),
            Paragraph("Stress and sleep data vechu High (Red), Medium (Yellow), Low (Green) triage auto calculate aagum.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>4-7-8 Breathing Stabilizer</b>", tc_bold),
            Paragraph("Personnel", tc_style),
            Paragraph("Animated circle guide vechu 4s Inhale, 7s Hold, 8s Exhale seithu panic relief pera.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Smartwatch Telemetry Sync</b>", tc_bold),
            Paragraph("Personnel", tc_style),
            Paragraph("1-click-la wearable sensor heart rate and sleep biometrics form-la load panna.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>1-Click Crisis SOS Beacon</b>", tc_bold),
            Paragraph("Personnel / Officer", tc_style),
            Paragraph("Army 1902 &amp; Tele-MANAS 14416 call seiya + Officer screen-la pulsing red alert kaatta.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Cumulative Fatigue Forecaster</b>", tc_bold),
            Paragraph("Personnel / Officer", tc_style),
            Paragraph("7-day sleep debt calculation panni Operational Strain Index (0-100%) and rest alert kaatta.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Gamified Morale Badges</b>", tc_bold),
            Paragraph("Personnel", tc_style),
            Paragraph("Continuous self-logging seiyumbodhu daily streak and resilience badges unlock panna.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Personnel Monitoring Roster</b>", tc_bold),
            Paragraph("Officer", tc_style),
            Paragraph("Command unit jawans list-ai triage color tags and filters vechu live monitor panna.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Soldier Clinical Dossier</b>", tc_bold),
            Paragraph("Officer", tc_style),
            Paragraph("Oru soldier-oda complete historical trends, sleep graph, past notes review seiya.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Confidential Counseling Notes</b>", tc_bold),
            Paragraph("Officer", tc_style),
            Paragraph("1-on-1 counseling mudithu findings, treatment plan, next review date secure-ah log panna.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Executive Analytics Dashboard</b>", tc_bold),
            Paragraph("Admin", tc_style),
            Paragraph("Army-wide High, Medium, Low triage counts and unit health distribution overview.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Direct Multi-Role Access</b>", tc_bold),
            Paragraph("All Roles", tc_style),
            Paragraph("PIN barrier illamal direct-ah Personnel, Officer, Admin onboarding seiyyum streamlined system.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Unit Self-Service Recovery</b>", tc_bold),
            Paragraph("All Roles", tc_style),
            Paragraph("`/forgot_password` moolam Name + Service Unit submit panni password reset seiya.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Immutable Activity Audit Trail</b>", tc_bold),
            Paragraph("Admin / System", tc_style),
            Paragraph("All critical events, logins, notes, PIN changes timestamp-udan log aagum.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Vernacular Multi-Language</b>", tc_bold),
            Paragraph("All Roles", tc_style),
            Paragraph("Zero-latency-la English, Tamil, Hindi language switch seiya (`localStorage` persistence).", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Laptop 2-Col &amp; Mobile Drawer UI</b>", tc_bold),
            Paragraph("All Roles", tc_style),
            Paragraph("Zero horizontal overflow, 2-column laptop grid, touch-friendly mobile drawer menu.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Vercel Blob Cloud Persistence</b>", tc_bold),
            Paragraph("Cloud Backend", tc_style),
            Paragraph("Serverless cold boots-la SQLite database azhindhu pogamal automatic snapshot sync seiya.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>PDF Report Generators</b>", tc_bold),
            Paragraph("Personnel/Officer/Admin", tc_style),
            Paragraph("Soldier Dossier (`/my/export_pdf`), Officer Report, Admin Command Report download panna.", tc_style),
            Paragraph("Active", tc_bold)
        ],
        [
            Paragraph("<b>Delete Your Account</b>", tc_bold),
            Paragraph("All Roles", tc_style),
            Paragraph("Password verify panni user thanga account &amp; biometric data-vai permanently erase seiya.", tc_style),
            Paragraph("Active", tc_bold)
        ],
    ]

    t_matrix = Table(matrix_data, colWidths=[105, 75, printable_width - 230, 50], repeatRows=1)
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 1.6),
    ]))
    story.append(t_matrix)
    story.append(Spacer(1, 10))

    # Conclusion & Sign-off callout
    story.append(callout(
        "<b>Mudivu &amp; System Guarantee:</b> Indha APPS platform ippo military welfare monitoring-kku "
        "thevaiyaana anaithu modern tools-udan 100% production-ready aagi Vercel-la live-ah run aagudhu. "
        "Soldiers friction-free direct single-step login moolam entry podalaam, officers immediate triage action edukalaam, "
        "matrum Senior Admins command overview-ai securely maintain seiyalaam.",
        bg=colors.HexColor("#EFF6FF"),
        border_color=c_accent
    ))

    # Build the PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "APPS_Features_Guide_Tanglish.pdf"
    create_tanglish_guide_pdf(out_file)
