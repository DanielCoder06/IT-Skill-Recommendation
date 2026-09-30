import sqlite3

DB_PATH = "data/it_jobs.db"


def main() -> None:
    connection = sqlite3.connect(DB_PATH)

    total = connection.execute(
        """
        SELECT COUNT(*)
        FROM jobs
        WHERE job_url LIKE 'https://itviec.com/%'
        """
    ).fetchone()[0]

    quality = connection.execute(
        """
        SELECT
            COUNT(*),
            SUM(
                CASE
                    WHEN jd_raw IS NULL
                         OR TRIM(jd_raw) = ''
                    THEN 1
                    ELSE 0
                END
            ),
            MIN(LENGTH(jd_raw)),
            MAX(LENGTH(jd_raw))
        FROM jobs
        WHERE job_url LIKE 'https://itviec.com/%'
        """
    ).fetchone()

    duplicates = connection.execute(
        """
        SELECT job_url, COUNT(*)
        FROM jobs
        WHERE job_url LIKE 'https://itviec.com/%'
        GROUP BY job_url
        HAVING COUNT(*) > 1
        """
    ).fetchall()

    connection.close()

    print("=== ITVIEC DB VERIFICATION ===")
    print(f"ITviec jobs: {total}")
    print(f"Total checked: {quality[0]}")
    print(f"Empty JD: {quality[1]}")
    print(f"Min JD length: {quality[2]}")
    print(f"Max JD length: {quality[3]}")
    print(f"Duplicate URLs: {len(duplicates)}")

    if duplicates:
        print("\n=== DUPLICATES ===")
        for url, count in duplicates:
            print(f"{count}x {url}")


if __name__ == "__main__":
    main()