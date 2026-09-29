# -*- coding: utf-8 -*-

import glob
import json
import random
from pathlib import Path


from skill_matcher import SkillMatcher


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RESUME_DIR = (
    BASE_DIR
    / "data"
    / "external"
    / "resumes"
    / "ResumesJsonAnnotated"
)

OUTPUT_DIR = BASE_DIR / "experiments" / "ner" / "data"

SKILL_DICTIONARY_PATH = (
    BASE_DIR
    / "config"
    / "skills_dictionary.json"
)


# ============================================================
# DATASET CONFIGURATION
# ============================================================

RANDOM_SEED = 42

TRAIN_RATIO = 0.85
DEV_RATIO = 0.075
TEST_RATIO = 0.075

MAX_TEXT_LENGTH = 20_000


# ============================================================
# HELPERS
# ============================================================

def load_resume_text(json_path: Path) -> str | None:
    """
    Đọc text CV từ file JSON.

    Hỗ trợ một số cấu trúc JSON phổ biến:
        {"text": "..."}
        {"content": "..."}
    """

    try:
        with open(json_path, encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return None

    text = None

    if isinstance(data, dict):
        text = data.get("text")

        if text is None:
            text = data.get("content")

    if not isinstance(text, str):
        return None

    text = text.encode(
        "utf-8",
        "ignore",
    ).decode(
        "utf-8"
    ).strip()

    if not text:
        return None

    if len(text) > MAX_TEXT_LENGTH:
        return None

    return text


def create_example(text: str, matcher: SkillMatcher) -> dict | None:
    """
    Dùng SkillMatcher để tạo pseudo-label cho một CV.

    Chỉ giữ CV có ít nhất một skill.
    """

    matches = matcher.extract(text)

    if not matches:
        return None

    entities = []

    for match in matches:
        entities.append(
            [
                match["start"],
                match["end"],
                "SKILL",
            ]
        )

    entities.sort(key=lambda item: (item[0], item[1]))

    return {
        "text": text,
        "entities": entities,
    }


def deduplicate_examples(examples: list[dict]) -> list[dict]:
    """
    Loại duplicate CV dựa trên toàn bộ nội dung text.

    Nếu cùng một CV xuất hiện nhiều lần,
    chỉ giữ lại một bản.

    Việc này giúp tránh cùng một CV xuất hiện
    ở train/dev/test.
    """

    unique_examples: dict[str, dict] = {}

    for example in examples:
        text = example["text"]

        if text not in unique_examples:
            unique_examples[text] = example

    return list(unique_examples.values())


def split_dataset(
    examples: list[dict],
) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Shuffle và chia dataset thành:

        Train: 85%
        Dev:    7.5%
        Test:   7.5%

    Seed cố định để kết quả có thể tái lập.
    """

    random.seed(RANDOM_SEED)

    examples = examples.copy()
    random.shuffle(examples)

    total = len(examples)

    train_size = int(total * TRAIN_RATIO)
    dev_size = int(total * DEV_RATIO)

    train = examples[:train_size]

    dev_start = train_size
    dev_end = dev_start + dev_size

    dev = examples[dev_start:dev_end]
    test = examples[dev_end:]

    return train, dev, test


def save_jsonl(
    examples: list[dict],
    output_path: Path,
) -> None:
    """
    Lưu dataset dưới dạng JSONL.
    """

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        for example in examples:
            file.write(
                json.dumps(
                    example,
                    ensure_ascii=False,
                )
                + "\n"
            )


# ============================================================
# MAIN
# ============================================================

def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 60)
    print("AUTO-LABEL NER DATASET")
    print("=" * 60)

    print(f"Resume directory: {RESUME_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # --------------------------------------------------------
    # 1. Tìm CV
    # --------------------------------------------------------

    resume_files = glob.glob(
        str(RESUME_DIR / "**" / "*.json"),
        recursive=True,
    )

    print(f"Found {len(resume_files)} CV files.")
    print()

    if not resume_files:
        raise FileNotFoundError(
            f"Không tìm thấy CV JSON trong: {RESUME_DIR}"
        )

    # --------------------------------------------------------
    # 2. Load SkillMatcher
    # --------------------------------------------------------

    matcher = SkillMatcher(
        SKILL_DICTIONARY_PATH
    )

    # --------------------------------------------------------
    # 3. Auto-label
    # --------------------------------------------------------

    examples = []

    skipped_invalid = 0
    skipped_no_skill = 0

    for index, file_path in enumerate(
        resume_files,
        start=1,
    ):

        text = load_resume_text(
            Path(file_path)
        )

        if text is None:
            skipped_invalid += 1
            continue

        example = create_example(
            text,
            matcher,
        )

        if example is None:
            skipped_no_skill += 1
            continue

        examples.append(example)

    print("-" * 60)
    print("AUTO-LABEL RESULT")
    print("-" * 60)

    print(f"CV có skill:       {len(examples)}")
    print(f"CV invalid/skipped: {skipped_invalid}")
    print(f"CV không có skill:  {skipped_no_skill}")
    print()

    if not examples:
        raise RuntimeError(
            "Không tạo được dataset nào có skill."
        )

    # --------------------------------------------------------
    # 4. Deduplicate
    # --------------------------------------------------------

    before_dedup = len(examples)

    examples = deduplicate_examples(
        examples
    )

    after_dedup = len(examples)

    duplicate_count = (
        before_dedup - after_dedup
    )

    print("-" * 60)
    print("DEDUPLICATION")
    print("-" * 60)

    print(
        f"Before deduplication: {before_dedup}"
    )

    print(
        f"After deduplication:  {after_dedup}"
    )

    print(
        f"Duplicates removed:   {duplicate_count}"
    )

    print()

    # --------------------------------------------------------
    # 5. Split
    # --------------------------------------------------------

    train, dev, test = split_dataset(
        examples
    )

    print("-" * 60)
    print("DATASET SPLIT")
    print("-" * 60)

    print(
        f"train: {len(train)} CV"
    )

    print(
        f"dev:   {len(dev)} CV"
    )

    print(
        f"test:  {len(test)} CV"
    )

    print()

    # --------------------------------------------------------
    # 6. Save
    # --------------------------------------------------------

    train_path = OUTPUT_DIR / "train.jsonl"
    dev_path = OUTPUT_DIR / "dev.jsonl"
    test_path = OUTPUT_DIR / "test.jsonl"

    save_jsonl(
        train,
        train_path,
    )

    save_jsonl(
        dev,
        dev_path,
    )

    save_jsonl(
        test,
        test_path,
    )

    # --------------------------------------------------------
    # 7. Summary
    # --------------------------------------------------------

    total_entities = sum(
        len(example["entities"])
        for example in examples
    )

    print("-" * 60)
    print("DATASET CREATED")
    print("-" * 60)

    print(
        f"Total unique CV:       {len(examples)}"
    )

    print(
        f"Total SKILL entities:  {total_entities}"
    )

    print()

    print(
        f"Created: {train_path}"
    )

    print(
        f"Created: {dev_path}"
    )

    print(
        f"Created: {test_path}"
    )

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()