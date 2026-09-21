import json
import sqlite3
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

CLEANED_DATASET_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "resumes"
    / "cleaned_annotations.json"
)

DB_PATH = BASE_DIR / "data" / "it_jobs.db"

PROFILE_OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "resumes"
    / "resume_skill_profiles.json"
)


# Những label rõ ràng có khả năng không phải skill.
# Đây chỉ là danh sách để profiling.
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


def normalize_text(value: str) -> str:
    """Chuẩn hóa text để so sánh label."""
    return " ".join(value.lower().strip().split())


def load_cleaned_dataset() -> list[dict]:
    """Load dataset đã được cleaning."""
    with CLEANED_DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def load_skill_annotations(data: dict) -> list[str]:
    """
    Lấy các skill label từ một CV.
    """
    annotations = data.get("annotations", [])

    skills = []

    for annotation in annotations:
        if len(annotation) != 3:
            continue

        _, _, label = annotation

        if not isinstance(label, str):
            continue

        if not label.startswith("SKILL:"):
            continue

        skill = label.replace(
            "SKILL:",
            "",
            1,
        ).strip()

        if skill:
            skills.append(skill)

    return skills


def load_current_skills() -> set[str]:
    """
    Load taxonomy skill hiện tại từ database.
    """
    connection = sqlite3.connect(DB_PATH)

    try:
        result = connection.execute(
            "SELECT name FROM skills"
        )

        return {
            normalize_text(row[0])
            for row in result.fetchall()
        }

    finally:
        connection.close()


def load_skill_lookup() -> dict[str, str]:
    """
    Tạo lookup:
    normalized skill -> tên skill canonical trong DB.
    """
    connection = sqlite3.connect(DB_PATH)

    try:
        result = connection.execute(
            "SELECT name FROM skills"
        )

        return {
            normalize_text(row[0]): row[0]
            for row in result.fetchall()
        }

    finally:
        connection.close()


def build_resume_skill_profiles(
    dataset: list[dict],
    skill_lookup: dict[str, str],
) -> list[dict]:
    """
    Tạo skill profile cho từng CV.

    Chỉ giữ những skill đã tồn tại
    trong taxonomy của database.
    """

    profiles = []

    for cv_index, data in enumerate(
        dataset,
        start=1,
    ):

        skills = load_skill_annotations(data)

        profile_skills = set()

        for skill in skills:

            normalized_skill = normalize_text(
                skill
            )

            canonical_skill = skill_lookup.get(
                normalized_skill
            )

            if canonical_skill:
                profile_skills.add(
                    canonical_skill
                )

        profiles.append(
            {
                "cv_id": cv_index,
                "skills": sorted(profile_skills),
            }
        )

    return profiles


def save_resume_skill_profiles(
    profiles: list[dict],
) -> None:
    """
    Lưu skill profile của toàn bộ CV.
    """

    PROFILE_OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with PROFILE_OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            profiles,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(
        "\nSkill profiles saved to:"
    )

    print(
        PROFILE_OUTPUT_PATH
    )


def print_frequency_distribution(
    cv_counter: Counter,
) -> None:
    """
    Thống kê số lượng label theo mức độ xuất hiện
    trong các CV.
    """

    thresholds = [
        1,
        5,
        10,
        50,
        100,
        500,
        1000,
    ]

    print(
        "\nLabel frequency distribution:"
    )

    for threshold in thresholds:

        count = sum(
            1
            for frequency in cv_counter.values()
            if frequency >= threshold
        )

        print(
            f"Labels appearing in >= {threshold:4} CVs: "
            f"{count}"
        )


def print_unmatched_labels(
    cv_counter: Counter,
    current_skills: set[str],
) -> None:
    """
    Hiển thị những label trong dataset
    chưa xuất hiện trong taxonomy hiện tại.
    """

    unmatched_labels = [
        (skill, count)
        for skill, count in cv_counter.items()
        if normalize_text(skill)
        not in current_skills
    ]

    unmatched_labels.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    print(
        "\nTop 50 labels not in current DB:"
    )

    for skill, count in unmatched_labels[:50]:

        print(
            f"{skill:40} {count}"
        )


