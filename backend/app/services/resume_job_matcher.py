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


def _parse_month_year(value: str, reference_date: date) -> date | None:
    """Parse a month/year date or the word Present."""
    value = value.strip().strip(".,")

    if value.lower() in {"present", "current", "now"}:
        return reference_date

    formats = (
        "%B %Y",  # April 2025
        "%b %Y",  # Apr 2025
        "%B, %Y",
        "%b, %Y",
    )

    from datetime import datetime

    for fmt in formats:
        try:
            parsed = datetime.strptime(value, fmt)
            return date(parsed.year, parsed.month, 1)
        except ValueError:
            continue

    return None


def _parse_experience_date_range(
    dates_text: str,
    reference_date: date,
) -> tuple[date, date] | None:
    """Parse ranges such as 'Jan 2025 – Present' or 'April 2025 to March 2026'."""
    if not dates_text:
        return None

    text = dates_text.strip()

    month_pattern = (
        r"\b("
        r"January|February|March|April|May|June|July|August|"
        r"September|October|November|December|"
        r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
        r")\.?\s*,?\s+\d{4}\b"
    )

    matches = list(re.finditer(month_pattern, text, flags=re.IGNORECASE))

    if not matches:
        return None

    start = _parse_month_year(matches[0].group(), reference_date)

    if start is None:
        return None

    # Use Present, Current, or Now as the end date when specified.
    remaining_text = text[matches[0].end():].strip()
    if re.match(r"^(?:to\b|[-–—])\s*(?:present|current|now)\b",
                remaining_text, flags=re.IGNORECASE):
        end = reference_date
    else:
        if len(matches) < 2:
            return None
        end = _parse_month_year(matches[1].group(), reference_date)

    if end is None or end < start:
        return None

    return start, end


def assess_experience(
        resume_experience,
        required_experience,
        reference_date: date | None = None,
) -> dict:
    """
    Compare dated resume experience against a job's required experience.

    The calculation counts calendar months inclusively. This is a
    practical month-level estimate, not an exact day-by-day duration.
    """
    reference_date = reference_date or date.today()

    if not required_experience:
        return {
            "status": "Unknown",
            "required": required_experience,
            "evidence": "No experience requirement was provided.",
        }

    requirement_text = str(required_experience).lower()
    requirement_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(years?|yrs?|months?|mos?)",
        requirement_text,
    )

    if not requirement_match:
        return {
            "status": "Unknown",
            "required": required_experience,
            "evidence": "Could not determine the required experience duration.",
        }

    amount = float(requirement_match.group(1))
    unit = requirement_match.group(2)

    required_months = (
        round(amount * 12)
        if unit.startswith(("year", "yr"))
        else round(amount)
    )

    if isinstance(resume_experience, str):
        records = [{"dates": resume_experience}]
    elif isinstance(resume_experience, dict):
        records = [resume_experience]
    else:
        records = resume_experience or []

    durations = []
    for record in records:
        if not isinstance(record, dict):
            continue

        dates_text = record.get("dates")
        if not dates_text:
            continue

        date_range = _parse_experience_date_range(
            str(dates_text),
            reference_date,
        )

        if date_range is None:
            continue

        start, end = date_range
        months = (
                (end.year - start.year) * 12
                + end.month - start.month
                + 1
        )
        durations.append(months)

    if not durations:
        return {
            "status": "Unknown",
            "required": required_experience,
            "evidence": "No valid employment date ranges were found.",
        }

    # Sum the records as a simple estimate. Overlapping jobs can be
    # double-counted, so this should not be treated as verified total tenure.
    total_months = sum(durations)

    if total_months >= required_months:
        status = "Met"
    else:
        status = "Not Met"

    years, months = divmod(total_months, 12)
    duration_parts = []

    if years:
        duration_parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months:
        duration_parts.append(f"{months} month{'s' if months != 1 else ''}")

    duration_text = " ".join(duration_parts) or "less than one month"

    return {
        "status": status,
        "required": required_experience,
        "evidence": (
            f"Resume date ranges indicate approximately {duration_text} "
            f"of experience ({total_months} calendar months)."
        ),
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
