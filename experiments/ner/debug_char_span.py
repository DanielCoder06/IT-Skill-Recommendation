import json
from pathlib import Path

import spacy


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "experiments" / "ner" / "data"


def debug_file(path: Path):
    nlp = spacy.blank("en")

    print(f"\n{'=' * 70}")
    print(path.name)
    print(f"{'=' * 70}")

    with open(path, encoding="utf-8") as file:
        for doc_id, line in enumerate(file):
            item = json.loads(line)

            text = item["text"]
            doc = nlp.make_doc(text)

            for start, end, label in item["entities"]:
                span = doc.char_span(
                    start,
                    end,
                    label=label,
                    alignment_mode="contract",
                )

                if span is None:
                    continue

                entity_text = text[start:end]
                converted_text = span.text

                if converted_text != converted_text.strip():
                    print(f"\nDocument: {doc_id}")
                    print(f"Original: {entity_text!r}")
                    print(f"Converted: {converted_text!r}")
                    print(f"Original span: {start}:{end}")
                    print(
                        f"Token span: "
                        f"{span.start}:{span.end}"
                    )


if __name__ == "__main__":
    debug_file(DATA_DIR / "train.jsonl")
    debug_file(DATA_DIR / "dev.jsonl")