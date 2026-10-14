
from backend.app.services.requirement_matcher import (
    extract_resume_evidence,
    match_requirements_to_resume,
)



def test_extract_resume_evidence_splits_text():
    text = (
        "Python developer.\n"
        "Built backend APIs using FastAPI."
    )

    evidence = extract_resume_evidence(text)

    assert {
        "text": "Python developer.",
        "section": "other",
    } in evidence

    assert {
        "text": "Built backend APIs using FastAPI.",
        "section": "other",
    } in evidence



def test_empty_resume_returns_insufficient_evidence():
    results = match_requirements_to_resume(
        "",
        ["Develop REST APIs"],
    )

    assert results[0]["status"] == "insufficient_evidence"
    assert results[0]["evidence"] is None


def test_invalid_threshold_is_rejected():
    try:
        match_requirements_to_resume(
            "Developed backend APIs.",
            ["Develop REST APIs"],
            threshold=1.5,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid threshold")
