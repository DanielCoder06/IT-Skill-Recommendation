# -*- coding: utf-8 -*-

import json
from pathlib import Path

import spacy
from spacy.tokens import DocBin


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "experiments" / "ner" / "data"


def convert(jsonl_path: Path, output_path: Path):
    nlp = spacy.blank("en")
    db = DocBin()

    total_entities = 0
    whitespace_adjusted = 0
    invalid_after_alignment = 0
    alignment_skipped = 0

    with open(jsonl_path, encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)

            text = item["text"]
            entities = item["entities"]

            doc = nlp.make_doc(text)
            spans = []

            for start, end, label in entities:
                total_entities += 1

                original_text = text[start:end]

                # Bỏ whitespace ở đầu/cuối annotation
                stripped_text = original_text.strip()

                if not stripped_text:
                    invalid_after_alignment += 1
                    continue

                left_trim = len(original_text) - len(
                    original_text.lstrip()
                )
                right_trim = len(original_text) - len(
                    original_text.rstrip()
                )

                if left_trim > 0 or right_trim > 0:
                    whitespace_adjusted += 1

                start += left_trim
                end -= right_trim

                span = doc.char_span(
                    start,
                    end,
                    label=label,
                    alignment_mode="contract",
                )

                if span is None:
                    alignment_skipped += 1
                    continue

                # Kiểm tra span sau alignment.
                # Nếu spaCy tạo entity bắt đầu/kết thúc bằng whitespace,
                # không đưa span lỗi vào dataset.
                if span.text != span.text.strip():
                    invalid_after_alignment += 1
                    continue

                spans.append(span)

            doc.ents = spans
            db.add(doc)

    db.to_disk(output_path)

    print(f"Created: {output_path}")
    print(f"Source entities: {total_entities}")
    print(f"Whitespace adjusted: {whitespace_adjusted}")
    print(f"Invalid after alignment: {invalid_after_alignment}")
    print(f"Alignment skipped: {alignment_skipped}")


if __name__ == "__main__":
    for name in ("train", "dev", "test"):
        convert(
            DATA_DIR / f"{name}.jsonl",
            DATA_DIR / f"{name}.spacy",
        )