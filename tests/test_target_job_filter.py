from src.scraper.job_schema import JobRecord
from src.scraper.target_job_filter import is_target_internship
from src.scraper.target_job_filter import filter_target_internships


def test_it_internship_is_target():
    job = JobRecord(
        title="Python Developer Intern",
        company="Tech Company",
        description="Looking for Python and SQL skills.",
        location="Remote",
        url="https://example.com/python-intern",
        experience="",
    )

    assert is_target_internship(job) is True


def test_non_it_internship_is_not_target():
    job = JobRecord(
        title="Marketing Intern",
        company="Marketing Company",
        description="Marketing and communication.",
        location="Remote",
        url="https://example.com/marketing-intern",
        experience="",
    )

    assert is_target_internship(job) is False


def test_senior_it_job_is_not_target():
    job = JobRecord(
        title="Senior Software Engineer",
        company="Tech Company",
        description="Python, Docker and Kubernetes.",
        location="Remote",
        url="https://example.com/senior-engineer",
        experience="",
    )

    assert is_target_internship(job) is False

def test_filter_target_internships():
    jobs = [
        JobRecord(
            title="Python Developer Intern",
            company="Tech Company",
            description="Python and SQL",
            location="Remote",
            url="https://example.com/1",
            experience="",
        ),
        JobRecord(
            title="Marketing Intern",
            company="Marketing Company",
            description="Marketing and communication",
            location="Remote",
            url="https://example.com/2",
            experience="",
        ),
        JobRecord(
            title="Senior Software Engineer",
            company="Tech Company",
            description="Python, Docker and Kubernetes",
            location="Remote",
            url="https://example.com/3",
            experience="",
        ),
    ]

    result = filter_target_internships(jobs)

    assert len(result) == 1
    assert result[0].title == "Python Developer Intern"