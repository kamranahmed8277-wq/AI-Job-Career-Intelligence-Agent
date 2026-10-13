import unicodedata
import re
from datetime import date, datetime


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
        normalize_skill(skill) for skill in resume_skills
    }

    # Remove duplicate required skills while preserving order.
    unique_required_skills = []
    seen_skills = set()

    for skill in required_skills:
        normalized_skill = normalize_skill(skill)

        if normalized_skill not in seen_skills:
            unique_required_skills.append(skill)
            seen_skills.add(normalized_skill)

    matched_skills = []
    missing_skills = []

    for skill in unique_required_skills:
        normalized_skill = normalize_skill(skill)

        if normalized_skill in normalized_resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_score = calculate_match_score(
        matched_skills,
        unique_required_skills
    )

    job_fit = analyze_job_fit(
        match_score,
        unique_required_skills
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
        "job_fit": job_fit
    }

def assess_experience(
    resume_experience: list[dict],
    required_experience: str | None,
    reference_date: date | None = None
) -> dict:
    """Compare resume experience duration with the job requirement."""

    if not required_experience:
        return {
            "status": "Unknown",
            "required": None,
            "evidence": "No experience requirement found."
        }

    # Extract the required number of years or months.
    requirement = re.search(
        r"(\d+(?:\.\d+)?)\s*(years?|yrs?|months?|mos?)\b",
        required_experience,
        re.IGNORECASE
    )

    if not requirement:
        return {
            "status": "Unknown",
            "required": required_experience,
            "evidence": "Could not understand the experience requirement."
        }

    required_amount = float(requirement.group(1))
    unit = requirement.group(2).lower()

    if unit.startswith(("year", "yr")):
        required_months = required_amount * 12
    else:
        required_months = required_amount

    # Use today's date in the application, or a supplied date in tests.
    today = reference_date or date.today()

    total_months = 0
    found_dates = False

    for record in resume_experience:
        dates = record.get("dates")

        if not dates or not isinstance(dates, str):
            continue

        # Example: Apr 2026 – Present
        parts = re.split(r"\s*[–—-]\s*", dates, maxsplit=1)

        if len(parts) != 2:
            continue

        try:
            start = datetime.strptime(parts[0].strip(), "%b %Y").date()
        except ValueError:
            try:
                start = datetime.strptime(
                    parts[0].strip(), "%B %Y"
                ).date()
            except ValueError:
                continue

        if parts[1].strip().lower() == "present":
            end = today
        else:
            try:
                end = datetime.strptime(
                    parts[1].strip(), "%b %Y"
                ).date()
            except ValueError:
                try:
                    end = datetime.strptime(
                        parts[1].strip(), "%B %Y"
                    ).date()
                except ValueError:
                    continue

        if start > today or end < start:
            continue

        months = (
            (end.year - start.year) * 12
            + end.month - start.month
        )

        total_months += months
        found_dates = True

    if not found_dates:
        return {
            "status": "Unknown",
            "required": required_experience,
            "evidence": "No valid employment date ranges were found."
        }

    if total_months >= required_months:
        status = "Met"
    else:
        status = "Not Met"

    return {
        "status": status,
        "required": required_experience,
        "evidence": (
            f"Resume shows approximately {total_months} months "
            f"of experience; the job requires "
            f"{required_months:g} months."
        )
    }





def assess_education(
    resume_education: dict | None,
    required_education: list[str]
) -> dict:
    """Compare the candidate's education with job requirements."""

    if not required_education:
        return {
            "status": "Unknown",
            "required": [],
            "evidence": "No education requirement found in the job description."
        }

    if not resume_education or not resume_education.get("degree"):
        return {
            "status": "Unknown",
            "required": required_education,
            "evidence": "No education degree was extracted from the resume."
        }

    degree = resume_education["degree"].lower()

    degree_levels = {
        "bachelor's": ["bachelor", "bachelors", "b.s.", "b.sc."],
        "master's": ["master", "masters", "m.s.", "m.sc."],
        "phd": ["phd", "ph.d.", "doctorate"],
    }

    candidate_level = None

    for level, terms in degree_levels.items():
        if any(term in degree for term in terms):
            candidate_level = level
            break

    if candidate_level is None:
        return {
            "status": "Unknown",
            "required": required_education,
            "evidence": "The extracted degree level could not be identified."
        }

    # A higher degree level generally meets a lower-level requirement.
    degree_order = {
        "bachelor's": 1,
        "master's": 2,
        "phd": 3,
    }

    for requirement in required_education:
        required_level = requirement.lower()

        if required_level not in degree_order:
            continue

        if degree_order[candidate_level] >= degree_order[required_level]:
            return {
                "status": "Met",
                "required": required_education,
                "evidence": f"Resume lists a {candidate_level} degree."
            }

    return {
        "status": "Not Met",
        "required": required_education,
        "evidence": f"Resume lists a {candidate_level} degree."
    }
