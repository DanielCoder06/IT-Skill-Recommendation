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
    Classify job level based primarily on the job title.

    Returns:
        internship
        junior
        senior
        unspecified
    """
    title = job.title.lower()

    if contains_keyword(title, SENIOR_KEYWORDS):
        return "senior"

    if contains_keyword(title, INTERNSHIP_KEYWORDS):
        return "internship"

    if contains_keyword(title, JUNIOR_KEYWORDS):
        return "junior"

    return "unspecified"