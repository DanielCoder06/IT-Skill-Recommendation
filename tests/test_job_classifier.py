from src.scraper.job_classifier import classify_job_level
from src.scraper.job_schema import JobRecord


def make_job(title: str, description: str = "") -> JobRecord:
    return JobRecord(
        title=title,
        company="Test Company",
        description=description,
        location="Remote",
        url="https://example.com/test",
        experience="",
    )


def test_internship():
    job = make_job("Python Intern")

    assert classify_job_level(job) == "internship"


def test_praktikum():
    job = make_job("Software Engineering Praktikum")

    assert classify_job_level(job) == "internship"


def test_werkstudent():
    job = make_job("Werkstudent Software Development")

    assert classify_job_level(job) == "internship"


def test_junior():
    job = make_job("Junior Software Engineer")

    assert classify_job_level(job) == "junior"


def test_entry_level():
    job = make_job("Entry-Level Data Analyst")

    assert classify_job_level(job) == "junior"


def test_senior():
    job = make_job("Senior Software Engineer")

    assert classify_job_level(job) == "senior"


def test_principal():
    job = make_job("Principal Software Engineer")

    assert classify_job_level(job) == "senior"


def test_unspecified():
    job = make_job("Software Engineer")

    assert classify_job_level(job) == "unspecified"
    
def test_senior_title_overrides_internship_in_description():
    job = make_job(
        "Senior Software Engineer",
        "Join our internship and training programs.",
    )

    assert classify_job_level(job) == "senior"


def test_staff_is_senior():
    job = make_job(
        "Staff Cloud Platform Engineer",
    )

    assert classify_job_level(job) == "senior"


def test_principal_is_senior():
    job = make_job(
        "Principal Software Engineer",
    )

    assert classify_job_level(job) == "senior"


def test_team_lead_is_senior():
    job = make_job(
        "Team Lead AI Engineering",
    )

    assert classify_job_level(job) == "senior"
    
def test_sr_is_senior():
    job = make_job("Sr. Software Engineer")
    assert classify_job_level(job) == "senior"