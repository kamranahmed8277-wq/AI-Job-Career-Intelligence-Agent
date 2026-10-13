from datetime import date
from backend.app.services.resume_job_matcher import (
    match_resume_to_job,
    calculate_match_score,
    analyze_job_fit,
    assess_experience,
    assess_education,
)

def test_match_resume_to_job():
    resume_skills = ["Python", "FastAPI"]
    required_skills = ["Python", "FastAPI", "Docker"]

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result == {
        "matched_skills": ["Python", "FastAPI"],
        "missing_skills": ["Docker"],
        "match_score": 66.67,
        "job_fit": "Moderate Fit"
    }


def test_all_skills_matched():
    resume_skills = ["Python", "FastAPI", "Docker"]
    required_skills = ["Python", "FastAPI", "Docker"]

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result == {
        "matched_skills": ["Python", "FastAPI", "Docker"],
        "missing_skills": [],
        "match_score": 100.0,
        "job_fit": "Strong Fit"
    }


def test_all_skills_missing():
    resume_skills = []
    required_skills = ["Python", "FastAPI"]

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result == {
        "matched_skills": [],
        "missing_skills": ["Python", "FastAPI"],
        "match_score": 0.0,
        "job_fit":"Weak Fit",
    }


def test_no_required_skills():
    resume_skills = ["Python", "FastAPI"]
    required_skills = []

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result == {
        "matched_skills": [],
        "missing_skills": [],
        "match_score": 0.0,
        "job_fit": "Insufficient Data",
    }


def test_case_insensitive_matching():
    resume_skills = ["python", "fastAPI", "docker"]
    required_skills = ["Python", "FastAPI", "Docker"]

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result == {
        "matched_skills": ["Python", "FastAPI", "Docker"],
        "missing_skills": [],
        "match_score": 100.0,
        "job_fit": "Strong Fit"
    }

def test_skill_whitespace_matching():
    resume_skills = [" Python ", "FastAPI", "Docker "]
    required_skills = ["Python", "FastAPI", "Docker"]

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result == {
        "matched_skills": ["Python", "FastAPI", "Docker"],
        "missing_skills": [],
        "match_score": 100.0,
        "job_fit": "Strong Fit"
    }

def test_match_score():
    matched_skills = ["Python", "FastAPI", "Docker"]
    required_skills = ["Python", "FastAPI", "Docker", "RAG", "LLMs"]

    result = calculate_match_score(
        matched_skills,
        required_skills
    )

    assert result == 60.0


def test_match_score_all_matched():
    matched_skills = ["Python", "FastAPI", "Docker"]
    required_skills = ["Python", "FastAPI", "Docker"]

    result = calculate_match_score(
        matched_skills,
        required_skills
    )

    assert result == 100.0


def test_match_score_no_matches():
    matched_skills = []
    required_skills = ["Python", "FastAPI", "Docker"]

    result = calculate_match_score(
        matched_skills,
        required_skills
    )

    assert result == 0.0


def test_match_score_no_required_skills():
    matched_skills = []
    required_skills = []

    result = calculate_match_score(
        matched_skills,
        required_skills
    )

    assert result == 0.0


def test_strong_job_fit():
    result = analyze_job_fit(85, ["Python"])
    assert result == "Strong Fit"


def test_moderate_job_fit():
    result = analyze_job_fit(60, ["Python"])
    assert result == "Moderate Fit"


def test_weak_job_fit():
    result = analyze_job_fit(40, ["Python"])
    assert result == "Weak Fit"


def test_job_fit_returns_insufficient_data_when_no_required_skills():
    assert analyze_job_fit(0.0, []) == "Insufficient Data"


def test_job_fit_returns_weak_fit_when_skills_are_required_but_none_match():
    assert analyze_job_fit(0.0, ["Python"]) == "Weak Fit"


def test_duplicate_required_skills():
    resume_skills = ["Python", "FastAPI"]
    required_skills = ["Python", "Python", "FastAPI"]

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result["matched_skills"] == ["Python", "FastAPI"]
    assert result["missing_skills"] == []
    assert result["match_score"] == 100.0
    assert result["job_fit"] == "Strong Fit"


