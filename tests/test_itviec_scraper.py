from pathlib import Path

from src.scraper.itviec_scraper import ITviecScraper


BASE_DIR = Path(__file__).resolve().parents[1]

HTML_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "itviec"
    / "Việc làm AI, Data.html"
)


def test_parse_itviec_html():
    scraper = ITviecScraper()

    jobs = scraper.scrape(str(HTML_PATH))

    assert len(jobs) > 0

    first_job = jobs[0]

    assert first_job.source == "itviec"
    assert first_job.title == (
        "AI Tech Lead — Context & Harness"
    )
    assert first_job.company == (
        "MONEY FORWARD VIETNAM CO.,LTD"
    )
    assert first_job.location == (
        "Ho Chi Minh - Ha Noi"
    )
    assert first_job.job_url.startswith(
        "https://itviec.com/viec-lam-it/"
    )

    assert "AI" in first_job.tags
    assert "RAG" in first_job.tags
    assert "LLM" in first_job.tags


def test_itviec_url_is_cleaned():
    scraper = ITviecScraper()

    jobs = scraper.scrape(str(HTML_PATH))

    url = jobs[0].job_url

    assert "?" not in url
    assert "gclid" not in url
    assert "utm_" not in url