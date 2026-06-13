from google import genai
from dotenv import load_dotenv
import os

import streamlit as st

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def get_resume_suggestions(
    resume_text,
    job_description
):
   
    prompt = f"""
    You are an ATS expert and hiring manager.
    

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Provide:

    1. ATS Score Explanation
    2. Missing Skills
    3. Resume Improvements
    4. Stronger Resume Summary
    5. Project Ideas To Add
    6. Certifications To Pursue
    7. Interview Questions Based On Resume

    Format in markdown..
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt )
        return response.text
    except Exception as e:
        
        return f"❌ Error generating suggestions:\n\n{e}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text