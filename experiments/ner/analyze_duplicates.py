import hashlib
import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "experiments" / "ner" / "data"


def load_documents(path: Path):
    documents = []

    with open(path, encoding="utf-8") as file:
        for index, line in enumerate(file):
            item = json.loads(line)

            text = item["text"]

            text_hash = hashlib.sha256(
                text.encode("utf-8")
            ).hexdigest()

            documents.append(
                {
                    "index": index,
                    "hash": text_hash,
                    "text": text,
                }
            )

    return documents


all_documents = []

for name in ("train", "dev", "test"):
    documents = load_documents(DATA_DIR / f"{name}.jsonl")

    for item in documents:
        item["split"] = name
        all_documents.append(item)


hash_counter = Counter(
    item["hash"]
    for item in all_documents
)


duplicate_groups = {
    text_hash: count
    for text_hash, count in hash_counter.items()
    if count > 1
}


print("=" * 60)
print("DATASET DUPLICATE ANALYSIS")
print("=" * 60)

print(f"Total records: {len(all_documents)}")
print(f"Unique texts: {len(hash_counter)}")
print(f"Duplicate groups: {len(duplicate_groups)}")

duplicate_records = sum(
    count - 1
    for count in duplicate_groups.values()
)

print(f"Duplicate records: {duplicate_records}")


split_counter = Counter()

for item in all_documents:
    if item["hash"] in duplicate_groups:
        split_counter[
            (
                item["hash"],
                item["split"],
            )
        ] += 1


print("\nExamples:")
print("-" * 60)

shown = 0

for text_hash, count in duplicate_groups.items():
    items = [
        item
        for item in all_documents
        if item["hash"] == text_hash
    ]

    splits = Counter(
        item["split"]
        for item in items
    )

    print(f"\nOccurrences: {count}")
    print(f"Splits: {dict(splits)}")
    print(f"Preview: {items[0]['text'][:200]!r}")

    shown += 1

    if shown >= 20:
        break