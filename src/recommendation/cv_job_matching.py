from src.recommendation.skill_gap import calculate_skill_gap


def match_cv_to_job(
    cv_skills: set[str],
    job_id: int,
):
    """
    Match a CV skill profile against a job.
    """

    return calculate_skill_gap(
        student_skills=cv_skills,
        job_id=job_id,
    )