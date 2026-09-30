from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from src.pipeline.load_jobs_to_db import save_jobs_to_db
from src.scraper.itviec_scraper import ITviecScraper
from src.scraper.job_adapter import raw_jobs_to_job_records
from src.scraper.job_filter import filter_it_jobs


HTML_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "itviec"
    / "Việc làm AI, Data.html"
)


def main() -> None:
    scraper = ITviecScraper()

    raw_jobs = scraper.scrape(
        str(HTML_PATH)
    )

    jobs = raw_jobs_to_job_records(
        raw_jobs
    )

    it_jobs = filter_it_jobs(jobs)

    print(f"RAW jobs: {len(raw_jobs)}")
    print(f"IT jobs: {len(it_jobs)}")

    job_ids = save_jobs_to_db(it_jobs)

    print(
        f"Saved jobs: {len(job_ids)}"
    )


if __name__ == "__main__":
    main()