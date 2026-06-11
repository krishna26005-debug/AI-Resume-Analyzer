def calculate_ats_score(
    detected_skills,
    jd_skills,
    match_score,
    health_score
):

    detected_skills = {
        skill.lower()
        for skill in detected_skills
    }

    jd_skills = {
        skill.lower()
        for skill in jd_skills
    }

    matched_skills = (
        detected_skills
        &
        jd_skills
    )

    # 50% Skill Match

    skill_score = (
        len(matched_skills)
        /
        max(len(jd_skills), 1)
    ) * 50

    # 30% Resume vs JD Similarity

    content_score = (
        match_score
        * 0.30
    )

    # 20% Resume Quality

    quality_score = (
        health_score
        * 0.20
    )

    ats_score = (
        skill_score
        +
        content_score
        +
        quality_score
    )

    return round(
        min(ats_score, 100),
        2
    )