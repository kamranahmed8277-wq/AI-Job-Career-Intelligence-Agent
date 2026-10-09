from backend.app.services.job_description_analyzer import (
    extract_required_skills,
    analyze_job_description,
    extract_job_title,
    extract_required_experience,
    extract_education_requirements,
    extract_responsibilities,
    extract_important_keywords,
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
    AI Engineer
    Must know Python, FastAPI, Docker and RAG.
    """

    result = analyze_job_description(job_description)

    assert result == {
        "job_title": "AI Engineer",
        "required_skills": ["Python", "FastAPI", "Docker", "RAG"],
        "required_experience": None,
        "education_requirements": [],
        "responsibilities":[],
        "important_keywords":[],
    }


def test_analyze_job_description_with_experience():
    job_description = """
    AI Engineer
    Must know Python and FastAPI.
    Requires 3+ years of experience.
    """

    result = analyze_job_description(job_description)

    assert result == {
        "job_title": "AI Engineer",
        "required_skills": ["Python", "FastAPI"],
        "required_experience": "3+ years of experience",
        "education_requirements": [],
        "responsibilities":[],
        "important_keywords":[],
    }


def test_extract_job_title():
    text = """
    Frontend Developer

    We are looking for a skilled developer.
    Requirements: React, JavaScript, TypeScript.
    """
    result = extract_job_title(text)
    assert result == "Frontend Developer"


def test_extract_job_title_empty_text():
    result = extract_job_title("")
    assert result is None


def test_extract_required_experience():
    text = "AI Engineer with 3+ years of experience required."

    result = extract_required_experience(text)

    assert result == "3+ years of experience"


def test_extract_required_experience_range():
    text = "Candidates should have 2-4 years of experience."

    result = extract_required_experience(text)

    assert result == "2-4 years of experience"


def test_extract_required_experience_missing():
    text = "Python and FastAPI knowledge required."

    result = extract_required_experience(text)

    assert result is None


def test_extract_bachelors_requirement():
    text = "Requires a Bachelor's degree in Computer Science."

    result = extract_education_requirements(text)

    assert result == ["Bachelor's"]


def test_extract_masters_and_phd_requirements():
    text = "A Master's degree or PhD is preferred."

    result = extract_education_requirements(text)

    assert result == ["Master's", "PhD"]


def test_extract_education_requirements_missing():
    text = "Python, FastAPI, and Docker experience required."

    result = extract_education_requirements(text)

    assert result == []


def test_extract_responsibilities():
    text = """
    AI Engineer

    Responsibilities:
    - Build AI-powered applications
    - Develop REST APIs
    - Test and debug machine learning systems

    Requirements:
    - Python
    - FastAPI
    """

    result = extract_responsibilities(text)

    assert result == [
        "Build AI-powered applications",
        "Develop REST APIs",
        "Test and debug machine learning systems",
    ]


def test_extract_responsibilities_missing():
    text = """
    AI Engineer
    Requirements:
    - Python
    - FastAPI
    """

    result = extract_responsibilities(text)

    assert result == []



def test_extract_important_keywords():
    text = """
    Build Generative AI applications using LLMs.
    Develop REST API services and support automation of data pipelines.
    """

    result = extract_important_keywords(text)

    assert result == [
        "Generative AI",
        "LLMs",
        "automation",
        "REST API",
        "data pipelines",
    ]

def test_extract_important_keywords_case_insensitive():
    text = "Experience with NLP and CLOUD DEPLOYMENT."

    result = extract_important_keywords(text)

    assert result == ["NLP", "cloud deployment"]


def test_extract_important_keywords_empty_text():
    result = extract_important_keywords("")

    assert result == []



def test_complete_ai_engineer_job_description():
    text = """
    AI Engineer

    Responsibilities:
    - Build Generative AI applications.
    - Develop REST API services.

    Requirements:
    - Python, FastAPI, and Docker.
    - Bachelor's degree in Computer Science.
    - Requires 3+ years of experience.
    - Experience with LLMs and cloud deployment.
    """

    result = analyze_job_description(text)

    assert result["job_title"] == "AI Engineer"
    assert result["required_skills"] == [
        "Python", "FastAPI", "Docker","LLMs"
    ] or result["required_skills"] == [
        "Python", "FastAPI", "Docker"
    ]
    assert result["required_experience"] == "3+ years of experience"
    assert result["education_requirements"] == ["Bachelor's"]
    assert result["responsibilities"] == [
        "Build Generative AI applications.",
        "Develop REST API services.",
    ]
    assert result["important_keywords"] == [
        "Generative AI", "LLMs", "cloud deployment", "REST API"
    ]