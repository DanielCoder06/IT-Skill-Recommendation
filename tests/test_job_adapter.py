from src.models.raw_job import RawJob
from src.scraper.job_adapter import (
    raw_job_to_job_record,
    raw_jobs_to_job_records,
)


def test_raw_job_to_job_record():
    raw_job = RawJob(
        source="arbeitnow",
        external_id="123",
        title="Python Developer",
        company="ABC Company",
        location="Berlin",
        description="Python backend development",
        job_url="https://example.com/job/123",
        experience="Intern",
    )

    job = raw_job_to_job_record(raw_job)

    assert job.title == "Python Developer"
    assert job.company == "ABC Company"
    assert job.location == "Berlin"
    assert job.description == "Python backend development"
    assert job.url == "https://example.com/job/123"
    assert job.experience == "Intern"
    assert job.skills == []


def test_raw_job_optional_company_and_location():
    raw_job = RawJob(
        source="arbeitnow",
        external_id="123",
        title="Python Developer",
        company=None,
        location=None,
        description="Python development",
        job_url="https://example.com/job/123",
    )

    job = raw_job_to_job_record(raw_job)

    assert job.company == "Unknown"
    assert job.location == "Unknown"


def test_raw_jobs_to_job_records():
    raw_jobs = [
        RawJob(
            source="arbeitnow",
            external_id="1",
            title="Python Developer",
            company="Company A",
            location="Berlin",
            description="Python",
            job_url="https://example.com/1",
        ),
        RawJob(
            source="arbeitnow",
            external_id="2",
            title="Data Analyst",
            company="Company B",
            location="Munich",
            description="SQL",
            job_url="https://example.com/2",
        ),
    ]

    jobs = raw_jobs_to_job_records(raw_jobs)

    assert len(jobs) == 2
    assert jobs[0].title == "Python Developer"
    assert jobs[1].title == "Data Analyst"