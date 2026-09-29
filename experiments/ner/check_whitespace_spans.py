import spacy
from pathlib import Path
from spacy.tokens import DocBin

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "experiments" / "ner" / "data"


def check_file(path: Path):
    nlp = spacy.blank("en")
    doc_bin = DocBin().from_disk(path)

    print(f"\n=== {path.name} ===")

    count = 0

    for doc_id, doc in enumerate(doc_bin.get_docs(nlp.vocab)):
        for ent in doc.ents:
            entity_text = doc.text[ent.start_char:ent.end_char]

            if entity_text != entity_text.strip():
                count += 1

                start = max(0, ent.start_char - 50)
                end = min(len(doc.text), ent.end_char + 50)

                print(f"\nDocument: {doc_id}")
                print(f"Entity: {repr(entity_text)}")
                print(f"Label: {ent.label_}")
                print(f"Span: {ent.start_char}:{ent.end_char}")
                print(f"Context: {repr(doc.text[start:end])}")

    print(f"\nTotal invalid: {count}")


for name in ("train", "dev", "test"):
    check_file(DATA_DIR / f"{name}.spacy")
