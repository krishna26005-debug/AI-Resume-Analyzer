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

    # ==========================
    # TITLE
    # ==========================
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        0,
        12,
        "AI Resume Analyzer Report",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    # ==========================
    # SUMMARY
    # ==========================
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Candidate Analysis Summary", ln=True)

    pdf.set_font("Helvetica", "", 12)

    pdf.cell(
        0,
        8,
        f"ATS Score: {ats_score}/100",
        ln=True
    )

    pdf.cell(
        0,
        8,
        f"Resume Match: {match_score}%",
        ln=True
    )

    if ats_score >= 80:
        status = "Excellent"
    elif ats_score >= 60:
        status = "Good"
    else:
        status = "Needs Improvement"

    pdf.cell(
        0,
        8,
        f"Status: {status}",
        ln=True
    )

    pdf.ln(5)

    # ==========================
    # MATCHED SKILLS
    # ==========================
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "MATCHED SKILLS", ln=True)

    pdf.set_font("Helvetica", "", 12)

    if matched_skills:
        for skill in matched_skills:
            pdf.cell(
                0,
                8,
                f"✓ {skill}",
                ln=True
            )
    else:
        pdf.cell(
            0,
            8,
            "No matched skills found.",
            ln=True
        )

    pdf.ln(5)

    # ==========================
    # MISSING SKILLS
    # ==========================
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "MISSING SKILLS", ln=True)

    pdf.set_font("Helvetica", "", 12)

    if missing_skills:
        for skill in missing_skills:
            pdf.cell(
                0,
                8,
                f"✗ {skill}",
                ln=True
            )
    else:
        pdf.cell(
            0,
            8,
            "No missing skills detected.",
            ln=True
        )

    pdf.ln(5)

    # ==========================
    # RECOMMENDATIONS
    # ==========================
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "RECOMMENDATIONS", ln=True)

    pdf.set_font("Helvetica", "", 12)

    if recommendations:
        for recommendation in recommendations:
            pdf.multi_cell(
                0,
                8,
                f"• {recommendation}"
            )

    pdf.ln(5)

    # ==========================
    # FOOTER
    # ==========================
    current_date = datetime.now().strftime("%d %B %Y")

    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(
        0,
        8,
        f"Generated on: {current_date}",
        ln=True
    )

    file_name = "resume_report.pdf"
    pdf.output(file_name)

    return file_name