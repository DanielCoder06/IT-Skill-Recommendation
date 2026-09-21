import json
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parents[2]

CLEANED_DATASET_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "resumes"
    / "cleaned_annotations.json"
)


def normalize_text(value: str) -> str:
    """Normalize text before comparing annotation with text span."""
    return " ".join(value.lower().split())


def check_annotation(text: str, annotation: list) -> str:
    """Check whether one annotation matches its text span."""

    if len(annotation) != 3:
        return "invalid_annotation"

    start, end, label = annotation

    if not isinstance(start, int) or not isinstance(end, int):
        return "invalid_offset"

    if start < 0 or end > len(text) or start >= end:
        return "invalid_offset"

    if not isinstance(label, str):
        return "invalid_label"

    label_text = label.removeprefix("SKILL:").strip()
    extracted_text = text[start:end]

    if normalize_text(extracted_text) == normalize_text(label_text):
        return "exact_match"

    return "mismatch"


def profile_annotations() -> None:

    with CLEANED_DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    result_counter = Counter()
    mismatch_examples = []

    total_annotations = 0

    for index, data in enumerate(dataset, start=1):

        text = data.get("text", "")
        annotations = data.get("annotations", [])

        for annotation in annotations:

            total_annotations += 1

            result = check_annotation(
                text,
                annotation,
            )

            result_counter[result] += 1

            if (
                result == "mismatch"
                and len(mismatch_examples) < 20
            ):
                start, end, label = annotation

                extracted_text = text[start:end]

                mismatch_examples.append(
                    {
                        "cv_index": index,
                        "label": label,
                        "text_span": extracted_text,
                        "start": start,
                        "end": end,
                    }
                )

    print("=== CLEANED DATASET VALIDATION ===")
    print(f"Total CVs: {len(dataset)}")
    print(f"Total annotations: {total_annotations}")

    print("\nAnnotation consistency:")

    for result, count in result_counter.items():

        percentage = (
            count / total_annotations * 100
            if total_annotations
            else 0
        )

        print(
            f"{result:20}"
            f"{count:10}"
            f"{percentage:10.2f}%"
        )

    print("\nMismatch examples:")

    if not mismatch_examples:
        print("No mismatches found.")

    for example in mismatch_examples:

        print("-" * 60)
        print(f"CV index: {example['cv_index']}")
        print(f"Label: {example['label']}")
        print(f"Text span: {example['text_span']}")
        print(
            f"Offset: "
            f"{example['start']}:{example['end']}"
        )


if __name__ == "__main__":
    profile_annotations()