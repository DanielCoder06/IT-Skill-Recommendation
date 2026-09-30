import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from src.scraper.itviec_scraper import ITviecScraper
from src.scraper.job_filter import is_it_job
from src.scraper.job_schema import JobRecord
from src.scraper.target_job_filter import filter_target_internships


LISTING_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "external"
    / "itviec"
    / "Việc làm AI, Data.html"
)

BATCH_SIZE = 5


def main() -> None:
    print("=== ITVIEC DETAIL ENRICHMENT BATCH TEST ===")

    scraper = ITviecScraper()

    jobs = scraper.scrape(str(LISTING_PATH))

    print("Listing jobs:", len(jobs))

    it_jobs = [
        job
        for job in jobs
        if is_it_job(
            JobRecord(
                title=job.title,
                company=job.company or "Unknown",
                description=job.description,
                location=job.location or "Unknown",
                url=job.job_url,
                experience="",
            )
        )
    ]

    print("IT jobs:", len(it_jobs))

    batch = it_jobs[:BATCH_SIZE]

    print("Batch size:", len(batch))
    print()

    success = 0
    empty = 0
    failed = 0

    enriched_jobs = []

    for index, job in enumerate(batch, start=1):
        print(
            f"[{index}/{len(batch)}] "
            f"{job.title}"
        )

        try:
            enriched_job = scraper.enrich_job_detail(
                job
            )

            description_length = len(
                enriched_job.description
            )

            print(
                "  Description length:",
                description_length,
            )

            if description_length == 0:
                empty += 1
                print("  RESULT: EMPTY")
            else:
                success += 1
                enriched_jobs.append(
                    enriched_job
                )
                print("  RESULT: SUCCESS")

        except Exception as exc:
            failed += 1
            print(
                "  RESULT: FAILED"
            )
            print(
                "  Error:",
                type(exc).__name__,
                str(exc),
            )

        print()

    print("=== SUMMARY ===")
    print("Total:", len(batch))
    print("Success:", success)
    print("Empty:", empty)
    print("Failed:", failed)

    if enriched_jobs:
        print("\n=== FIRST JOB PREVIEW ===")
        print(enriched_jobs[0].description[:1000])


if __name__ == "__main__":
    main()