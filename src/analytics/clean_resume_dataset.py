import json
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RESUME_DIR = BASE_DIR / "data" / "external" / "resumes"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "resumes"

MAPPING_PATH = BASE_DIR / "config" / "resume_label_mapping.json"
OUTPUT_PATH = OUTPUT_DIR / "cleaned_annotations.json"


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def load_mapping():
    with MAPPING_PATH.open("r", encoding="utf-8") as file:
        return {
            normalize_text(key): value
            for key, value in json.load(file).items()
        }


def clean_dataset():
    mapping = load_mapping()

    cleaned_resumes = []

    stats = Counter()

    for file_path in RESUME_DIR.rglob("*.json"):
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        text = data.get("text", "")
        annotations = data.get("annotations", [])

        cleaned_annotations = []

        for annotation in annotations:
            if len(annotation) != 3:
                continue

            start, end, label = annotation

            if not label.startswith("SKILL:"):
                continue

            skill = label.replace("SKILL:", "", 1).strip()
            normalized_skill = normalize_text(skill)

            action = mapping.get(normalized_skill)

            if action == "REMOVE":
                stats["removed"] += 1
                continue

            if action == "REVIEW":
                stats["review"] += 1
                cleaned_annotations.append(annotation)
                continue

            if action:
                cleaned_annotations.append(annotation)
                stats["mapped"] += 1
                continue

            cleaned_annotations.append(annotation)
            stats["unchanged"] += 1

        cleaned_resumes.append(
            {
                "text": text,
                "annotations": cleaned_annotations,
            }
        )

        stats["cv_count"] += 1
        stats["original_annotations"] += len(annotations)
        stats["cleaned_annotations"] += len(cleaned_annotations)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            cleaned_resumes,
            file,
            ensure_ascii=True,
            indent=2,
        )

    return stats


def main():
    stats = clean_dataset()

    print("=== RESUME CLEANING ===")
    print(f"CVs: {stats['cv_count']}")
    print(f"Original annotations: {stats['original_annotations']}")
    print(f"Cleaned annotations: {stats['cleaned_annotations']}")
    print(f"Mapped: {stats['mapped']}")
    print(f"Removed: {stats['removed']}")
    print(f"Review: {stats['review']}")
    print(f"Unchanged: {stats['unchanged']}")
    print(f"\nOutput: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()