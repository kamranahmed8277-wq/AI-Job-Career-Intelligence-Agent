import re

def extract_email(text: str) -> str | None:
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text: str) -> str | None:
    pattern = r"(?:\+92|0092|0)\s*\d{3}\s*\d{3}\s*\d{4}"

    match = re.search(pattern, text)

    if match:
        return match.group(0).strip()

    return None


def extract_name(text: str) -> str | None:
    lines = text.strip().splitlines()

    if not lines:
        return None

    name = lines[0].strip().strip(" .,:;-")

    if re.fullmatch(r"[A-Za-z]+(?:[ '-][A-Za-z]+)*", name):
        return name

    return None


KNOWN_SKILLS = [
    "Python",
    "FastAPI",
    "Flask",
    "Django",
    "SQL",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "Docker",
    "Git",
    "GitHub",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Generative AI",
    "LLMs",
]


def extract_skills(text: str) -> list[str]:
    found_skills = []

    for skill in KNOWN_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills



import re


def extract_education(text: str) -> dict | None:
    degree_pattern = (
        r"(Bachelor's|Bachelors|Bachelor|Master's|Masters|Master|"
        r"B\.S\.|B\.Sc\.|M\.S\.|M\.Sc\.|PhD)"
        r"\s+degree\s+in\s+[A-Za-z ]+?"
        r"(?=\s+from\b|[,.]|\s+\d{4}\s*[-–]\s*\d{4}|"
        r"\s+(?:Experience|Skills|Projects|Certifications|Awards)\b|$)"
    )

    match = re.search(degree_pattern, text, re.IGNORECASE)

    if not match:
        return None

    degree = match.group(0).strip()

    institution = None
    institution_match = re.search(
        r"\bfrom\s+(.+?)(?=\s+\d{4}\s*[-–]\s*\d{4}|[,.]|$)",
        text[match.end():],
        re.IGNORECASE,
    )

    if institution_match:
        institution = institution_match.group(1).strip()

    years_match = re.search(
        r"\b(19\d{2}|20\d{2})\s*[-–]\s*(19\d{2}|20\d{2})\b",
        text,
    )
    years = years_match.group(0) if years_match else None

    location = None

    if institution:
        location_match = re.search(
            r"\b(rawalpindi|islamabad|lahore|karachi)\b",
            institution,
            re.IGNORECASE,
        )

        if location_match:
            location = location_match.group(0).title()
            institution = institution[:location_match.start()].strip()

    return {
        "institution": institution,
        "degree": degree,
        "location": location,
        "years": years,
    }


def extract_experience_section(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # First, look for a formal Experience heading.
    for i, line in enumerate(lines):
        if line.rstrip(":").lower() == "experience":
            experience_lines = []

            for next_line in lines[i + 1:]:
                if next_line.rstrip(":").lower() in [
                    "projects", "skills", "education",
                    "certifications", "awards"
                ]:
                    break

                experience_lines.append(next_line)

            if experience_lines:
                return "\n".join(experience_lines)

    # Otherwise, look for sentences describing actual work.
    evidence = []

    for line in lines:
        sentences = re.split(r"(?<=[.!?])\s+", line)

        for sentence in sentences:
            sentence = sentence.strip()

            if any(phrase in sentence.lower() for phrase in [
                "worked on",
                "developed",
                "built",
                "implemented",
                "experience using",
                "experience with"
            ]):
                evidence.append(sentence)

    if evidence:
        return "\n".join(evidence)

    return None


def extract_experience_records(experience_text: str) -> list[dict]:
    lines = [
        line.strip()
        for line in experience_text.splitlines()
        if line.strip()
    ]

    records = []

    for line in lines:
        # Example: Junior Python Developer at Codecelix Company
        # from Apr 2026 – Present
        if " at " in line.lower():
            parts = re.split(
                r"\s+at\s+",
                line,
                maxsplit=1,
                flags=re.IGNORECASE
            )

            title = parts[0].strip()
            company_part = parts[1].strip()

            # Remove an experience claim accidentally included in the title.
            title = re.sub(
                r"\s+with\s+\d+\+?\s+years?\s+of\s+experience.*$",
                "",
                title,
                flags=re.IGNORECASE
            ).strip()

            company = company_part
            dates = None

            # Separate the company name from employment dates.
            if " from " in company_part.lower():
                company_parts = re.split(
                    r"\s+from\s+",
                    company_part,
                    maxsplit=1,
                    flags=re.IGNORECASE
                )

                company = company_parts[0].strip()
                dates = company_parts[1].strip()

            records.append({
                "company": company,
                "title": title,
                "dates": dates,
                "bullets": []
            })

    # Keep the original text if no job title/company line was found.
    if not records and lines:
        records.append({
            "company": None,
            "title": None,
            "dates": None,
            "bullets": lines
        })

    return records


def clean_resume_text(text: str) -> str:
    # Remove invisible zero-width characters
    text = text.replace("\u200b", "")

    lines = text.splitlines()

    section_headers = {
        "Experience",
        "Projects",
        "Skills",
        "Education",
        "Certifications",
        "Awards"
    }

    cleaned_lines = []
    current_line = ""
    previous_blank = False

    for raw_line in lines:
        line = raw_line.strip()

        # Empty line
        if not line:
            if current_line:
                cleaned_lines.append(current_line)
                current_line = ""

            cleaned_lines.append("")
            previous_blank = True
            continue

        # Major section header
        if line in section_headers:
            if current_line:
                cleaned_lines.append(current_line)
                current_line = ""

            cleaned_lines.append(line)
            previous_blank = False
            continue

        # New bullet
        if line.startswith("•"):
            if current_line:
                cleaned_lines.append(current_line)

            current_line = line

        # Continuation of a bullet caused by PDF line wrapping
        elif current_line.startswith("•") and not previous_blank:
            current_line += " " + line

        # Normal line
        else:
            if current_line:
                cleaned_lines.append(current_line)

            current_line = line

        previous_blank = False

    # Add final line
    if current_line:
        cleaned_lines.append(current_line)

    return "\n".join(cleaned_lines)

def analyze_resume(text: str) -> dict:
    text = clean_resume_text(text)

    experience_section = extract_experience_section(text)

    experience_records = []

    if experience_section:
        experience_records = extract_experience_records(
            experience_section
        )

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": experience_records
    }