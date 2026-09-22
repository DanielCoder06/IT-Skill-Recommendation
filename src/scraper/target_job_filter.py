from src.scraper.job_filter import is_it_job
from src.scraper.job_classifier import classify_job_level
from src.scraper.job_schema import JobRecord


def is_target_internship(job: JobRecord) -> bool:
    """
    Return True when a job is both an IT job and an internship.
    """
    return is_it_job(job) and classify_job_level(job) == "internship"


def filter_target_internships(
    jobs: list[JobRecord],
) -> list[JobRecord]:
    """
    Keep only IT internship jobs from a list of jobs.
    """
    return [job for job in jobs if is_target_internship(job)]