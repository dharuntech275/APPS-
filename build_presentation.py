"""
build_presentation.py
Generates a 10-slide, print-friendly widescreen (16:9) PowerPoint presentation (.pptx)
for the Final Year Mini Project:
"AI PREDICTIVE PERSONNEL STRESS AND WELFARE MONITORING SYSTEMS"
Presented by: DHARUN.M (Final Year, Computer Science and Business Systems)

Key features:
1. PRINT-FRIENDLY THEME:
   - Pure White (#FFFFFF) clean backgrounds across all 10 slides (saves ink/toner).
   - Crisp high-contrast dark text (#0F172A) that prints razor-sharp in Color or B&W.
   - Elegant thin borders without heavy dark fills that smudge on paper.
2. SIMPLE, EASY-TO-UNDERSTAND ENGLISH:
   - Crystal clear, conversational, punchy English that anyone can easily read,
     memorize, and present without stumbling.
3. SLIDE 1 REQUIREMENTS STRICTLY MET:
   - NAME : DHARUN.M
   - YEAR : FINAL YEAR
   - DEPT : COMPUTER SCIENCE AND BUSINESS SYSTEMS
   - PROJECT TITLE : AI PREDICTIVE PERSONNEL STRESS AND WELFARE MONITORING SYSTEMS
4. SLIDES 2 TO 10:
   - Exactly 3 clear, distinct points per slide with '01', '02', '03' indicators.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path="APPS_Mini_Project_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Print-Friendly High-Contrast Color Palette
    c_white = RGBColor(255, 255, 255)         # Pure White BG
    c_black_ink = RGBColor(15, 23, 42)        # #0F172A - Deep Charcoal Ink
    c_card_bg = RGBColor(250, 250, 250)       # #FAFAFA - Ultra-light Card BG
    c_card_border = RGBColor(148, 163, 184)   # #94A3B8 - Clean Border
    c_accent_blue = RGBColor(29, 78, 216)     # #1D4ED8 - High-visibility Blue
    c_accent_teal = RGBColor(15, 118, 110)    # #0F766E - Crisp Teal
    c_body_text = RGBColor(30, 41, 59)        # #1E293B - Crisp Body Text
    c_muted_text = RGBColor(100, 116, 139)    # #64748B - Gray for footer/meta

    blank_layout = prs.slide_layouts[6]

    # Helper: add pure white background with optional subtle border
    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_white
        bg.line.fill.background()
        return bg

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Print-Friendly Clean White Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    # Outer Decorative Print Border
    outer_frame = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.5), Inches(12.133), Inches(6.5))
    outer_frame.fill.solid()
    outer_frame.fill.fore_color.rgb = c_white
    outer_frame.line.color.rgb = c_accent_blue
    outer_frame.line.width = Pt(2)

    # Top Tag Box
    tag_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(4.5), Inches(0.42))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = RGBColor(239, 246, 255)
    tag_box.line.color.rgb = c_accent_blue
    tag_tf = tag_box.text_frame
    tag_tf.text = "FINAL YEAR MINI PROJECT PRESENTATION"
    p = tag_tf.paragraphs[0]
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = c_accent_blue
    p.alignment = PP_ALIGN.CENTER

    # Project Title
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.35), Inches(11.333), Inches(1.7))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    p_title = t_tf.paragraphs[0]
    p_title.text = "AI PREDICTIVE PERSONNEL STRESS AND WELFARE MONITORING SYSTEMS"
    p_title.font.name = "Arial"
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = c_black_ink
    p_title.alignment = PP_ALIGN.LEFT

    # Subtitle line in plain English
    p_sub = t_tf.add_paragraph()
    p_sub.text = "A Smart Web Platform to Track, Predict, and Protect the Mental Health of Soldiers"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = c_accent_teal
    p_sub.font.bold = True
    p_sub.space_before = Pt(6)

    # Candidate Credentials Card (White background, crisp outline for ink-saving printouts)
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.3), Inches(11.333), Inches(3.1))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(248, 250, 252)
    card.line.color.rgb = c_card_border
    card.line.width = Pt(1.5)

    c_tf = card.text_frame
    c_tf.word_wrap = True
    c_tf.vertical_anchor = MSO_ANCHOR.TOP

    p_card_hd = c_tf.paragraphs[0]
    p_card_hd.text = "STUDENT & PROJECT DETAILS"
    p_card_hd.font.name = "Arial"
    p_card_hd.font.size = Pt(12)
    p_card_hd.font.bold = True
    p_card_hd.font.color.rgb = c_accent_blue
    p_card_hd.space_after = Pt(12)

    details = [
        ("NAME :", "DHARUN.M"),
        ("YEAR :", "FINAL YEAR"),
        ("DEPT :", "COMPUTER SCIENCE AND BUSINESS SYSTEMS"),
        ("PROJECT TITLE :", "AI PREDICTIVE PERSONNEL STRESS AND WELFARE MONITORING SYSTEMS"),
    ]

    for label, val in details:
        p_row = c_tf.add_paragraph()
        p_row.text = f"{label:<16}  {val}"
        p_row.font.name = "Consolas"
        p_row.font.size = Pt(12.5)
        p_row.font.bold = True
        p_row.font.color.rgb = c_black_ink
        p_row.space_after = Pt(6)

    # Helper function for Content Slides (Slides 2 to 10)
    # Strictly 3 cards per slide, print-friendly white styling & simple English
    def add_content_slide(slide_num, category, title, points):
        s = prs.slides.add_slide(blank_layout)
        set_slide_bg(s)

        # Header Pill
        cat_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.45), Inches(3.5), Inches(0.35))
        cat_box.fill.solid()
        cat_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
        cat_box.line.color.rgb = c_card_border
        c_p = cat_box.text_frame.paragraphs[0]
        c_p.text = f"SLIDE {slide_num:02d} | {category.upper()}"
        c_p.font.name = "Arial"
        c_p.font.size = Pt(9.5)
        c_p.font.bold = True
        c_p.font.color.rgb = c_accent_blue
        c_p.alignment = PP_ALIGN.CENTER

        # Slide Title
        t_box = s.shapes.add_textbox(Inches(0.9), Inches(0.85), Inches(11.5), Inches(0.8))
        t_tf = t_box.text_frame
        t_p = t_tf.paragraphs[0]
        t_p.text = title
        t_p.font.name = "Arial"
        t_p.font.size = Pt(21)
        t_p.font.bold = True
        t_p.font.color.rgb = c_black_ink

        # 3 Structured Horizontal Cards (Crisp white fill, thin border - prints perfectly)
        card_w = Inches(11.533)
        card_h = Inches(1.6)
        start_y = Inches(1.75)
        gap_y = Inches(0.2)

        for i, (p_title, p_desc) in enumerate(points):
            y_pos = start_y + (i * (card_h + gap_y))

            # Outer Card
            c_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), y_pos, card_w, card_h)
            c_box.fill.solid()
            c_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
            c_box.line.color.rgb = c_card_border
            c_box.line.width = Pt(1)

            # Left Accent Badge (01, 02, 03) - Clean white background with colored border
            b_box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.15), y_pos + Inches(0.28), Inches(0.85), Inches(0.95))
            b_box.fill.solid()
            b_box.fill.fore_color.rgb = RGBColor(241, 245, 249)
            accent_borders = [c_accent_blue, c_accent_teal, c_black_ink]
            b_box.line.color.rgb = accent_borders[i % 3]
            b_box.line.width = Pt(1.5)

            b_tf = b_box.text_frame
            b_p = b_tf.paragraphs[0]
            b_p.text = f"{i+1:02d}"
            b_p.font.name = "Arial"
            b_p.font.size = Pt(20)
            b_p.font.bold = True
            b_p.font.color.rgb = accent_borders[i % 3]
            b_p.alignment = PP_ALIGN.CENTER

            # Text box for Card Title & Content
            txt_box = s.shapes.add_textbox(Inches(2.25), y_pos + Inches(0.15), Inches(10.0), Inches(1.3))
            txt_tf = txt_box.text_frame
            txt_tf.word_wrap = True

            pt_head = txt_tf.paragraphs[0]
            pt_head.text = p_title
            pt_head.font.name = "Arial"
            pt_head.font.size = Pt(13.5)
            pt_head.font.bold = True
            pt_head.font.color.rgb = c_black_ink

            pt_body = txt_tf.add_paragraph()
            pt_body.text = p_desc
            pt_body.font.name = "Arial"
            pt_body.font.size = Pt(11)
            pt_body.font.color.rgb = c_body_text
            pt_body.space_before = Pt(4)

        # Footer (Clear slide number for sorting printed paper)
        f_box = s.shapes.add_textbox(Inches(0.9), Inches(7.05), Inches(11.5), Inches(0.35))
        f_tf = f_box.text_frame
        f_p = f_tf.paragraphs[0]
        f_p.text = f"APPS - Final Year Mini Project | DHARUN.M (CSBS) | Slide {slide_num} of 10"
        f_p.font.name = "Arial"
        f_p.font.size = Pt(9)
        f_p.font.color.rgb = c_muted_text

        return s

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT (Super Simple English)
    # =========================================================================
    add_content_slide(
        2,
        "Problem Statement",
        "Why is This Project Needed? (Real Military Challenges)",
        [
            (
                "Hidden Stress in Field Duty",
                "Soldiers deployed in remote border areas face high mental pressure and very little sleep, but their daily stress goes unnoticed until it becomes severe."
            ),
            (
                "Manual Check-ups are Too Late",
                "Existing psychological reviews happen only once in 3 or 6 months. This huge delay prevents officers from stopping critical mental breakdowns in time."
            ),
            (
                "Soldiers Hesitate to Share Directly",
                "Due to fear and hesitation, soldiers do not talk about their sadness openly, and commanding officers have no digital tool to spot high-risk jawans early."
            )
        ]
    )

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES (Super Simple English)
    # =========================================================================
    add_content_slide(
        3,
        "Project Objectives",
        "What Did We Build to Solve This Problem?",
        [
            (
                "Easy Daily Health Tracking",
                "Build a simple website where every soldier can easily submit their daily sleep hours, duty stress, and heart rate in less than 30 seconds."
            ),
            (
                "Automatic Color Alert (Triage System)",
                "Automatically categorize soldiers into Red (High Risk), Yellow (Medium Risk), and Green (Safe) based on their daily health scores."
            ),
            (
                "Instant Emergency Help & Calming Tool",
                "Provide a 1-click Crisis SOS call button to Army Helplines and an interactive 4-7-8 breathing exercise to calm rapid heartbeats and panic."
            )
        ]
    )

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (Super Simple English)
    # =========================================================================
    add_content_slide(
        4,
        "System Architecture",
        "How the System Works: 3 Roles & Cloud Setup",
        [
            (
                "Three Clear User Roles",
                "Strict division of duties: Soldiers log daily data; Welfare Officers monitor risk rosters and give counseling; Senior Admins manage overall Army stats."
            ),
            (
                "Safe Cloud Database with Zero Data Loss",
                "Developed using Python Flask and SQLite, connected to private Vercel cloud storage so that database records are permanently saved without losing data."
            ),
            (
                "Works Smoothly on Mobile & Laptop",
                "Designed with a clean mobile slide-out menu for smartphones and an executive two-column dashboard for laptops with zero horizontal scrolling."
            )
        ]
    )

    # =========================================================================
    # SLIDE 5: PERSONNEL MODULE (Super Simple English)
    # =========================================================================
    add_content_slide(
        5,
        "Personnel Module",
        "How a Soldier Uses the System Daily",
        [
            (
                "4 Quick Daily Health Inputs",
                "Soldier enters only four basic numbers: Sleep hours (0-12), Operational stress slider (1-10), Heart rate (bpm), and Squad morale (1-5)."
            ),
            (
                "Smartwatch One-Click Sync",
                "A single 'Sync Smartwatch' button automatically fills sensor heart rate and sleep values so the soldier does not need to type manually."
            ),
            (
                "Daily Streak & Achievement Badges",
                "App rewards consecutive daily entries with positive streak counts and military badges (like 'Iron Mind') to encourage daily self-care habits."
            )
        ]
    )

    # =========================================================================
    # SLIDE 6: CLINICAL TRIAGE & FATIGUE FORECASTER (Super Simple English)
    # =========================================================================
    add_content_slide(
        6,
        "Smart Health Logic",
        "Automated Risk Triage & 7-Day Sleep Loss Forecaster",
        [
            (
                "Automatic Red / Yellow / Green Tagging",
                "If sleep is under 5 hours or stress is 8 or above, the app immediately tags the soldier in RED (High Risk) so officers can help right away."
            ),
            (
                "7-Day Sleep Debt Calculation",
                "App calculates total lost sleep compared to the 7-hour army baseline and creates a 0-100% Operational Fatigue Score."
            ),
            (
                "Rest Alert to Prevent Duty Accidents",
                "If a soldier's fatigue score crosses 65%, the system immediately recommends mandatory rest to prevent weapon accidents and duty mistakes."
            )
        ]
    )

    # =========================================================================
    # SLIDE 7: CRISIS SOS & RELAXATION (Super Simple English)
    # =========================================================================
    add_content_slide(
        7,
        "Emergency Tools",
        "1-Click Crisis SOS & 4-7-8 Breathing Calmer",
        [
            (
                "1-Click Crisis SOS Button",
                "A prominent red SOS button allows soldiers in severe distress to immediately call the Army Helpline (1902) or Tele-MANAS (14416)."
            ),
            (
                "Flashing Red Alert for Officers",
                "When a soldier taps the SOS button, a flashing crimson red alert banner immediately pops up on the commanding officer's computer screen."
            ),
            (
                "Tactical 4-7-8 Breathing Stabilizer",
                "An animated circle guides the soldier: Inhale for 4s, Hold for 7s, and Exhale for 8s to quickly lower elevated heart rate and panic."
            )
        ]
    )

    # =========================================================================
    # SLIDE 8: OFFICER & ADMIN SUITE (Super Simple English)
    # =========================================================================
    add_content_slide(
        8,
        "Command Suite",
        "Supervision Tools for Welfare Officers & Admins",
        [
            (
                "Live Soldier Roster with Risk Filters",
                "Welfare Officers can view all soldiers in their unit, filter by Red, Yellow, or Green, and immediately help soldiers in danger."
            ),
            (
                "Confidential Counseling Diary",
                "Officers can record private clinical counseling notes, save action steps, and schedule follow-up dates securely in the database."
            ),
            (
                "Command Master PIN & Army Statistics",
                "Senior Admins can view army-wide risk charts, check tamper-proof activity logs, and change the 4-digit signup security PIN anytime."
            )
        ]
    )

    # =========================================================================
    # SLIDE 9: TECHNOLOGY & SECURITY (Super Simple English)
    # =========================================================================
    add_content_slide(
        9,
        "Tech Stack & Security",
        "Tools Used & Safety Mechanisms",
        [
            (
                "Reliable Modern Full-Stack",
                "Built using Python Flask, SQLite database, Vercel Cloud Serverless platform, ReportLab for PDF exports, and Vanilla HTML/CSS/JS."
            ),
            (
                "Strong Password & Recovery Security",
                "Passwords are encrypted using PBKDF2 hashing. Soldiers can reset forgotten passwords using their Name and Service Unit without email/SMS."
            ),
            (
                "Instant 3-Language Switcher",
                "One-click language dropdown allows soldiers to switch between English, Tamil, and Hindi instantly for barrier-free comfort."
            )
        ]
    )

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE SCOPE (Super Simple English)
    # =========================================================================
    add_content_slide(
        10,
        "Conclusion & Future Scope",
        "Project Summary & Next Steps",
        [
            (
                "Successfully Tested & Live Online",
                "The project is 100% completed and deployed live on Vercel at https://apps-nu-henna.vercel.app for real-world testing."
            ),
            (
                "Fast, Friction-Free Experience",
                "Removed all slow verification barriers so soldiers can log in directly and submit their health records in under 30 seconds."
            ),
            (
                "Future Plans: Real Smartwatches & Voice AI",
                "Future upgrades include direct Bluetooth pairing with actual military smartwatches and AI voice sentiment analysis during counseling."
            )
        ]
    )

    prs.save(output_path)
    print(f"Presentation successfully updated with {len(prs.slides)} print-friendly slides at: {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "APPS_Mini_Project_Presentation.pptx"
    create_presentation(out_file)
