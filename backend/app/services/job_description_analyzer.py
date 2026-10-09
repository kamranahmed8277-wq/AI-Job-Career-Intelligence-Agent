import re
import unicodedata


KNOWN_SKILLS = [
    "Python",
    "FastAPI",
    "Docker",
    "Azure",
    "Machine Learning",
    "RAG",
    "LLMs",
    "PyTorch",
]

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return text


def extract_job_title(text: str) -> str | None:
    text = normalize_text(text)
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:
        return lines[0]

    return None

def extract_required_skills(text: str) -> list[str]:
    text = normalize_text(text)

    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = rf"\b{re.escape(skill)}\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


def extract_required_experience(text: str) -> str | None:
    patterns = [
        r"\b\d+\+?\s*(?:-|to)\s*\d+\s+years?\s+of experience\b",
        r"\b\d+\+?\s+years?\s+of experience\b",
        r"\b\d+\+?\s+years?\s+experience\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    return None


def extract_education_requirements(text: str) -> list[str]:
    education_patterns = [
        (r"\bBachelor'?s?\b|\bBS\b|\bB\.S\.\b|\bBSc\b|\bB\.Sc\.\b", "Bachelor's"),
        (r"\bMaster'?s?\b|\bMS\b|\bM\.S\.\b|\bMSc\b|\bM\.Sc\.\b", "Master's"),
        (r"\bPh\.?D\.?\b|\bdoctorate\b", "PhD"),
    ]

    found_education = []

    for pattern, degree in education_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            found_education.append(degree)

    return found_education


def extract_responsibilities(text: str) -> list[str]:
    lines = text.splitlines()
    responsibilities = []
    in_responsibilities_section = False

    section_headers = (
        "responsibilities",
        "what you'll do",
        "what you will do",
        "duties",
        "role overview",
    )

    stop_headers = (
        "requirements",
        "qualifications",
        "education",
        "benefits",
        "what we're looking for",
        "what we are looking for",
    )

    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue

        normalized_line = cleaned_line.lower().rstrip(":")

        if any(
                normalized_line == header
                for header in section_headers
        ):
            in_responsibilities_section = True
            continue

        if any(
                normalized_line == header
                for header in stop_headers
        ):
            in_responsibilities_section = False
            continue

        if in_responsibilities_section:
            item = re.sub(r"^[\s•\-*]+", "", cleaned_line).strip()
            if item:
                responsibilities.append(item)

    return responsibilities


def extract_important_keywords(text: str) -> list[str]:
    known_keywords = [
        "Generative AI",
        "LLM",
        "LLMs",
        "NLP",
        "automation",
        "cloud deployment",
        "REST API",
        "deep learning",
        "computer vision",
        "data pipelines",
    ]

    found_keywords = []

    for keyword in known_keywords:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_keywords.append(keyword)

    return found_keywords

def analyze_job_description(text: str) -> dict:
    job_title = extract_job_title(text)
    required_skills = extract_required_skills(text)
    required_experience = extract_required_experience(text)
    education_requirements = extract_education_requirements(text)
    responsibilities = extract_responsibilities(text)
    important_keywords = extract_important_keywords(text)

    return {
        "job_title": job_title,
        "required_skills": required_skills,
        "required_experience": required_experience,
        "education_requirements":education_requirements,
        "responsibilities": responsibilities,
        "important_keywords": important_keywords,
    }