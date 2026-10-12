
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


KNOWN_KEYWORDS = [
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
    "RAG",
    "model evaluation",
]


SECTION_HEADINGS = {
    "required skills",
    "skills required",
    "preferred skills",
    "experience",
    "work experience",
    "education",
    "qualifications",
    "requirements",
    "responsibilities",
    "keywords",
    "important keywords",
}


def normalize_text(text: str) -> str:
    """Normalize Unicode text before extracting information."""
    return unicodedata.normalize("NFKC", text)


def clean_heading_value(line: str, heading: str) -> str:
    """Return the text following a section heading."""
    pattern = rf"^\s*{re.escape(heading)}\s*:\s*"
    return re.sub(pattern, "", line, count=1, flags=re.IGNORECASE).strip()


def get_heading(line: str) -> str | None:
    """Identify a known section heading, with or without a colon."""
    cleaned = line.strip().rstrip(":").strip().lower()

    if cleaned in SECTION_HEADINGS:
        return cleaned

    for heading in SECTION_HEADINGS:
        pattern = rf"^\s*{re.escape(heading)}\s*:"
        if re.match(pattern, line, re.IGNORECASE):
            return heading

    return None


def extract_job_title(text: str) -> str | None:
    """Use the first non-empty line as the job title."""
    for line in normalize_text(text).splitlines():
        title = line.strip().rstrip(" .,:;-")
        if title:
            return title

    return None


def extract_required_skills(text: str) -> list[str]:
    """
    Extract skills from the explicit required-skills section.
    If no such section exists, fall back to the full description.
    """
    normalized_text = normalize_text(text)
    lines = normalized_text.splitlines()

    section_lines = []
    in_required_section = False
    found_required_section = False

    for line in lines:
        stripped = line.strip()
        heading = get_heading(stripped)

        if heading in {"required skills", "skills required"}:
            in_required_section = True
            found_required_section = True
            section_lines.append(
                clean_heading_value(stripped, heading)
            )
            continue

        if heading and in_required_section:
            break

        if in_required_section and stripped:
            section_lines.append(stripped)

    if found_required_section:
        search_text = " ".join(section_lines)
    else:
        search_text = normalized_text

    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, search_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills



def extract_required_experience(text: str) -> str | None:
    """Extract the experience duration without unrelated sentence text."""
    normalized_text = normalize_text(text)

    duration_pattern = re.compile(
        r"\b(?P<amount>"
        r"\d+\s*(?:\+\s*|-\s*\d+\s*)?"
        r"|one|two|three|four|five|six|seven|eight|nine|ten"
        r")\s*(?P<unit>years?|months?)"
        r"(?P<of_experience>\s+of\s+experience)?",
        re.IGNORECASE,
    )

    for line in normalized_text.splitlines():
        stripped = re.sub(r"^\s*[-*•]\s*", "", line.strip())

        if not stripped:
            continue

        match = duration_pattern.search(stripped)
        if not match:
            continue

        amount = re.sub(r"\s+", "", match.group("amount"))
        unit = match.group("unit").lower()
        duration = f"{amount} {unit}"

        remainder = stripped[match.end():]
        has_experience_context = bool(
            re.search(r"\bexperience\b", stripped, re.IGNORECASE)
        )

        if match.group("of_experience") or has_experience_context:
            duration += " of experience"

        # Preserve the preferred wording for descriptions such as
        # "Two years of experience preferred."
        if re.search(r"\bpreferred\b", remainder, re.IGNORECASE):
            return f"{duration} preferred."

        return duration

    return None


def extract_education_requirements(text: str) -> list[str]:
    """Identify common degree requirements mentioned in the JD."""
    normalized_text = normalize_text(text)

    education_patterns = [
        (
            r"\b(?:bachelor'?s?|BS|B\.S\.|BSc|B\.Sc\.)\b",
            "Bachelor's",
        ),
        (
            r"\b(?:master'?s?|MS|M\.S\.|MSc|M\.Sc\.)\b",
            "Master's",
        ),
        (
            r"\b(?:Ph\.?D\.?|doctorate)\b",
            "PhD",
        ),
    ]

    found_education = []

    for pattern, degree in education_patterns:
        if re.search(pattern, normalized_text, re.IGNORECASE):
            found_education.append(degree)

    return found_education


def extract_responsibilities(text: str) -> list[str]:
    """Extract responsibility items until the next recognized section."""
    lines = normalize_text(text).splitlines()
    responsibilities = []
    in_section = False

    for line in lines:
        stripped = line.strip()
        heading = get_heading(stripped)

        if heading == "responsibilities":
            in_section = True
            continue

        if not in_section:
            continue

        if heading:
            break

        if stripped:
            item = re.sub(r"^[-*•]\s*", "", stripped).strip()
            if item:
                responsibilities.append(item)

    return responsibilities



def extract_important_keywords(text: str) -> list[str]:
    """Extract configured keywords, prioritizing an explicit Keywords section."""
    normalized_text = normalize_text(text)
    lines = normalized_text.splitlines()

    keyword_lines = []
    in_keyword_section = False

    for line in lines:
        stripped = line.strip()
        heading = get_heading(stripped)

        if heading in {"keywords", "important keywords"}:
            in_keyword_section = True
            keyword_lines.append(
                clean_heading_value(stripped, heading)
            )
            continue

        if in_keyword_section and heading:
            break

        if in_keyword_section and stripped:
            keyword_lines.append(stripped)

    # Use the explicit Keywords section when supplied.
    # Otherwise, preserve legacy behavior but exclude RAG from
    # keyword-only extraction.
    if in_keyword_section:
        search_text = " ".join(keyword_lines)
        keywords = KNOWN_KEYWORDS
    else:
        search_text = normalized_text
        keywords = [
            keyword for keyword in KNOWN_KEYWORDS
            if keyword.lower() != "rag"
        ]

    found_keywords = []

    for keyword in keywords:
        pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"

        if re.search(pattern, search_text, re.IGNORECASE):
            if keyword == "LLM" and re.search(
                r"(?<!\w)LLMs(?!\w)",
                search_text,
                re.IGNORECASE,
            ):
                continue

            found_keywords.append(keyword)

    return found_keywords


def analyze_job_description(text: str) -> dict:
    """Analyze a job description using rule-based extraction."""
    normalized_text = normalize_text(text)

    return {
        "job_title": extract_job_title(normalized_text),
        "required_skills": extract_required_skills(normalized_text),
        "required_experience": extract_required_experience(normalized_text),
        "education_requirements": extract_education_requirements(
            normalized_text
        ),
        "responsibilities": extract_responsibilities(normalized_text),
        "important_keywords": extract_important_keywords(normalized_text),
    }
