import re
import json
from pathlib import Path

from src.analytics.analyze_resume_candidate_context import (
    build_alias_lookup,
    collect_unmatched_candidates,
    load_skill_dictionary,
)

BASE_DIR = Path(__file__).resolve().parents[2]
RESUME_LABEL_MAPPING_PATH = (
    BASE_DIR
    / "config"
    / "resume_label_mapping.json"
)

MIN_CV_FREQUENCY = 10
MAX_CANDIDATES = 200
MAX_CONTEXTS_PER_LABEL = 5

HARD_NON_SKILL_LABELS = {
    "personal",
    "nationality",
    "gender",
    "marital status",
    "passport",
    "email",
    "mobile",
    "gmail",
    "hindi",
    "religion",
    "organization",
    "ltd",
    "manager",

    # thêm
    "college",
    "activities",
    "academic",
    "can",
    "per",
    "languages",
    "work experience",
    "curriculum",
    "curriculum vitae",
    "education",
    "training",
    "qualification",
    "qualifications",
    "board",
    "responsibilities",
    "department",
}

GENERIC_LABELS = {
    "skills",
    "work",
    "knowledge",
    "team",
    "office",
    "management",
    "technical",
    "engineering",
    "system",
    "systems",
    "computer",
    "technology",
    "development",
    "data",
    "analysis",
    "service",
    "support",
    "ability",
    "requirements",
    "software",
    "language",
    "science",
    "business",
    "client",
    "clients",
    "customer",
    "customers",
    "process",
    "performance",
    "application",
    "operations",
    "operation",
    "procedures",
    "report",
    "reports",
    "project",
    "projects",
    "microsoft",
}

ROLE_LABELS = {
    "engineer",
    "developer",
    "manager",
    "analyst",
    "scientist",
    "consultant",
    "administrator",
    "designer",
    "intern",
    "director",
    "specialist",
    "technician",
    "architect",
}

ACTION_LABELS = {
    "work",
    "working",
    "maintain",
    "maintaining",
    "manage",
    "managing",
    "ensure",
    "handling",
    "installation",
    "install",
    "prepare",
    "preparation",
    "planning",
}

SHORT_EXCEPTIONS = {
    "c",
    "r",
    "go",
    "sql",
    "ai",
    "ml",
    "nlp",
    "c++",
    "c#",
    ".net",
}

TECHNICAL_KEYWORDS = {
    "software",
    "programming",
    "developer",
    "database",
    "web",
    "framework",
    "library",
    "api",
    "testing",
    "operating system",
    "linux",
    "windows",
    "server",
    "network",
    "cloud",
    "computer",
    "data",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "algorithm",
    "coding",
    "python",
    "java",
    "javascript",
    "sql",
    "excel",
    "docker",
    "git",
}

TARGET_AMBIGUOUS_LABELS = {
    "technology",
    "software",
    "development",
    "data",
    "control",
}

EMAIL_PATTERN = re.compile(
    r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b"
)

DOMAIN_PATTERN = re.compile(
    r"\bwww\.[\w.-]+\.com\b"
)

def load_resume_label_mapping() -> dict[str, str]:
    with RESUME_LABEL_MAPPING_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return {
            key.lower().strip(): value
            for key, value in json.load(file).items()
        }

def classify_candidate(label: str, contexts: list[str]):
    label = label.lower().strip()

    # 1. Clearly not a skill
    if label in HARD_NON_SKILL_LABELS:
        return "NON_SKILL"

    # 2. Job role
    if label in ROLE_LABELS:
        return "ROLE"

    # 3. Action / verb
    if label in ACTION_LABELS:
        return "ACTION"

    # 4. Very short labels
    if len(label) <= 2 and label not in SHORT_EXCEPTIONS:
        return "SHORT_LABEL"

    # 5. Generic words
    if label in GENERIC_LABELS:
        return "AMBIGUOUS"

    # 6. Contact/domain noise
    for context in contexts:
        if EMAIL_PATTERN.search(context):
            return "NON_SKILL"

        if DOMAIN_PATTERN.search(context):
            return "NON_SKILL"

    # 7. Context evidence
    technical_score = 0

    for context in contexts:
        context_lower = context.lower()

        for keyword in TECHNICAL_KEYWORDS:
            if keyword in context_lower:
                technical_score += 1

    if technical_score >= 3:
        return "TECHNICAL_CANDIDATE"

    return "AMBIGUOUS"


def main():
    skill_dictionary = load_skill_dictionary()
    known_labels = build_alias_lookup(skill_dictionary)

    label_mapping = load_resume_label_mapping()

    label_counter, contexts = collect_unmatched_candidates(
        known_labels
    )

    # Những label đã có quyết định ở canonical mapping
    # không cần đưa lại vào candidate review.
    resolved_labels = set(label_mapping.keys())

    candidates = [
        (label, count)
        for label, count in label_counter.items()
        if count >= MIN_CV_FREQUENCY
        and label not in resolved_labels
    ]

    candidates.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    candidates = candidates[:MAX_CANDIDATES]

    results = {
        "TECHNICAL_CANDIDATE": [],
        "AMBIGUOUS": [],
        "NON_SKILL": [],
        "ROLE": [],
        "ACTION": [],
        "SHORT_LABEL": [],
    }

    for label, count in candidates:
        classification = classify_candidate(
            label,
            contexts.get(label, []),
        )

        results[classification].append(
            (label, count)
        )

    print(f"Total unmatched labels: {len(label_counter)}")
    print(f"Candidate pool: {len(candidates)}")
    print(f"Reviewing top {MAX_CANDIDATES} candidates...\n")

    print("Classification summary:")

    for category, items in results.items():
        print(f"  {category}: {len(items)}")
    print("\n=== MAPPED / REMOVED / REVIEW ===")

    for label, decision in sorted(
        label_mapping.items()
    ):
        count = label_counter.get(label, 0)

        if decision in {
            "REMOVE",
            "REVIEW",
        }:
            print(
                f"{label:30} "
                f"{decision:10} "
                f"{count} CVs"
            )
    print("\n=== TECHNICAL CANDIDATE CONTEXTS ===")

    for label, count in results["TECHNICAL_CANDIDATE"]:
        print(f"\n--- {label} ({count} CVs) ---")

        for context in contexts.get(label, [])[:3]:
            print(f"  {context}")
            
    print("\n=== TARGET AMBIGUOUS CONTEXTS ===")

    for label in TARGET_AMBIGUOUS_LABELS:
        count = label_counter.get(label, 0)

        print(f"\n--- {label} ({count} CVs) ---")

        for context in contexts.get(label, [])[:3]:
            print(f"  {context}")

    print("\n=== AMBIGUOUS ===")

    for index, (label, count) in enumerate(
        results["AMBIGUOUS"],
        start=1,
    ):
        print(f"{index:2}. {label} ({count} CVs)")

        if index <= 5:
            print("  Contexts:")

            for context in contexts.get(label, [])[:3]:
                print(f"    - {context}")

    print("\n=== REMOVED / OTHER ===")

    for category in [
        "NON_SKILL",
        "ROLE",
        "ACTION",
        "SHORT_LABEL",
    ]:
        print(f"\n[{category}]")

        for label, count in results[category]:
            print(f"  {label} ({count} CVs)")


if __name__ == "__main__":
    main()