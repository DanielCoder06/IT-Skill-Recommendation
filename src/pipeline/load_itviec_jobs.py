import json
from pathlib import Path

from src.models.raw_job import RawJob


BASE_DIR = Path(__file__).resolve().parents[2]

ITVIEC_ENRICHED_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "itviec"
    / "it_jobs_enriched.json"
)


def load_itviec_jobs() -> list[RawJob]:
    with ITVIEC_ENRICHED_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    jobs = []

    for job in data["jobs"]:
        raw_job = RawJob(
            source=job["source"],
            external_id=job["external_id"],
            title=job["title"],
            company=job["company"],
            location=job["location"],
            description=job["description"],
            job_url=job["job_url"],
            posted_date=None,
            employment_type=job["employment_type"],
            experience=job["experience"],
            remote=job["remote"],
            tags=job["tags"],
            raw_data=job["raw_data"],
        )

        jobs.append(raw_job)

    return jobs