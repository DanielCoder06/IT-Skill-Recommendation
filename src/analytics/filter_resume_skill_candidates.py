from collections import Counter

from src.analytics.normalize_resume_labels import (
    build_alias_lookup,
    load_resume_labels,
    load_skill_dictionary,
)


MIN_CV_FREQUENCY = 10


NOISE_LABELS = {
    # Personal information
    "personal",
    "nationality",
    "gender",
    "marital status",
    "passport",
    "email",
    "mobile",
    "gmail",

    # CV structure
    "curriculum",
    "curriculum vitae",
    "work experience",
    "education",
    "qualification",
    "college",
    "board",
    "training",

    # Generic CV terms
    "company",
    "professional",
    "information",
    "project",
    "projects",
    "responsibilities",
    "activities",
}

def filter_candidates(
    label_counter: Counter,
    known_labels: set[str],
) -> list[tuple[str, int]]:
    candidates = []

    for label, frequency in label_counter.items():

        # Skip labels that are already known skills
        if label in known_labels:
            continue

        # Skip obvious noise
        if label in NOISE_LABELS:
            continue

        # Skip very rare labels
        if frequency < MIN_CV_FREQUENCY:
            continue

        candidates.append((label, frequency))

    candidates.sort(
        key=lambda item: (-item[1], item[0])
    )

    return candidates


def main():
    label_counter = load_resume_labels()

    skill_dictionary = load_skill_dictionary()
    alias_lookup = build_alias_lookup(skill_dictionary)

    known_labels = set(alias_lookup.keys())

    candidates = filter_candidates(
        label_counter,
        known_labels,
    )

    print(f"Total unique labels: {len(label_counter)}")
    print(f"Known/alias labels: {len(known_labels)}")
    print(f"Noise labels: {len(NOISE_LABELS)}")
    print(
        f"Potential candidates "
        f"(frequency >= {MIN_CV_FREQUENCY}): "
        f"{len(candidates)}"
    )

    print("\nTop 100 potential candidates:\n")

    for index, (label, frequency) in enumerate(
        candidates[:100],
        start=1,
    ):
        print(
            f"{index:3}. "
            f"{label:<35} "
            f"{frequency:>5} CVs"
        )


if __name__ == "__main__":
    main()