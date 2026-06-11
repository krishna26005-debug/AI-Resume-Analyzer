import re
from skills_db import skills

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))