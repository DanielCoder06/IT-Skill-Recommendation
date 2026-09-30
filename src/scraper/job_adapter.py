from src.models.raw_job import RawJob
from src.scraper.job_schema import JobRecord


def raw_job_to_job_record(job: RawJob) -> JobRecord:
    """
    Convert a RawJob from a data source into the internal JobRecord model.
    """

    return JobRecord(
        title=job.title,
        company=job.company or "Unknown",
        description=job.description,
        location=job.location or "Unknown",
        url=job.job_url,
        experience=job.experience or "",
    )


def raw_jobs_to_job_records(
    jobs: list[RawJob],
) -> list[JobRecord]:
    """
    Convert multiple RawJob objects into JobRecord objects.
    """

    return [
        raw_job_to_job_record(job)
        for job in jobs
    ]