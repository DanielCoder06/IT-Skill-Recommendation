import json
from collections import Counter
from pathlib import Path

from src.extractor.extractor_regex import extract_skills


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "clean_it_jobs.json"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "arbeitnow"
    / "it_jobs_with_skills.json"
)


def load_jobs() -> list[dict]:
    with INPUT_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def extract_skills_from_jobs(jobs: list[dict]) -> tuple[list[dict], Counter]:
    skill_counter = Counter()

    for job in jobs:
        description = job["description"]

        skills = extract_skills(description)

        job["skills"] = sorted(skills)

        skill_counter.update(skills)

    return jobs, skill_counter


def save_jobs(jobs: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            jobs,
            file,
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    jobs = load_jobs()

    jobs, skill_counter = extract_skills_from_jobs(jobs)

    save_jobs(jobs)

    print("========================================")
    print("SKILL EXTRACTION - ARBEITNOW")
    print("========================================")

    print(f"Tổng số IT jobs: {len(jobs)}")
    print()

    jobs_with_skills = sum(
        1 for job in jobs if job["skills"]
    )

    print(f"Jobs có ít nhất 1 skill: {jobs_with_skills}")
    print(
        f"Jobs không tìm thấy skill: "
        f"{len(jobs) - jobs_with_skills}"
    )

    print()
    print("Top skills:")

    for skill, count in skill_counter.most_common(20):
        print(f"- {skill}: {count} jobs")

    print()
    print(f"Đã lưu kết quả vào: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()