from pathlib import Path
import sys
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from src.scraper.itviec_scraper import ITviecScraper
from src.scraper.job_adapter import raw_jobs_to_job_records
from src.scraper.job_filter import filter_it_jobs
from src.scraper.job_classifier import classify_job_level


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

    levels = Counter(
        classify_job_level(job)
        for job in it_jobs
    )

    print("=== ITVIEC PIPELINE ===")
    print(f"RawJob: {len(raw_jobs)}")
    print(f"JobRecord: {len(jobs)}")
    print(f"IT jobs: {len(it_jobs)}")

    print("\n=== JOB LEVEL ===")
    for level, count in sorted(levels.items()):
        print(f"{level}: {count}")

    print("\n=== FIRST 20 IT JOBS ===")

    for index, job in enumerate(
        it_jobs[:20],
        start=1,
    ):
        level = classify_job_level(job)

        print(
            f"{index}. "
            f"{job.title} | "
            f"{job.company} | "
            f"{job.location} | "
            f"{level}"
        )


if __name__ == "__main__":
    main()