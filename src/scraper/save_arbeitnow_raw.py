import json
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parents[2]

API_URL = "https://www.arbeitnow.com/api/job-board-api"

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "raw_jobs.json"
)


def fetch_jobs() -> list[dict]:
    """
    Lấy toàn bộ job raw từ Arbeitnow API.
    """
    response = requests.get(
        API_URL,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    return data["data"]


def save_raw_jobs(jobs: list[dict]) -> None:
    """
    Lưu nguyên dữ liệu job từ API thành JSON.
    """
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
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


def main() -> None:
    jobs = fetch_jobs()

    print("Số jobs lấy được:", len(jobs))

    save_raw_jobs(jobs)

    print(
        f"Đã lưu raw jobs vào: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()