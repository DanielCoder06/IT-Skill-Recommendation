import json
import sys
import time
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

from src.scraper.itviec_scraper import ITviecScraper
from src.scraper.job_filter import is_it_job
from src.scraper.job_schema import JobRecord


BASE_DIR = Path(__file__).resolve().parents[1]

LISTING_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "itviec"
    / "Việc làm AI, Data.html"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "itviec"
    / "it_jobs_enriched.json"
)

DELAY_SECONDS = 1.0


def is_itviec_job(job) -> bool:
    job_record = JobRecord(
        title=job.title,
        company=job.company or "",
        description=job.description or "",
        location=job.location or "",
        url=job.job_url,
        experience=job.experience or "",
    )

    return is_it_job(job_record)


def raw_job_to_dict(job) -> dict:
    return {
        "source": job.source,
        "external_id": job.external_id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "job_url": job.job_url,
        "posted_date": (
            job.posted_date.isoformat()
            if job.posted_date
            else None
        ),
        "employment_type": job.employment_type,
        "experience": job.experience,
        "remote": job.remote,
        "tags": job.tags,
        "raw_data": job.raw_data,
    }


def main() -> None:
    scraper = ITviecScraper()

    print("=== ITVIEC FULL DETAIL ENRICHMENT ===")

    jobs = scraper.scrape(str(LISTING_PATH))

    it_jobs = [
        job
        for job in jobs
        if is_itviec_job(job)
    ]

    print(f"Listing jobs: {len(jobs)}")
    print(f"IT jobs: {len(it_jobs)}")
    print()

    enriched_jobs = []

    success_count = 0
    empty_count = 0
    failed_count = 0

    failures = []

    for index, job in enumerate(it_jobs, start=1):
        print(
            f"[{index}/{len(it_jobs)}] "
            f"{job.title}"
        )

        try:
            enriched_job = scraper.enrich_job_detail(job)

            description_length = len(
                enriched_job.description
            )

            print(
                f"  Description length: "
                f"{description_length}"
            )

            if not enriched_job.description.strip():
                empty_count += 1
                print("  RESULT: EMPTY")
            else:
                success_count += 1
                print("  RESULT: SUCCESS")

            enriched_jobs.append(
                raw_job_to_dict(enriched_job)
            )

        except Exception as exc:
            failed_count += 1

            print(
                f"  RESULT: FAILED - {exc}"
            )

            failures.append(
                {
                    "title": job.title,
                    "url": job.job_url,
                    "error": str(exc),
                }
            )

        if index < len(it_jobs):
            time.sleep(DELAY_SECONDS)

    output = {
        "source": "itviec",
        "total_listing_jobs": len(jobs),
        "total_it_jobs": len(it_jobs),
        "success": success_count,
        "empty": empty_count,
        "failed": failed_count,
        "failures": failures,
        "jobs": enriched_jobs,
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print("=== SUMMARY ===")
    print(f"Total IT jobs: {len(it_jobs)}")
    print(f"Success: {success_count}")
    print(f"Empty: {empty_count}")
    print(f"Failed: {failed_count}")

    print()
    print(
        f"Saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()