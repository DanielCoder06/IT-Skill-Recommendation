import json
import re
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESUME_DIR = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "resumes"
    / "ResumesJsonAnnotated"
    / "ResumesJsonAnnotated"
)

SKILLS_DICTIONARY_PATH = (
    PROJECT_ROOT
    / "config"
    / "skills_dictionary.json"
)

MIN_FREQUENCY = 5
CONTEXT_WINDOW = 180

# Những label đã xác định là generic/non-skill.
IGNORED_LABELS = {
    "skills",
    "skill",
    "knowledge",
    "work",
    "project",
    "projects",
    "professional",
    "information",
    "company",
    "management",
    "team",
    "office",
    "technical",
    "engineering",
    "system",
    "systems",
    "technology",
    "development",
    "developing",
    "data",
    "software",
    "testing",
    "control",
    "tools",
    "problems",
    "solutions",
    "review",
    "proficiency",
    "expertise",
    "type",
    "phone",
    "music",
    "electronics",
    "equipment",
    "internet",
}

TECHNICAL_KEYWORDS = {
    "python",
    "java",
    "javascript",
    "sql",
    "programming",
    "software",
    "hardware",
    "network",
    "server",
    "database",
    "web",
    "cloud",
    "api",
    "framework",
    "library",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "computer vision",
    "natural language processing",
    "nlp",
    "tensorflow",
    "pytorch",
    "docker",
    "linux",
    "windows",
    "git",
    "github",
    "aws",
    "azure",
    "oracle",
    "cisco",
    "active directory",
    "dns",
    "dhcp",
    "vlan",
    "selenium",
    "matlab",
    "vmware",
}

def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def load_known_skills():
    with SKILLS_DICTIONARY_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    known = set()

    for skill_name, skill_info in data.items():
        known.add(normalize_text(skill_name))

        for alias in skill_info.get("aliases", []):
            known.add(normalize_text(alias))

    return known


def extract_annotations(data):
    annotations = []

    for annotation in data.get("annotations", []):
        if len(annotation) != 3:
            continue

        start, end, label = annotation

        if not isinstance(start, int) or not isinstance(end, int):
            continue

        if not isinstance(label, str):
            continue

        if not label.startswith("SKILL:"):
            continue

        skill = label.replace("SKILL:", "", 1).strip()
        normalized = normalize_text(skill)

        if not normalized:
            continue

        annotations.append(
            {
                "start": start,
                "end": end,
                "label": skill,
                "normalized": normalized,
            }
        )

    return annotations


def is_candidate(label: str, known_skills: set[str]) -> bool:
    normalized = normalize_text(label)

    if normalized in known_skills:
        return False

    if normalized in IGNORED_LABELS:
        return False

    # Bỏ các label quá ngắn.
    if len(normalized) < 3:
        return False

    # Chỉ lấy label có chữ/số.
    if not re.search(r"[a-zA-Z0-9]", normalized):
        return False

    return True


def discover_candidates():
    known_skills = load_known_skills()

    frequency = Counter()
    contexts = defaultdict(list)

    files = list(RESUME_DIR.rglob("*.json"))

    print(f"CV files: {len(files)}")

    for index, file_path in enumerate(files, start=1):
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        text = data.get("text", "")
        annotations = extract_annotations(data)

        for annotation in annotations:
            label = annotation["normalized"]

            if not is_candidate(label, known_skills):
                continue

            frequency[label] += 1

            if len(contexts[label]) < 3:
                start = max(
                    0,
                    annotation["start"] - CONTEXT_WINDOW,
                )

                end = min(
                    len(text),
                    annotation["end"] + CONTEXT_WINDOW,
                )

                context = text[start:end]
                context = " ".join(context.split())

                context_lower = context.lower()

                has_technical_context = any(
                    keyword in context_lower
                    for keyword in TECHNICAL_KEYWORDS
                )

                if not has_technical_context:
                    continue

                contexts[label].append(context)

        if index % 500 == 0:
            print(f"Processed: {index}/{len(files)}")

    return frequency, contexts


def main():
    frequency, contexts = discover_candidates()

    candidates = [
        (label, count)
        for label, count in frequency.items()
        if count >= MIN_FREQUENCY
    ]

    candidates.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    print()
    print("=== CONCRETE SKILL CANDIDATES ===")
    print(f"Candidates >= {MIN_FREQUENCY} CVs: {len(candidates)}")

    for label, count in candidates[:100]:
        print()
        print(f"--- {label} ({count} CVs) ---")

        for context in contexts[label]:
            print(f"  {context}")


if __name__ == "__main__":
    main()