def test_unicode_styled_skill_matching():
    resume_skills = ["𝗣𝘆𝘁𝗵𝗼𝗻", "FastAPI"]
    required_skills = ["Python", "FastAPI"]

    result = match_resume_to_job(
        resume_skills,
        required_skills
    )

    assert result["matched_skills"] == ["Python", "FastAPI"]
    assert result["missing_skills"] == []
    assert result["match_score"] == 100.0
    assert result["job_fit"] == "Strong Fit"


from backend.app.services.resume_job_matcher import assess_experience


def test_experience_unknown_when_job_has_no_requirement():
    result = assess_experience(
        [{"company": "Example Company", "dates": "Jan 2025 – Present"}],
        None
    )

    assert result["status"] == "Unknown"


def test_experience_unknown_when_resume_has_no_records():
    result = assess_experience([], "1 year of experience")

    assert result["status"] == "Unknown"



def test_experience_met_when_dates_meet_requirement():
    result = assess_experience(
        [{"company": "Example Company", "dates": "Jan 2025 – Present"}],
        "1 year of experience",
        reference_date=date(2026, 1, 1)
    )

    assert result["status"] == "Met"


def test_education_requirement_met():
    result = assess_education(
        {"degree": "Bachelor's degree in Software Engineering"},
        ["Bachelor's"]
    )

    assert result["status"] == "Met"


def test_education_unknown_when_resume_has_no_degree():
    result = assess_education(None, ["Bachelor's"])

    assert result["status"] == "Unknown"


def test_education_unknown_when_job_has_no_requirement():
    result = assess_education(
        {"degree": "Bachelor's degree in Software Engineering"},
        []
    )

    assert result["status"] == "Unknown"

def test_extract_education_stops_before_experience():
    from backend.app.services.resume_analyzer import extract_education

    resume_text = (
        "Sara Khan\n"
        "Education\n"
        "Bachelor's degree in Software Engineering\n"
        "Experience\n"
        "Junior Python Developer at Example Company"
    )

    result = extract_education(resume_text)

    assert result is not None
    assert result["degree"] == "Bachelor's degree in Software Engineering"


from datetime import date

from backend.app.services.resume_job_matcher import assess_experience


def test_experience_met():
    experience = [
        {"dates": "Jan 2024 – Present"}
    ]

    result = assess_experience(
        experience,
        "1 year of experience",
        reference_date=date(2026, 1, 1)
    )

    assert result["status"] == "Met"


def test_experience_not_met():
    experience = [
        {"dates": "Jul 2025 – Present"}
    ]

    result = assess_experience(
        experience,
        "1 year of experience",
        reference_date=date(2026, 1, 1)
    )

    assert result["status"] == "Not Met"


def test_experience_unknown_when_dates_missing():
    experience = [
        {"company": "Example Company", "dates": None}
    ]

    result = assess_experience(
        experience,
        "1 year of experience",
        reference_date=date(2026, 1, 1)
    )

    assert result["status"] == "Unknown"


def test_experience_unknown_when_dates_invalid():
    experience = [
        {"dates": "Unknown"}
    ]

    result = assess_experience(
        experience,
        "1 year of experience",
        reference_date=date(2026, 1, 1)
    )

    assert result["status"] == "Unknown"



from datetime import date

from backend.app.services.resume_job_matcher import assess_experience


def test_experience_range_with_to_separator():
    result = assess_experience(
        [{"dates": "April 2025 to March 2026"}],
        "1 year of experience",
        reference_date=date(2026, 10, 13),
    )

    assert result["status"] == "Met"


def test_experience_range_with_dash_separator():
    result = assess_experience(
        [{"dates": "Apr 2025 – Mar 2026"}],
        "1 year of experience",
        reference_date=date(2026, 10, 13),
    )

    assert result["status"] == "Met"


def test_experience_range_with_present():
    result = assess_experience(
        [{"dates": "Apr 2026 – Present"}],
        "1 year of experience",
        reference_date=date(2026, 10, 13),
    )

    assert result["status"] == "Not Met"


def test_experience_with_invalid_dates_is_unknown():
    result = assess_experience(
        [{"dates": "Dates not available"}],
        "1 year of experience",
        reference_date=date(2026, 10, 13),
    )

    assert result["status"] == "Unknown"
