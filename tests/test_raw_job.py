from datetime import datetime

from src.models.raw_job import RawJob


def test_create_raw_job():
    job = RawJob(
        source="jobicy",
        external_id="12345",
        title="Python Developer",
        company="Example Company",
        location="Remote",
        description="Looking for a Python developer.",
        job_url="https://example.com/jobs/12345",
    )

    assert job.source == "jobicy"
    assert job.external_id == "12345"
    assert job.title == "Python Developer"
    assert job.company == "Example Company"
    assert job.location == "Remote"
    assert job.description == "Looking for a Python developer."
    assert job.job_url == "https://example.com/jobs/12345"


def test_optional_fields_have_default_values():
    job = RawJob(
        source="itviec",
        external_id=None,
        title="Backend Intern",
        company="Example",
        location="Ho Chi Minh City",
        description="Backend internship.",
        job_url="https://example.com/job",
    )

    assert job.posted_date is None
    assert job.employment_type is None
    assert job.experience is None
    assert job.remote is None
    assert job.tags == []
    assert job.raw_data == {}


def test_raw_data_is_preserved():
    raw_data = {
        "jobTitle": "Python Developer",
        "companyName": "Example",
        "jobType": ["Full-time"],
    }

    job = RawJob(
        source="jobicy",
        external_id="123",
        title="Python Developer",
        company="Example",
        location="Remote",
        description="Python development.",
        job_url="https://example.com/job/123",
        raw_data=raw_data,
    )

    assert job.raw_data == raw_data


def test_posted_date_and_tags():
    posted_date = datetime(2026, 9, 29)

    job = RawJob(
        source="jobicy",
        external_id="123",
        title="Data Analyst",
        company="Example",
        location="Remote",
        description="Data analysis.",
        job_url="https://example.com/job/123",
        posted_date=posted_date,
        employment_type="Full-time",
        experience="Junior",
        remote=True,
        tags=["Python", "SQL", "Data"],
    )

    assert job.posted_date == posted_date
    assert job.employment_type == "Full-time"
    assert job.experience == "Junior"
    assert job.remote is True
    assert job.tags == ["Python", "SQL", "Data"]