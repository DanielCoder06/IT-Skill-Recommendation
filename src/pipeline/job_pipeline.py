from src.pipeline.load_jobs import load_jobs
from src.pipeline.load_jobs_to_db import save_jobs_to_db
from src.scraper.job_schema import JobRecord

from src.extractor.extractor_hybrid import extract_hybrid_skills
from src.extractor.skill_merger import (
    merge_skills,
    get_skill_sources,
)
from src.extractor.extractor_regex import save_job_skills


def build_job_records() -> list[JobRecord]:
    raw_jobs = load_jobs()

    return [
        JobRecord(
            title=job["title"],
            company=job["company_name"],
            description=job["description"],
            location=job["location"],
            url=job["url"],
            experience=job.get("experience", ""),
            skills=job.get("skills", []),
        )
        for job in raw_jobs
    ]


def run_pipeline() -> None:
    jobs = build_job_records()

    job_ids = save_jobs_to_db(jobs)

    for job in jobs:
        job_id = job_ids.get(job.url)

        if job_id is None:
            print(f"Không tìm thấy job_id: {job.url}")
            continue

        hybrid_result = extract_hybrid_skills(
            job.description
        )

        confirmed_skills = hybrid_result[
            "confirmed_skills"
        ]

        suggested_skills = hybrid_result[
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
        print("Confirmed:")
        for skill in sorted(confirmed_skills):
            print(f"- {skill}")

        print("Suggested:")
        for skill in sorted(suggested_skills):
            print(f"- {skill}")

        print("Final:")
        for skill in sorted(final_skills):
            print(f"- {skill}")


if __name__ == "__main__":
    run_pipeline()