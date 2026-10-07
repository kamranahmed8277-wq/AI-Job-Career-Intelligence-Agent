import re
import unicodedata


KNOWN_SKILLS = [
    "Python",
    "FastAPI",
    "Docker",
    "Azure",
    "Machine Learning",
    "RAG",
    "LLM",
]

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return text


def extract_required_skills(text: str) -> list[str]:
    text = normalize_text(text)

    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = rf"\b{re.escape(skill)}\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills

def analyze_job_description(text: str) -> dict:
    required_skills = extract_required_skills(text)

    return {
        "required_skills": required_skills
    }