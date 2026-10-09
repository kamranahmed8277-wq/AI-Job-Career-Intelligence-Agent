import unicodedata


def normalize_skill(skill: str) -> str:
    return unicodedata.normalize(
        "NFKC",
        skill
    ).strip().lower()


def analyze_job_fit(
    match_score: float,
    required_skills: list[str]
) -> str:
    if not required_skills:
        return "Insufficient Data"

    if match_score >= 80:
        return "Strong Fit"

    if match_score >= 60:
        return "Moderate Fit"

    return "Weak Fit"


def calculate_match_score(
    matched_skills: list[str],
    required_skills: list[str]
) -> float:

    if not required_skills:
        return 0.0

    return round(
        (len(matched_skills) / len(required_skills)) * 100,
        2
    )


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

    match_score = calculate_match_score(
        matched_skills,
        required_skills
    )

    job_fit = analyze_job_fit(
        match_score,
        required_skills
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
        "job_fit": job_fit
    }