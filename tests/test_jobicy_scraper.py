from unittest.mock import Mock, patch

from src.models.raw_job import RawJob
from src.scraper.jobicy_scraper import JobicyScraper


def test_jobicy_scraper_maps_response_to_raw_job():
    mock_response = Mock()

    mock_response.json.return_value = {
        "jobs": [
            {
                "id": 123456,
                "url": "https://jobicy.com/jobs/python-developer",
                "jobTitle": "Python Developer",
                "companyName": "Example Company",
                "jobIndustry": [
                    "Software Development",
                ],
                "jobType": [
                    "full-time",
                ],
                "jobGeo": "Worldwide",
                "jobLevel": "Mid-level",
                "jobExcerpt": "Python developer",
                "jobDescription": (
                    "<p>Build Python applications.</p>"
                    "<ul><li>Python</li></ul>"
                ),
                "pubDate": "2026-09-29T10:00:00+00:00",
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "src.scraper.jobicy_scraper.requests.get",
        return_value=mock_response,
    ) as mock_get:

        scraper = JobicyScraper()
        jobs = scraper.scrape()

    mock_get.assert_called_once()

    assert len(jobs) == 1

    job = jobs[0]

    assert isinstance(job, RawJob)

    assert job.source == "jobicy"
    assert job.external_id == "123456"
    assert job.title == "Python Developer"
    assert job.company == "Example Company"
    assert job.location == "Worldwide"

    assert job.description == (
        "Build Python applications.\n"
        "Python"
    )
    assert job.job_url == (
        "https://jobicy.com/jobs/python-developer"
    )

    assert job.employment_type == "full-time"
    assert job.experience == "Mid-level"
    assert job.remote is True

    assert job.tags == [
        "Software Development",
    ]

    assert job.raw_data["id"] == 123456


def test_jobicy_scraper_handles_missing_optional_fields():
    mock_response = Mock()

    mock_response.json.return_value = {
        "jobs": [
            {
                "id": 1,
                "url": "https://jobicy.com/jobs/example",
                "jobTitle": "Developer",
                "jobDescription": "<p>Developer role.</p>",
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "src.scraper.jobicy_scraper.requests.get",
        return_value=mock_response,
    ):

        scraper = JobicyScraper()
        jobs = scraper.scrape()

    assert len(jobs) == 1

    job = jobs[0]

    assert job.company is None
    assert job.location is None
    assert job.experience is None
    assert job.employment_type == ""
    assert job.tags == []
    assert job.remote is True