from src.scraper.job_classifier import classify_job_level
from src.scraper.job_schema import JobRecord


def make_job(
    title: str,
    description: str = "",
    experience: str = "",
) -> JobRecord:
    return JobRecord(
        title=title,
        company="Test Company",
        description=description,
        location="Remote",
        url="https://example.com/test",
        experience=experience,
    )


# ============================================================
# Title-based classification
# ============================================================


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


# ============================================================
# Source-provided experience classification
# ============================================================


def test_experience_internship():
    job = make_job(
        "Software Engineer",
        experience="Intern",
    )

    assert classify_job_level(job) == "internship"


def test_experience_internship_overrides_unspecified_title():
    job = make_job(
        "Software Developer",
        experience="Internship",
    )

    assert classify_job_level(job) == "internship"


def test_experience_junior():
    job = make_job(
        "Software Engineer",
        experience="Junior",
    )

    assert classify_job_level(job) == "junior"


def test_experience_entry_level():
    job = make_job(
        "Software Engineer",
        experience="Entry-Level, Junior",
    )

    assert classify_job_level(job) == "junior"


def test_experience_senior():
    job = make_job(
        "Software Engineer",
        experience="Senior",
    )

    assert classify_job_level(job) == "senior"


def test_experience_director_is_senior():
    job = make_job(
        "Engineering Manager",
        experience="Director",
    )

    assert classify_job_level(job) == "senior"


# ============================================================
# Priority between experience and title
# ============================================================


def test_experience_has_priority_over_title():
    job = make_job(
        "Software Engineer",
        experience="Senior",
    )

    assert classify_job_level(job) == "senior"


def test_senior_experience_overrides_junior_title():
    job = make_job(
        "Junior Software Engineer",
        experience="Senior",
    )

    assert classify_job_level(job) == "senior"


def test_internship_experience_overrides_unspecified_title():
    job = make_job(
        "Software Engineer",
        experience="Intern",
    )

    assert classify_job_level(job) == "internship"


# ============================================================
# Unknown source-provided levels
# ============================================================


def test_any_experience_is_unspecified():
    job = make_job(
        "Software Engineer",
        experience="Any",
    )

    assert classify_job_level(job) == "unspecified"


def test_midweight_experience_is_unspecified():
    job = make_job(
        "Software Engineer",
        experience="Midweight",
    )

    assert classify_job_level(job) == "unspecified"


def test_empty_experience_falls_back_to_title():
    job = make_job(
        "Junior Software Engineer",
        experience="",
    )

    assert classify_job_level(job) == "junior"