from fpdf import FPDF
from datetime import datetime


def generate_report(
    ats_score,
    match_score,
    matched_skills,
    missing_skills,
    recommendations
):
    ats_score = round(float(ats_score), 2)
    match_score = round(float(match_score), 2)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # =====================================
    # HEADER
    # =====================================
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(
        0,
        12,
        "AI RESUME ANALYZER REPORT",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C"
    )

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        0,
        8,
        f"Generated on {datetime.now().strftime('%d %B %Y')}",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C"
    )

    pdf.ln(5)

    # =====================================
    # SUMMARY BOX
    # =====================================
    if ats_score >= 80:
        status = "Excellent"
    elif ats_score >= 60:
        status = "Good"
    else:
        status = "Needs Improvement"

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(
        0,
        8,
        "CANDIDATE SUMMARY",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.rect(10, pdf.get_y(), 190, 32)

    y = pdf.get_y() + 4

    pdf.set_xy(15, y)
    pdf.set_font("Helvetica", "", 12)

    pdf.cell(
        0,
        7,
        f"ATS Score       : {ats_score}/100",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        7,
        f"Resume Match    : {match_score}%",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        7,
        f"Status          : {status}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(10)

    # =====================================
    # PERFORMANCE OVERVIEW
    # =====================================
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(
        0,
        8,
        "PERFORMANCE OVERVIEW",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Courier", "", 10)

    ats_bar = "#" * int(ats_score / 10)
    ats_bar += "-" * (10 - int(ats_score / 10))

    match_bar = "#" * int(match_score / 10)
    match_bar += "-" * (10 - int(match_score / 10))

    pdf.cell(
        0,
        8,
        f"ATS Score      [{ats_bar}]",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        8,
        f"Resume Match   [{match_bar}]",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(4)

    # =====================================
    # MATCHED SKILLS
    # =====================================
    pdf.set_font("Helvetica", "B", 14)

    pdf.cell(
        0,
        8,
        f"MATCHED SKILLS ({len(matched_skills)})",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(3)

    pdf.set_font("Helvetica", "", 11)

    if matched_skills:
        skills_text = " | ".join(sorted(matched_skills))
        pdf.multi_cell(
            0,
            7,
            skills_text
        )
    else:
        pdf.cell(
            0,
            7,
            "No matched skills found.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    pdf.ln(4)

    # =====================================
    # MISSING SKILLS
    # =====================================
    pdf.set_font("Helvetica", "B", 14)

    pdf.cell(
        0,
        8,
        f"MISSING SKILLS ({len(missing_skills)})",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(3)

    pdf.set_font("Helvetica", "", 11)

    if missing_skills:
        missing_text = " | ".join(sorted(missing_skills))
        pdf.multi_cell(
            0,
            7,
            missing_text
        )
    else:
        pdf.cell(
            0,
            7,
            "No missing skills detected.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    pdf.ln(4)

    # =====================================
    # RECOMMENDATIONS
    # =====================================
    pdf.set_font("Helvetica", "B", 14)

    pdf.cell(
        0,
        8,
        "RECOMMENDATIONS",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(3)

    pdf.set_font("Helvetica", "", 11)

    if recommendations:
        for i, recommendation in enumerate(recommendations, start=1):

            clean_text = (
                str(recommendation)
                .encode("latin-1", "ignore")
                .decode("latin-1")
            )

            pdf.multi_cell(
                0,
                7,
                f"{i}. {clean_text}"
            )

            pdf.ln(1)

    else:
        pdf.multi_cell(
            0,
            7,
            "Your resume aligns well with the job description."
        )

    pdf.ln(6)

    # =====================================
    # FOOTER
    # =====================================
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(4)

    pdf.set_font("Helvetica", "I", 10)

    pdf.cell(
        0,
        8,
        "Generated by AI Resume Analyzer",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C"
    )

    file_name = "resume_report.pdf"

    pdf.output(file_name)

    return file_name