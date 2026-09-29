import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "experiments" / "ner" / "data"


def check_file(path: Path):
    print(f"\n=== {path.name} ===")

    invalid_count = 0

    with open(path, encoding="utf-8") as file:
        for doc_id, line in enumerate(file):
            item = json.loads(line)

            text = item["text"]

            for start, end, label in item["entities"]:
                entity_text = text[start:end]

                if entity_text != entity_text.strip():
                    invalid_count += 1

                    print(f"\nDocument: {doc_id}")
                    print(f"Entity: {entity_text!r}")
                    print(f"Span: {start}:{end}")
                    print(f"Label: {label}")

                    context_start = max(0, start - 50)
                    context_end = min(len(text), end + 50)

                    print(
                        f"Context: "
                        f"{text[context_start:context_end]!r}"
                    )

    print(f"\nTotal invalid: {invalid_count}")


if __name__ == "__main__":
    check_file(DATA_DIR / "train.jsonl")
    check_file(DATA_DIR / "dev.jsonl")
    check_file(DATA_DIR / "test.jsonl")