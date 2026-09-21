import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

RESUME_DIR = (
    BASE_DIR
    / "data"
    / "external"
    / "resumes"
)

SKILLS_DICTIONARY_PATH = (
    BASE_DIR
    / "config"
    / "skills_dictionary.json"
)

RESUME_LABEL_MAPPING_PATH = (
    BASE_DIR
    / "config"
    / "resume_label_mapping.json"
)


def normalize_text(text: str) -> str:
    return " ".join(
        text.lower().strip().split()
    )


def load_skill_dictionary() -> dict:
    with SKILLS_DICTIONARY_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def load_resume_label_mapping() -> dict:
    with RESUME_LABEL_MAPPING_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def build_alias_lookup(
    skill_dictionary: dict,
) -> dict[str, str]:

    alias_lookup = {}

    for skill_name, skill_info in skill_dictionary.items():

        canonical_skill = skill_name

        alias_lookup[
            normalize_text(skill_name)
        ] = canonical_skill

        for alias in skill_info.get(
            "aliases",
            [],
        ):
            alias_lookup[
                normalize_text(alias)
            ] = canonical_skill

    return alias_lookup


def load_resume_labels() -> Counter:

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

        labels_in_cv = set()

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
                labels_in_cv.add(
                    normalize_text(skill)
                )

        label_counter.update(
            labels_in_cv
        )

    return label_counter


def classify_labels(
    label_counter: Counter,
    alias_lookup: dict[str, str],
    label_mapping: dict[str, str],
):

    matched = {}
    mapped = {}
    removed = {}
    review = {}
    unmatched = {}

    for label, count in label_counter.items():

        # 1. Match trực tiếp với skill dictionary
        if label in alias_lookup:

            canonical_skill = alias_lookup[label]

            matched[canonical_skill] = (
                matched.get(canonical_skill, 0)
                + count
            )

            continue

        # 2. Kiểm tra mapping thủ công
        if label in label_mapping:

            target = label_mapping[label]

            if target == "REMOVE":
                removed[label] = count

            elif target == "REVIEW":
                review[label] = count

            else:
                mapped[target] = (
                    mapped.get(target, 0)
                    + count
                )

            continue

        # 3. Chưa xử lý
        unmatched[label] = count

    return (
        matched,
        mapped,
        removed,
        review,
        unmatched,
    )


def print_section(
    title: str,
    data: dict,
):

    print(f"\n{title}")

    for label, count in sorted(
        data.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(
            f"{label:40} {count}"
        )


def main() -> None:

    skill_dictionary = load_skill_dictionary()

    alias_lookup = build_alias_lookup(
        skill_dictionary
    )

    label_mapping = load_resume_label_mapping()

    label_counter = load_resume_labels()

    (
        matched,
        mapped,
        removed,
        review,
        unmatched,
    ) = classify_labels(
        label_counter,
        alias_lookup,
        label_mapping,
    )

    print(
        f"Total unique dataset labels: "
        f"{len(label_counter)}"
    )

    print(
        f"Matched canonical skills: "
        f"{len(matched)}"
    )

    print(
        f"Mapped labels: "
        f"{len(mapped)}"
    )

    print(
        f"Removed labels: "
        f"{len(removed)}"
    )

    print(
        f"Review labels: "
        f"{len(review)}"
    )

    print(
        f"Unmatched labels: "
        f"{len(unmatched)}"
    )

    print_section(
        "\n=== MAPPED ===",
        mapped,
    )

    print_section(
        "\n=== REMOVED ===",
        removed,
    )

    print_section(
        "\n=== REVIEW ===",
        review,
    )

    print_section(
        "\n=== TOP 100 UNMATCHED ===",
        dict(
            sorted(
                unmatched.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:100]
        ),
    )


if __name__ == "__main__":
    main()