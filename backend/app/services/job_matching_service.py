
from backend.app.services.resume_analyzer import analyze_resume
from backend.app.services.job_description_analyzer import (
    analyze_job_description,

)
from backend.app.services.resume_job_matcher import (
    match_resume_to_job,
    assess_experience,
    assess_education,

)
from backend.app.services.requirement_matcher import (
    match_requirements_to_resume,
)
from backend.app.services.resume_analyzer import analyze_resume
from backend.app.services.job_description_analyzer import (
    analyze_job_description,
)
from backend.app.services.resume_job_matcher import (
    match_resume_to_job,
    assess_experience,
    assess_education,
)
from backend.app.services.semantic_matcher import (
    calculate_semantic_similarity,
)



def match_resume_with_job(
    resume_text: str,
    job_description: str
) -> dict:

    resume_analysis = analyze_resume(resume_text)
    job_analysis = analyze_job_description(job_description)

    # Assess skills using the existing keyword-based matcher.
    skill_match = match_resume_to_job(
        resume_analysis["skills"],
        job_analysis["required_skills"]
    )

    # Assess experience.
    experience_assessment = assess_experience(
        resume_analysis["experience"],
        job_analysis["required_experience"]
    )

    # Assess education.
    education_assessment = assess_education(
        resume_analysis["education"],
        job_analysis["education_requirements"]
    )

    # Compare the full resume and job description by meaning.
    semantic_match = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    # Compare individual skills and responsibilities with resume evidence.

    # Match required skills against resume evidence.
    skill_requirement_matches = match_requirements_to_resume(
        resume_text,
        job_analysis["required_skills"],
        requirement_type="skill",
    )

    responsibility_matches = match_requirements_to_resume(
        resume_text,
        job_analysis["responsibilities"],
        requirement_type="responsibility",
    )

    requirement_matches = (
            skill_requirement_matches + responsibility_matches
    )

    return {
        "resume_analysis": resume_analysis,
        "job_analysis": job_analysis,
        "match": skill_match,
        "semantic_match": semantic_match,
        "requirement_matches": requirement_matches,
        "job_fit_assessment": {
            "skills": skill_match,
            "experience": experience_assessment,
            "education": education_assessment,
        }
    }


