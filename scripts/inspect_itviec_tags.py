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

    jobs = soup.select("h3.job-title")

    for index in [4, 5, 6, 10]:
        title = jobs[index - 1]

        card = title.find_parent(
            "div",
            class_="ipx-4",
        )

        print("\n" + "=" * 70)
        print(f"JOB {index}: {title.get_text(' ', strip=True)}")
        print("=" * 70)

        tag_container = card.select_one(
            "div[data-controller*='responsive-tag-list']"
        )

        if tag_container is None:
            print("TAG CONTAINER: NOT FOUND")
        else:
            print("TAG CONTAINER FOUND")
            print(
                tag_container.prettify()[:5000]
            )


if __name__ == "__main__":
    main()