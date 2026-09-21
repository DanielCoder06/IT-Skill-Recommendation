import json
import sqlite3
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

RESUME_DIR = (
    BASE_DIR
    / "data"
    / "external"
    / "resumes"
)

DB_PATH = (
    BASE_DIR
    / "data"
    / "it_jobs.db"
)


SUSPICIOUS_LABELS = {
    "personal",
    "knowledge",
    "company",
    "nationality",
    "office",
    "project",
    "professional",
    "information",
    "team",
    "work",
    "education",
    "training",
    "college",
    "languages",
    "organization",
    "system",
    "management",
}


def load_current_skills() -> set[str]:
    connection = sqlite3.connect(DB_PATH)

    result = connection.execute(
        "SELECT name FROM skills"
    )

    skills = {
        row[0].strip().lower()
        for row in result.fetchall()
    }

    connection.close()

    return skills


def load_all_labels() -> Counter:
    label_counter = Counter()

    json_files = RESUME_DIR.rglob("*.json")

    for file_path in json_files:
        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        annotations = data.get(
            "annotations",
            [],
        )

        for annotation in annotations:
            if len(annotation) != 3:
                continue

            _, _, label = annotation

            if not label.startswith("SKILL:"):
                continue

            skill = label.replace(
                "SKILL:",
                "",
                1,
            ).strip()

            if skill:
                label_counter[
                    skill.lower()
                ] += 1

    return label_counter


def analyze_candidates() -> None:
    current_skills = load_current_skills()

    label_counter = load_all_labels()

    known_skills = Counter()
    suspicious_labels = Counter()
    unknown_candidates = Counter()

    for label, count in label_counter.items():

        if label in current_skills:
            known_skills[label] = count

        elif label in SUSPICIOUS_LABELS:
            suspicious_labels[label] = count

        else:
            unknown_candidates[label] = count

    print(
        f"Total unique labels: "
        f"{len(label_counter)}"
    )

    print(
        f"Known skills: "
        f"{len(known_skills)}"
    )

    print(
        f"Suspicious labels: "
        f"{len(suspicious_labels)}"
    )

    print(
        f"Unknown candidates: "
        f"{len(unknown_candidates)}"
    )

    print("\nKnown skills:")

    for skill, count in known_skills.most_common():
        print(
            f"{skill:40} {count}"
        )

    print("\nSuspicious labels:")

    for label, count in suspicious_labels.most_common():
        print(
            f"{label:40} {count}"
        )

    print(
        "\nTop 100 unknown candidates:"
    )

    for label, count in (
        unknown_candidates
        .most_common(100)
    ):
        print(
            f"{label:40} {count}"
        )


if __name__ == "__main__":
    analyze_candidates()