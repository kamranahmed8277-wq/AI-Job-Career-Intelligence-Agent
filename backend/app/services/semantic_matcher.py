from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load the model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


def calculate_semantic_similarity(
    resume_text: str,
    job_description: str,
) -> dict:
    """Compare resume text and job-description text by meaning."""

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("Resume text must not be empty.")

    if (
        not isinstance(job_description, str)
        or not job_description.strip()
    ):
        raise ValueError("Job description must not be empty.")

    model = get_model()

    embeddings = model.encode(
        [resume_text.strip(), job_description.strip()],
        normalize_embeddings=True,
    )

    resume_embedding = embeddings[0]
    job_embedding = embeddings[1]

    similarity = float(np.dot(resume_embedding, job_embedding))

    # Similarity values can have tiny floating-point errors.
    similarity = float(np.clip(similarity, -1.0, 1.0))

    return {
        "similarity_score": round(similarity, 4),
        "similarity_percentage": round(similarity * 100, 2),
        "model": MODEL_NAME,
    }
