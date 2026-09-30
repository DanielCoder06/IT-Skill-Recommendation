from src.scraper.job_schema import JobRecord


INTERNSHIP_KEYWORDS = {
    "intern",
    "internship",
    "praktikum",
    "praktikant",
    "praktikantin",
    "werkstudent",
    "working student",
    "trainee",
    "ausbildung",
}


JUNIOR_KEYWORDS = {
    "junior",
    "entry level",
    "entry-level",
    "graduate",
    "berufseinsteiger",
    "absolvent",
}


SENIOR_KEYWORDS = {
    "senior",
    "sr.",
    "sr ",
    "staff",
    "principal",
    "lead",
    "director",
    "head of",
    "vp ",
    "vice president",
}


def contains_keyword(
    text: str,
    keywords: set[str],
) -> bool:
    return any(
        keyword in text
        for keyword in keywords
    )


def classify_job_level(job: JobRecord) -> str:
    """
    Classify job level using both source-provided experience
    and the job title.

    Priority:
        1. experience field
        2. job title
        3. unspecified

    Returns:
        internship
        junior
        senior
        unspecified
    """

    title = job.title.lower().strip()
    experience = job.experience.lower().strip()

    # ---------------------------------------------------------
    # 1. Use source-provided experience first
    # ---------------------------------------------------------

    if contains_keyword(
        experience,
        INTERNSHIP_KEYWORDS,
    ):
        return "internship"

    if contains_keyword(
        experience,
        JUNIOR_KEYWORDS,
    ):
        return "junior"

    if contains_keyword(
        experience,
        SENIOR_KEYWORDS,
    ):
        return "senior"

    # ---------------------------------------------------------
    # 2. Fall back to title classification
    # ---------------------------------------------------------

    if contains_keyword(
        title,
        SENIOR_KEYWORDS,
    ):
        return "senior"

    if contains_keyword(
        title,
        INTERNSHIP_KEYWORDS,
    ):
        return "internship"

    if contains_keyword(
        title,
        JUNIOR_KEYWORDS,
    ):
        return "junior"

    # ---------------------------------------------------------
    # 3. Unknown level
    # ---------------------------------------------------------

    return "unspecified"