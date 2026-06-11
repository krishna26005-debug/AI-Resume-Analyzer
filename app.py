from skill_extractor import extract_skills
from resume_parser import extract_text
from matcher import calculate_match_score
from jd_analyzer import extract_jd_skills
from ats_calculator import calculate_ats_score
from ai_suggestions import get_resume_suggestions
import plotly.graph_objects as go
from report_generator import generate_report
import plotly.express as px
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.skill-badge {
    display:inline-block;
    background:linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    color:white;
    padding:10px 18px;
    margin:6px;
    border-radius:25px;
    font-size:14px;
    font-weight:600;
    box-shadow:0px 4px 10px rgba(0,0,0,0.3);
    
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("📄 AI Resume Analyzer")

st.sidebar.markdown("---")

st.sidebar.success("✅ Resume Parsing")
st.sidebar.success("✅ Skill Extraction")
st.sidebar.success("✅ ATS Analysis")
st.sidebar.success("✅ Job Description Matching")

st.sidebar.info("🚧 AI Resume Suggestions")

st.sidebar.markdown("---")
st.sidebar.caption("Version 2.0")

# ==================================================
# HERO SECTION
# ==================================================
st.markdown("""
<div style="
padding:35px;
border-radius:20px;
background:linear-gradient(135deg,#1d4ed8,#7c3aed);
box-shadow:0px 8px 30px rgba(0,0,0,0.3);
margin-bottom:25px;
">

<h1 style="color:white;">
🚀 AI Resume Analyzer
</h1>

<p style="color:white;font-size:18px;">
Analyze resumes, calculate ATS scores,
identify missing skills, and receive AI-powered
career recommendations.
</p>

</div>
""", unsafe_allow_html=True)

# ==================================================
# FILE UPLOAD
# ==================================================
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

# ==================================================
# MAIN ANALYSIS
# ==================================================
if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    # ----------------------------------------------
    # JOB DESCRIPTION INPUT
    # ----------------------------------------------
    st.subheader("📋 Job Description")

    job_description = st.text_area(
        "Paste Job Description Here",
        height=200,
        placeholder="Paste the job description..."
    )

    # ----------------------------------------------
    # RESUME EXTRACTION
    # ----------------------------------------------
    resume_text = extract_text(uploaded_file)

    detected_skills = extract_skills(
        resume_text
    )

    tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analysis",
    "🎯 Skills",
    "🤖 AI Suggestions",
    "📄 Resume"
    ])

    # ----------------------------------------------
    # BASIC STATS
    # ----------------------------------------------
    word_count = len(
        resume_text.split()
    )

    char_count = len(
        resume_text
    )

    # ----------------------------------------------
    # HEALTH SCORE
    # ----------------------------------------------
    health_score = min(
        round(
            (len(detected_skills) * 4)
            + (word_count / 10)
        ),
        100
    )

    with tab1:
    # ----------------------------------------------
    # RESUME STATISTICS
    # ----------------------------------------------
        project_count = 0

        if (
            "projects" in resume_text.lower()
            and
            "certifications" in resume_text.lower()
        ):

            projects_section = (
                resume_text.lower()
                .split("projects")[1]
                .split("certifications")[0]
            )

            project_count = len([
                line
                for line in projects_section.split("\n")
                if "|" in line
           ])
        def count_certifications(resume_text):
            import re

            cert_match = re.search(
                r"CERTIFICATIONS(.*?)(SOFT SKILLS|$)",
                resume_text,
                re.IGNORECASE | re.DOTALL
            )

            if cert_match:
                cert_section = cert_match.group(1)

                certs = [
                line.strip()
                for line in cert_section.split("\n")
                if line.strip().startswith("•")
            ]

            return len([c for c in certs if len(c) > 3])

            return 0        
        
        
        cert_count = count_certifications(resume_text)
        st.subheader("📊 Resume Statistics")
        
        col1,col2,col3,col4,col5=st.columns(5)

        col1.metric("Skills",len(detected_skills))
        col2.metric("Words",word_count)
        col3.metric("Projects", project_count)
        col4.metric("Certifications", cert_count)
        col5.metric("Health",health_score)

        st.markdown("---")
        if health_score >= 80:
            st.success("🟢 Strong Resume")
        elif health_score >= 60: 
            st.warning("🟡 Good Resume - Needs Minor Improvements")
        else:
            st.error("🔴 Weak Resume - Significant Improvements Needed")   





    # ----------------------------------------------
    # RESUME SECTIONS
    # ----------------------------------------------
        st.markdown("---")

        st.subheader("📑 Resume Sections")

        section_checks = {
            
            "🎓 Education":
                "education" in resume_text.lower(),

            "🚀 Projects":
                "project" in resume_text.lower(),

            "🛠 Skills":
                "skill" in resume_text.lower(),

            "💼 Experience":
                "experience" in resume_text.lower(),

            "📜 Certifications":
                "certification" in resume_text.lower()
            }

        cols = st.columns(5)

        for col, (section, found) in zip(
        cols,
        section_checks.items()
        ):
            with col:

                if found:
                    st.success(section)
                else:
                    st.error(section)

    # ----------------------------------------------
    # ATS ANALYSIS
    # ----------------------------------------------
        if job_description:
            

            jd_skills = extract_jd_skills(
            job_description
            )

        

            match_score = calculate_match_score(
            resume_text,
            job_description
            )

            ats_score = calculate_ats_score(
            detected_skills,
            jd_skills,
            match_score,
            health_score    
            )

            fig= go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=ats_score,
                    title={"text": "ATS Score"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "blue"},
                        "steps": [
                            {"range": [0, 50], "color": "red"},
                            {"range": [50, 80], "color": "orange"},
                            {"range": [80, 100], "color": "green"}
                        ]
                    }
                )
            )    
  
            
            st.plotly_chart(
            fig,
            use_container_width=True
            )

            resume_skill_set={
            skill.lower()
            for skill in detected_skills
            }

            missing_skills=[
            skill 
            for skill in jd_skills
            if skill.lower() not in resume_skill_set
            ]

            st.markdown("---")

            st.subheader(
            "🎯 ATS Analysis"
            )

            if ats_score >= 80:
                st.success(
                "Excellent ATS Compatibility!"
                )
            elif ats_score >= 60:
                st.warning(
                "⚠ Resume Needs Minor Improvements"
                )
            else:
                st.error(
                "❌ ATS Optimization Required"
                )

            col1, col2, col3,col4 = st.columns(4)

            with col1:
                st.metric(
                "Resume Match %",
                f"{match_score:.2f}%"
                )

            with col2:
                st.metric(
                "ATS Score",
                f"{ats_score:.0f}/100"
                )
            with col3:
                if ats_score>=80:
                    st.metric(
                    "Status",
                    "Excellent"
                    )
                elif ats_score>= 60:
                    st.metric("Status","Moderate")
                else:
                    st.metric(
                    "Status",
                    "Low"
                    )        
            st.progress(min(max(float(ats_score/100), 0), 1))

            overall_score=round(
                (ats_score+health_score)/2
            )
            st.markdown("---")

            st.metric(
                "⭐ Overall Resume Score",
                f"{overall_score}/100"
            )

            jd_skill_set={
            jd_skill.lower()
            for jd_skill in jd_skills
            }


            matched_skills=[
            skill
            for skill in detected_skills
            if skill.lower() in jd_skill_set

            ]

            skills_match_percent = round(
            (
                len(matched_skills)
                /
                len(jd_skills)
            )*100,
            2
            ) if jd_skills else 0
        
            report_file=generate_report(
            ats_score,
            match_score,
            matched_skills,
            missing_skills
            )

            st.markdown("---")
            st.subheader("📄 ATS Report")
            with open(report_file, "rb") as pdf_file:
                st.download_button(
                label="📥 Download Detailed ATS Report",
                data=pdf_file,
                file_name="resume_report.pdf",
                mime="application/pdf")
            
            with col4:
               st.metric(
            "Skill Match %",
            f"{skills_match_percent}%"
                )
            


    with tab2:

    # ------------------------------------------
    # DETECTED SKILLS
    # ------------------------------------------
        st.markdown("---")

        st.subheader("🎯 Detected Skills")

        if detected_skills:


            skill_html = ""

            for skill in detected_skills:

               skill_html += f"""
            <span class="skill-badge">
                {skill}
            </span>
            """

            st.markdown(
            skill_html,
            unsafe_allow_html=True
            )

        else:
        
            st.warning(
               "No skills detected."
                )
        # ------------------------------------------
        # JOB DESCRIPTION ANALYSIS
        # ------------------------------------------
        if job_description:

            st.subheader(
            "⚠ Missing Skills"
                )

            if missing_skills:

                for skill in missing_skills:
                    st.markdown(
                    f"""
                    <div style="
                    padding:10px;
                    border-radius:10px;
                    background:#3f1d1d;
                    margin-bottom:8px;
                    ">
                    ❌ {skill}
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                    

            else:

                st.success(
                "No missing skills detected."
                )

        # ------------------------------------------
        # SKILL BREAKDOWN
        # ------------------------------------------
            st.subheader("📋 Skill Breakdown")
            st.progress(
            skills_match_percent/100
            )
            st.write(
            f"Skill Match: {skills_match_percent}%"
            )
            if matched_skills:

                st.success("Matched Skills")

                cols=st.columns(4)

                for i, skill in enumerate(matched_skills):
                   cols[i%4].success(skill)
        
        
        # ------------------------------------------
        # RECOMMENDED SKILLS TO LEARN
        # ------------------------------------------
            st.subheader("🎯 Learning Roadmap")

            if missing_skills:

                for skill in missing_skills:
                    st.markdown(
                    f"""
                    <div style="
                    padding:10px;
                    border-radius:10px;
                    background:#1d3f1d;
                    margin-bottom:8px;
                    ">
                    📚 Learn <b>{skill}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                   

            else:

                st.success(
                    "Your resume already covers all required skills."
                )
            

            pie_fig = px.pie(
                values=[
                len(matched_skills),
                len(missing_skills)
                ],
                names=[
                "Matched Skills",
                "Missing Skills"
                ],
                title="Skills Analysis"
            )  

            st.plotly_chart(
            pie_fig,
            use_container_width=True
            )
            pie_fig.update_traces(
                hole=0.55,
                textinfo="percent+label"
            )
        else:
                st.info(
                     "Paste a Job Description to view ATS skill analysis."

                )


    with tab3:
    # ----------------------------------------------
    # AI SUGGESTIONS
    # ----------------------------------------------

        if job_description:
            if st.button("🤖 Generate AI Suggestions"):
                with st.spinner("Generating AI Suggestions..."):
                    try:
                       suggestions = get_resume_suggestions(resume_text, job_description)
                       st.subheader("🤖 AI Resume Suggestions")
                       st.success("Analysis Complete!")
                       with st.expander("View AI Suggestions", expanded=True):
                            st.markdown(suggestions)
                            # Download button for AI suggestions
                       st.download_button(
                            label="📥 Download AI Suggestions",
                            data=suggestions,
                            file_name="ai_suggestions.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Gemini API Error: {e}")

        st.markdown("---")
        st.caption("Built with Python • Streamlit • Gemini AI • Plotly")
    

    with tab4:
        st.subheader(
            "📄 Resume Preview"
        )
        uploaded_file.seek(0)
        pdf_viewer(
            uploaded_file.read() 
        )


    # ----------------------------------------------
    # RESUME TEXT
    # ----------------------------------------------
        
        st.subheader(
        "📌 Resume Snapshot"
        )

        col1,col2,col3 = st.columns(3)

        with col1:
           st.metric(
            "Skills",
            len(detected_skills)
            )

        with col2:
           st.metric(
            "Words",
            word_count
            )

        with col3:
            st.metric(
            "Health Score",
            health_score
            )

        st.markdown("---")

        with st.expander(
        "📄 View Resume Text"
        ):

           st.text_area(
            "Resume Content",
            resume_text,
            height=500
            )
st.markdown("---")

st.caption(
    "Created by Krishna Singh | AI Resume Analyzer v2.0"
)         


       



