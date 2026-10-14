
import re

from backend.app.services.semantic_matcher import (
    calculate_semantic_similarity,
)

DEFAULT_SIMILARITY_THRESHOLD = 0.45


def extract_resume_evidence(
    resume_text: str,
) -> list[dict[str, str]]:
    """Split resume text into evidence items with section labels."""

    if not isinstance(resume_text, str) or not resume_text.strip():
        return []

    parts = re.split(r"[\r\n]+|(?<=[.!?])\s+", resume_text)

    evidence = []
    current_section = "other"

    for part in parts:
        cleaned = part.strip()

        if not cleaned:
            continue

        heading = cleaned.rstrip(":").lower()

        if heading in {
            "skills",
            "technical skills",
            "core skills",
            "skills and technologies",
        }:
            current_section = "skills"
            continue

        if heading in {
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "projects",
            "personal projects",
        }:
            current_section = "experience"
            continue

        # Handle headings that include content on the same line.
        if re.match(
            r"^(skills|technical skills|core skills)\s*:",
            cleaned,
            re.IGNORECASE,
        ):
            current_section = "skills"
            cleaned = re.sub(
                r"^(skills|technical skills|core skills)\s*:\s*",
                "",
                cleaned,
                flags=re.IGNORECASE,
            ).strip()

        elif re.match(
            r"^(experience|work experience|professional experience|projects|personal projects)\s*:",
            cleaned,
            re.IGNORECASE,
        ):
            current_section = "experience"
            cleaned = re.sub(
                r"^(experience|work experience|professional experience|projects|personal projects)\s*:\s*",
                "",
                cleaned,
                flags=re.IGNORECASE,
            ).strip()

        if cleaned:
            evidence.append({
                "text": cleaned,
                "section": current_section,
            })

    return evidence


def match_requirements_to_resume(
    resume_text: str,
    requirements: list[str],
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    requirement_type: str = "skill",
) -> list[dict]:
    """Find the strongest relevant resume evidence for each requirement."""

    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Threshold must be between 0 and 1.")

    evidence_items = extract_resume_evidence(resume_text)
    results = []

    for requirement in requirements:
        if not isinstance(requirement, str) or not requirement.strip():
            continue

        requirement = requirement.strip()

        if not evidence_items:
            results.append({
                "requirement": requirement,
                "evidence": None,
                "similarity_score": None,
                "status": "insufficient_evidence",
            })
            continue

        # Prefer skills-section evidence for short skill requirements.
        is_short_requirement = len(requirement.split()) <= 3
        if is_short_requirement:
            preferred_items = [
                item for item in evidence_items
                if item["section"] == "skills"
            ]
            candidates = preferred_items or evidence_items
        else:
            preferred_items = [
                item for item in evidence_items
                if item["section"] == "experience"
            ]
            candidates = preferred_items or evidence_items

        best_evidence = None
        best_score = -1.0
        exact_match_found = False

        # Search all preferred candidates before falling back to semantics.
        for item in candidates:
            evidence = item["text"]

            if re.search(
                rf"(?<!\w){re.escape(requirement)}(?!\w)",
                evidence,
                re.IGNORECASE,
            ):
                best_evidence = evidence
                best_score = 1.0
                exact_match_found = True
                break

        if not exact_match_found:
            for item in candidates:
                evidence = item["text"]

                comparison = calculate_semantic_similarity(
                    evidence,
                    requirement,
                )
                score = comparison["similarity_score"]

                if score > best_score:
                    best_score = score
                    best_evidence = evidence

        results.append({
            "requirement": requirement,
            "evidence": best_evidence,
            "similarity_score": round(best_score, 4),
            "status": (
                "potential_match"
                if best_score >= threshold
                else "no_strong_evidence"
            ),
        })

    return results
