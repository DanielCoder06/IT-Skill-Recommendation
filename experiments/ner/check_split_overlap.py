import hashlib
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "experiments" / "ner" / "data"


def load_documents(path: Path):
    documents = {}

    with open(path, encoding="utf-8") as file:
        for index, line in enumerate(file):
            item = json.loads(line)
            text = item["text"]

            text_hash = hashlib.sha256(
                text.encode("utf-8")
            ).hexdigest()

            documents[text_hash] = {
                "index": index,
                "text": text,
            }

    return documents


train = load_documents(DATA_DIR / "train.jsonl")
dev = load_documents(DATA_DIR / "dev.jsonl")
test = load_documents(DATA_DIR / "test.jsonl")


train_dev = set(train) & set(dev)
train_test = set(train) & set(test)
dev_test = set(dev) & set(test)


print("=" * 60)
print("EXACT DOCUMENT OVERLAP")
print("=" * 60)

print(f"Train documents: {len(train)}")
print(f"Dev documents:   {len(dev)}")
print(f"Test documents:  {len(test)}")

print()

print(f"Train ∩ Dev:  {len(train_dev)}")
print(f"Train ∩ Test: {len(train_test)}")
print(f"Dev ∩ Test:   {len(dev_test)}")


if train_dev:
    print("\nExamples of Train ∩ Dev:")

    for i, text_hash in enumerate(train_dev):
        train_item = train[text_hash]
        dev_item = dev[text_hash]

        print(f"\nExample {i + 1}")
        print(f"Train index: {train_item['index']}")
        print(f"Dev index:   {dev_item['index']}")
        print(f"Text preview: {train_item['text'][:200]!r}")

        if i >= 9:
            break