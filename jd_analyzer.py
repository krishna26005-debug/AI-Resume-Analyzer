import re
from skills_db import skills

def extract_jd_skills(jd_text):

    found = []

    jd_text = jd_text.lower()

    for skill in skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, jd_text):
            found.append(skill)

    return sorted(list(set(found)))