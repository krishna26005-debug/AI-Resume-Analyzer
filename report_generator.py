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

    # ==========================
    # TITLE
    # ==========================
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        0,
        12,
        "AI Resume Analyzer Report",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C"
    )

    pdf.ln(5)

    # ==========================
    # SUMMARY
    # ==========================
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(
        0,
        10,
        "Candidate Analysis Summary",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 12)

    pdf.cell(
        0,
        8,
        f"ATS Score: {ats_score}/100",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        8,
        f"Resume Match: {match_score}%",
        new_x="LMARGIN",
        new_y="NEXT"
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
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(5)

    # ==========================
    # MATCHED SKILLS
    # ==========================
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(
        0,
        10,
        "MATCHED SKILLS",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 12)

    if matched_skills:
        for skill in matched_skills:
            pdf.cell(
                0,
                8,
                f"[MATCH] {skill}",
                new_x="LMARGIN",
                new_y="NEXT"
            )
    else:
        pdf.cell(
            0,
            8,
            "No matched skills found.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    pdf.ln(5)

    # ==========================
    # MISSING SKILLS
    # ==========================
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(
        0,
        10,
        "MISSING SKILLS",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 12)

    if missing_skills:
        for skill in missing_skills:
            pdf.cell(
                0,
                8,
                f"[MISSING] {skill}",
                new_x="LMARGIN",
                new_y="NEXT"
            )
    else:
        pdf.cell(
            0,
            8,
            "No missing skills detected.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    pdf.ln(5)

    # ==========================
    # RECOMMENDATIONS
    # ==========================
 
    pdf.set_font("Helvetica", "B", 13)

    pdf.cell(0, 8, "-" * 35, new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "RECOMMENDATIONS", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "-" * 35, new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Helvetica", "", 12)

    if recommendations:
        for recommendation in recommendations:

            recommendation = str(recommendation).strip()

        # Remove problematic unicode characters
            recommendation = (
                recommendation
                .replace("✓", "")
                .replace("✗", "")
                .replace("•", "*")
                .replace("–", "-")
                .replace("—", "-")
                .replace("“", '"')
                .replace("”", '"')
                .replace("'", "'")
                .replace("'", "'")
            )

        # Convert to latin-1 safe text
            recommendation = recommendation.encode(
                "latin-1",
                "ignore"
            ).decode("latin-1")

            pdf.multi_cell(
                0,
                8,
                "- " + recommendation
            )
    else:
        pdf.multi_cell(
            0,
            8,
            "Resume aligns well with the job description."
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
        new_x="LMARGIN",
        new_y="NEXT"
    )

    file_name = "resume_report.pdf"
    pdf.output(file_name)

    return file_name