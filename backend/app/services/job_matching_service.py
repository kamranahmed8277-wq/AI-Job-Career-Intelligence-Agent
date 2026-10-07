from backend.app.services.resume_analyzer import analyze_resume
from backend.app.services.job_description_analyzer import (
    analyze_job_description,
)
from backend.app.services.resume_job_matcher import (
    match_resume_to_job,
)


def match_resume_with_job(
    resume_text: str,
    job_description: str
) -> dict:

    resume_analysis = analyze_resume(resume_text)

    job_analysis = analyze_job_description(
        job_description
    )

    match_result = match_resume_to_job(
        resume_analysis["skills"],
        job_analysis["required_skills"]
    )

    return {
        "resume_analysis": resume_analysis,
        "job_analysis": job_analysis,
        "match": match_result
    }