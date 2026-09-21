import json
from collections import Counter, defaultdict
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

MIN_CV_FREQUENCY = 10
MAX_CANDIDATES = 100
MAX_CONTEXTS_PER_LABEL = 3
CONTEXT_WINDOW = 120


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


def build_alias_lookup(
    skill_dictionary: dict,
) -> set[str]:
    """
    Tạo tập các canonical skill và alias
    đã được normalize.
    """

    known_labels = set()

    for skill_name, skill_info in skill_dictionary.items():

        known_labels.add(
            normalize_text(skill_name)
        )

        for alias in skill_info.get(
            "aliases",
            [],
        ):
            known_labels.add(
                normalize_text(alias)
            )

    return known_labels


def collect_unmatched_candidates(
    known_labels: set[str],
):
    """
    Thu thập các label chưa match dictionary.

    Trả về:

        label_counter:
            label -> số CV xuất hiện

        contexts:
            label -> danh sách context mẫu
    """

    label_counter = Counter()

    contexts = defaultdict(list)

    json_files = RESUME_DIR.rglob("*.json")

    for file_path in json_files:

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        text = data.get(
            "text",
            "",
        )

        annotations = data.get(
            "annotations",
            [],
        )

        labels_in_cv = set()

        for annotation in annotations:

            if len(annotation) != 3:
                continue

            start, end, label = annotation

            if not label.startswith("SKILL:"):
                continue

            skill = label.replace(
                "SKILL:",
                "",
                1,
            ).strip()

            normalized_skill = normalize_text(
                skill
            )

            if not normalized_skill:
                continue

            # Bỏ qua skill đã biết
            if normalized_skill in known_labels:
                continue

            # Một label chỉ tính một lần / CV
            labels_in_cv.add(
                normalized_skill
            )

            # Lấy context xung quanh annotation
            context_start = max(
                0,
                start - CONTEXT_WINDOW,
            )

            context_end = min(
                len(text),
                end + CONTEXT_WINDOW,
            )

            context = text[
                context_start:context_end
            ].replace(
                "\n",
                " ",
            )

            context = " ".join(
                context.split()
            )

            if (
                len(contexts[normalized_skill])
                < MAX_CONTEXTS_PER_LABEL
            ):
                contexts[
                    normalized_skill
                ].append(context)

        label_counter.update(
            labels_in_cv
        )

    return label_counter, contexts


def main() -> None:

    skill_dictionary = load_skill_dictionary()

    known_labels = build_alias_lookup(
        skill_dictionary
    )

    label_counter, contexts = (
        collect_unmatched_candidates(
            known_labels
        )
    )

    candidates = [
        (label, count)
        for label, count
        in label_counter.items()
        if count >= MIN_CV_FREQUENCY
    ]

    candidates.sort(
        key=lambda item: (
            -item[1],
            item[0],
        )
    )

    candidates = candidates[
        :MAX_CANDIDATES
    ]

    print(
        f"Total unmatched labels: "
        f"{len(label_counter)}"
    )

    candidate_count = sum(
        1
        for count in label_counter.values()
        if count >= MIN_CV_FREQUENCY
    )

    print(
        f"Candidates with frequency >= "
        f"{MIN_CV_FREQUENCY}: "
        f"{candidate_count}"
    )

    print(
        f"Showing top {len(candidates)} candidates."
    )

    print("\n" + "=" * 80)

    for label, count in candidates:

        print(
            f"\nLABEL: {label}"
        )

        print(
            f"CV frequency: {count}"
        )

        print(
            "Contexts:"
        )

        for index, context in enumerate(
            contexts[label],
            start=1,
        ):
            print(
                f"  {index}. {context}"
            )

        print("-" * 80)


if __name__ == "__main__":
    main()