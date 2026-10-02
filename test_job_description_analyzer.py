from backend.app.services.job_description_analyzer import (
    extract_required_skills,
    analyze_job_description,
)


def test_extract_required_skills():
    job_description = """
    • Practical knowledge of 𝗣𝘆𝘁𝗵𝗼𝗻
    """

    result = extract_required_skills(job_description)

    assert result == ["Python"]


def test_extract_required_skills_empty_text():
    job_description = ""

    result = extract_required_skills(job_description)

    assert result == []


def test_unknown_skill():
    job_description = """
    We need Python and Kubernetes experience.
    """

    result = extract_required_skills(job_description)

    assert result == ["Python"]


def test_analyze_job_description():
    job_description = """
    AI Engineer required.
    Must know Python, FastAPI, Docker and RAG.
    """

    result = analyze_job_description(job_description)

    assert result == {
        "required_skills": ["Python", "FastAPI", "Docker", "RAG"]
    }