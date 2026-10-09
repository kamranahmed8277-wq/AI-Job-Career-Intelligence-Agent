from backend.app.services.resume_job_matcher import (
    match_resume_to_job,
    calculate_match_score,
    analyze_job_fit,
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