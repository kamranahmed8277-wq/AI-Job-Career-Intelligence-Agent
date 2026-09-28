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

    if lines:
        name = lines[0].strip()

        if re.fullmatch(r"[A-Za-z ]+", name):
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


def extract_education(text: str) -> dict | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    try:
        education_index = lines.index("Education")
    except ValueError:
        return None

    education_lines = lines[education_index + 1:]

    if len(education_lines) < 4:
        return None

    institution = education_lines[0]
    degree = education_lines[1]
    location = education_lines[2]
    years = education_lines[3]

    return {
        "institution": institution,
        "degree": degree,
        "location": location,
        "years": years
    }


def extract_experience_section(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    try:
        start_index = lines.index("Experience")
    except ValueError:
        return None

    end_index = len(lines)

    section_headers = [
        "Projects",
        "Skills",
        "Education",
        "Certifications",
        "Awards"
    ]

    for i in range(start_index + 1, len(lines)):
        if lines[i] in section_headers:
            end_index = i
            break

    experience_lines = lines[start_index + 1:end_index]

    if not experience_lines:
        return None

    return "\n".join(experience_lines)


def extract_experience_records(experience_text: str) -> list[dict]:
    lines = [
        line.strip()
        for line in experience_text.splitlines()
        if line.strip()
    ]

    records = []

    date_pattern = r"^[A-Z][a-z]{2,9}\s+\d{4}\s*[–-]\s*(?:Present|[A-Z][a-z]{2,9}\s+\d{4})$"

    header_lines = []

    for line in lines:

        # 1. Detect date
        if re.fullmatch(date_pattern, line):

            if len(header_lines) >= 2:

                company = header_lines[-2]
                title = header_lines[-1]

                record = {
                    "company": company,
                    "title": title,
                    "dates": line,
                    "bullets": []
                }

                records.append(record)

            header_lines = []

        # 2. Detect bullet
        elif line.startswith("•"):

            if records:
                bullet = line.lstrip("•").strip()
                records[-1]["bullets"].append(bullet)

        # 3. Company/title lines
        else:
            header_lines.append(line)

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