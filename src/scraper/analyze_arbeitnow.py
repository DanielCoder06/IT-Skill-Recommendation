import json
from pathlib import Path

from src.scraper.job_filter import is_it_job
from src.scraper.job_classifier import classify_job_level
from src.scraper.job_schema import JobRecord


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "raw_jobs.json"
)


def load_raw_jobs() -> list[dict]:
    with RAW_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def main() -> None:
    raw_jobs = load_raw_jobs()

    jobs = [
        JobRecord(
            title=job["title"],
            company=job["company_name"],
            description=job["description"],
            location=job["location"],
            url=job["url"], 
            experience="",
            skills=job.get("skills", []),
        )
        for job in raw_jobs
    ]

    it_jobs = [
        job
        for job in jobs
        if is_it_job(job)
    ]

    internship_jobs = [
        job
        for job in it_jobs
        if classify_job_level(job) == "internship"
    ]

    print("Tổng raw jobs:", len(jobs))
    print("IT jobs:", len(it_jobs))
    print("IT internship jobs:", len(internship_jobs))

    print("\nMột số IT internship jobs:")

    for job in internship_jobs[:10]:
        print(
            f"- {job.title} | "
            f"{job.company} | "
            f"{job.location}"
        )


if __name__ == "__main__":
    main()