def main() -> None:

    # ==================================================
    # 1. Load cleaned dataset
    # ==================================================

    dataset = load_cleaned_dataset()

    print(
        f"Dataset: {CLEANED_DATASET_PATH}"
    )

    print(
        f"Total CVs: {len(dataset)}"
    )

    annotation_counter = Counter()
    cv_counter = Counter()
    suspicious_counter = Counter()

    annotation_counts = []

    current_skills = load_current_skills()
    skill_lookup = load_skill_lookup()

    matched_skills = Counter()

    # ==================================================
    # 2. Process CVs for profiling
    # ==================================================

    for data in dataset:

        skills = load_skill_annotations(data)

        annotation_counts.append(
            len(skills)
        )

        # ----------------------------------------------
        # Annotation frequency
        # ----------------------------------------------

        annotation_counter.update(
            skills
        )

        # ----------------------------------------------
        # CV frequency
        # Mỗi skill chỉ tính 1 lần / CV
        # ----------------------------------------------

        unique_skills = {
            normalize_text(skill)
            for skill in skills
        }

        cv_counter.update(
            unique_skills
        )

        # ----------------------------------------------
        # Suspicious labels
        # ----------------------------------------------

        for skill in unique_skills:

            if skill in SUSPICIOUS_LABELS:

                suspicious_counter[skill] += 1

        # ----------------------------------------------
        # Overlap với taxonomy hiện tại
        # ----------------------------------------------

        for skill in unique_skills:

            if skill in current_skills:

                matched_skills[skill] += 1

    # ==================================================
    # 3. General statistics
    # ==================================================

    total_annotations = sum(
        annotation_counts
    )

    average_annotations = (
        total_annotations / len(dataset)
        if dataset
        else 0
    )

    print(
        f"Total annotations: "
        f"{total_annotations}"
    )

    print(
        f"Average annotations/CV: "
        f"{average_annotations:.2f}"
    )

    print(
        f"Unique skill labels: "
        f"{len(annotation_counter)}"
    )

    # ==================================================
    # 4. Annotation frequency
    # ==================================================

    print(
        "\nTop 30 by annotation frequency:"
    )

    for skill, count in annotation_counter.most_common(30):

        print(
            f"{skill:40} {count}"
        )

    # ==================================================
    # 5. CV frequency
    # ==================================================

    print(
        "\nTop 30 by CV frequency:"
    )

    for skill, count in cv_counter.most_common(30):

        print(
            f"{skill:40} {count}"
        )

    # ==================================================
    # 6. Suspicious labels
    # ==================================================

    print(
        "\nSuspicious labels:"
    )

    for skill, count in suspicious_counter.most_common():

        print(
            f"{skill:40} {count}"
        )

    # ==================================================
    # 7. Overlap with current DB
    # ==================================================

    print(
        "\nOverlap with current DB skills:"
    )

    print(
        f"Matched labels: "
        f"{len(matched_skills)}"
    )

    for skill, count in matched_skills.most_common():

        print(
            f"{skill:40} {count}"
        )

    # ==================================================
    # 8. Frequency distribution
    # ==================================================

    print_frequency_distribution(
        cv_counter
    )

    # ==================================================
    # 9. Labels not in current DB
    # ==================================================

    print_unmatched_labels(
        cv_counter,
        current_skills,
    )

    # ==================================================
    # 10. Build CV Skill Profiles
    # IMPORTANT:
    # Phải nằm ngoài vòng for dataset ở trên.
    # ==================================================

    profiles = build_resume_skill_profiles(
        dataset,
        skill_lookup,
    )

    save_resume_skill_profiles(
        profiles
    )

    profiles_with_skills = sum(
        1
        for profile in profiles
        if profile["skills"]
    )

    print(
        "\nCVs with at least one recognized skill: "
        f"{profiles_with_skills}/{len(profiles)}"
    )

    # ==================================================
    # 11. Sample profiles
    # ==================================================

    print(
        "\nSample skill profiles:"
    )

    for profile in profiles[:10]:

        print(
            f"CV {profile['cv_id']}: "
            f"{profile['skills']}"
        )


if __name__ == "__main__":
    main()