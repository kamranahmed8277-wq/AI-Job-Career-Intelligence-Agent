import unicodedata


def normalize_skill(skill: str) -> str:
    return unicodedata.normalize(
        "NFKC",
        skill
    ).strip().lower()


def match_resume_to_job(
    resume_skills: list[str],
    required_skills: list[str]
) -> dict:

    normalized_resume_skills = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        normalized_skill = normalize_skill(skill)

        if normalized_skill in normalized_resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }