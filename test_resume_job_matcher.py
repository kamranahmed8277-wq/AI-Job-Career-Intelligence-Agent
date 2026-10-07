from backend.app.services.resume_job_matcher import (
    match_resume_to_job,
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
        "missing_skills": ["Docker"]
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
        "missing_skills": []
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
        "missing_skills": ["Python", "FastAPI"]
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
        "missing_skills": []
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
        "missing_skills": []
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
        "missing_skills": []
    }