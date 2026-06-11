from fpdf import FPDF

def generate_report(
    ats_score,
    match_score,
    matched_skills,
    missing_skills,
    filename="resume_report.pdf"
):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(
        200,
        10,
        "AI Resume Analyzer Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # ATS Score
    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        200,
        10,
        f"ATS Score: {ats_score}/100",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Resume Match: {match_score:.2f}%",
        ln=True
    )

    pdf.ln(5)

    # Matched Skills
    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        200,
        10,
        "Matched Skills",
        ln=True
    )

    pdf.set_font("Arial", "", 12)

    for skill in matched_skills:
        pdf.cell(
            200,
            8,
            f"- {skill}",
            ln=True
        )

    pdf.ln(5)

    # Missing Skills
    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        200,
        10,
        "Missing Skills",
        ln=True
    )

    pdf.set_font("Arial", "", 12)

    if missing_skills:

        for skill in missing_skills:

            pdf.cell(
                200,
                8,
                f"- {skill}",
                ln=True
            )

    else:

        pdf.cell(
            200,
            8,
            "No missing skills found",
            ln=True
        )

    pdf.output(filename)

    return filename