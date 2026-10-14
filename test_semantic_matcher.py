import pytest

from backend.app.services.semantic_matcher import (
    calculate_semantic_similarity,
)


def test_similar_text_returns_similarity_score():
    result = calculate_semantic_similarity(
        "Built backend services and REST APIs using Python.",
        "Developed and maintained Python REST API endpoints.",
    )

    assert -1.0 <= result["similarity_score"] <= 1.0
    assert 0.0 <= result["similarity_percentage"] <= 100.0
    assert result["model"] == (
        "sentence-transformers/all-MiniLM-L6-v2"
    )


def test_empty_resume_is_rejected():
    with pytest.raises(ValueError, match="Resume text"):
        calculate_semantic_similarity(
            "",
            "Develop Python applications.",
        )


def test_empty_job_description_is_rejected():
    with pytest.raises(ValueError, match="Job description"):
        calculate_semantic_similarity(
            "Built Python applications.",
            "   ",
        )
