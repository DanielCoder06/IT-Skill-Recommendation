import json
from pathlib import Path

from src.scraper.job_filter import is_it_job
from src.scraper.job_schema import JobRecord


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "raw_jobs.json"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "it_jobs.json"
)


def load_raw_jobs() -> list[dict]:
    with RAW_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def export_it_jobs() -> list[dict]:
    raw_jobs = load_raw_jobs()

    it_jobs = []

    for job in raw_jobs:
        job_record = JobRecord(
            title=job["title"],
            company=job["company_name"],
            description=job["description"],
            location=job["location"],
            url=job["url"],
            experience="",
        )

        if is_it_job(job_record):
            it_jobs.append(job)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            it_jobs,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return it_jobs


def main() -> None:
    it_jobs = export_it_jobs()

    print("Tổng raw jobs:", 250)
    print("IT jobs:", len(it_jobs))
    print(f"Đã lưu: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()