from pathlib import Path
from src.models.raw_job import RawJob
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

def test_extract_detail_description() -> None:
    html = """
    <div class="imy-5 paragraph">
        <h2>Mô tả công việc</h2>
        <h2>Role overview</h2>
        <p>Build AI applications.</p>
        <ul>
            <li>Develop Python services.</li>
            <li>Work with RAG pipelines.</li>
        </ul>
    </div>

    <div class="imy-5 paragraph">
        <h2>Yêu cầu công việc</h2>
        <h2>Required skills</h2>
        <ul>
            <li>Python</li>
            <li>Machine Learning</li>
        </ul>
    </div>
    """

    description = (
        ITviecScraper
        ._extract_detail_description(html)
    )

    assert "Mô tả công việc" in description
    assert "Build AI applications." in description
    assert "Python services." in description
    assert "RAG pipelines." in description
    assert "Yêu cầu công việc" in description
    assert "Machine Learning" in description

def test_enrich_job_detail(monkeypatch) -> None:
    job = RawJob(
        source="itviec",
        external_id="4508",
        title="AI Tech Lead",
        company="Money Forward Vietnam",
        location="Cần Thơ",
        description="",
        job_url="https://example.com/job",
    )

    html = """
    <div class="imy-5 paragraph">
        <h2>Mô tả công việc</h2>
        <p>Build AI applications.</p>
    </div>

    <div class="imy-5 paragraph">
        <h2>Yêu cầu công việc</h2>
        <ul>
            <li>Python</li>
            <li>Machine Learning</li>
        </ul>
    </div>
    """

    monkeypatch.setattr(
        ITviecScraper,
        "_fetch_detail_html",
        staticmethod(lambda url: html),
    )

    enriched_job = (
        ITviecScraper
        .enrich_job_detail(job)
    )

    assert job.description == ""

    assert (
        "Build AI applications."
        in enriched_job.description
    )

    assert (
        "Python"
        in enriched_job.description
    )

    assert (
        "Machine Learning"
        in enriched_job.description
    )

    assert enriched_job.title == job.title
    assert enriched_job.company == job.company
    assert enriched_job.job_url == job.job_url
