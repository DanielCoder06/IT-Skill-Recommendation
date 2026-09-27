import json
from pathlib import Path

from src.scraper.text_cleaner import clean_job_description


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "it_jobs.json"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "clean_it_jobs.json"
)


def main() -> None:
    with INPUT_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        jobs = json.load(file)

    for job in jobs:
        job["description"] = clean_job_description(
            job["description"]
        )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            jobs,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("Số IT jobs:", len(jobs))
    print(f"Đã lưu cleaned jobs vào: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()