from pathlib import Path

from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parents[1]

HTML_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "itviec"
    / "Việc làm AI, Data.html"
)


def main() -> None:
    html = HTML_PATH.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    title = soup.select_one("h3.job-title")

    if title is None:
        print("Không tìm thấy job title.")
        return

    card = title.find_parent("div", class_="ipx-4")

    if card is None:
        print("Không tìm thấy job card.")
        return

    print("=== JOB CARD ===")
    print(card.get_text(" ", strip=True))

    print("\n=== LINKS IN JOB CARD ===")

    for index, link in enumerate(
        card.find_all("a"),
        start=1,
    ):
        print(f"\n--- LINK {index} ---")
        print("text:", link.get_text(" ", strip=True))
        print("href:", link.get("href"))
        print("class:", link.get("class"))

    print("\n=== DIRECT CHILDREN ===")

    for index, child in enumerate(
        card.find_all(recursive=False),
        start=1,
    ):
        print(f"\n--- CHILD {index} ---")
        print("tag:", child.name)
        print("class:", child.get("class"))
        print("text:", child.get_text(" ", strip=True)[:300])


if __name__ == "__main__":
    main()