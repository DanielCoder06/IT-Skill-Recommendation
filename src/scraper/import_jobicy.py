from src.extractor.extractor_hybrid import extract_hybrid_skills
from src.extractor.extractor_regex import save_job_skills
from src.extractor.skill_merger import (
    get_skill_sources,
    merge_skills,
)
from src.pipeline.load_jobs_to_db import save_jobs_to_db
from src.scraper.job_adapter import raw_jobs_to_job_records
from src.scraper.job_filter import filter_it_jobs
from src.scraper.jobicy_scraper import JobicyScraper


def main() -> None:
    scraper = JobicyScraper()

    raw_jobs = scraper.scrape()
    jobs = raw_jobs_to_job_records(raw_jobs)
    it_jobs = filter_it_jobs(jobs)

    print(f"RAW jobs: {len(raw_jobs)}")
    print(f"IT jobs: {len(it_jobs)}")

    job_ids = save_jobs_to_db(it_jobs)

    for job in it_jobs:
        job_id = job_ids[job.url]

        result = extract_hybrid_skills(
            job.description
        )

        confirmed_skills = result[
            "confirmed_skills"
        ]

        suggested_skills = result[
            "suggested_skills"
        ]

        final_skills = merge_skills(
            confirmed_skills,
            suggested_skills,
        )

        skill_sources = get_skill_sources(
            confirmed_skills,
            suggested_skills,
        )

        save_job_skills(
            job_id,
            skill_sources,
        )

        print(f"\nJob: {job.title}")
        print(f"Confirmed: {sorted(confirmed_skills)}")
        print(f"Suggested: {sorted(suggested_skills)}")
        print(f"Final: {sorted(final_skills)}")


if __name__ == "__main__":
    main()
