import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

ARBEITNOW_JOBS_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "it_jobs_with_skills.json"
)


def load_jobs() -> list[dict]:
    with ARBEITNOW_JOBS_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)