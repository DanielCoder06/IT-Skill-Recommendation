from src.scraper.job_schema import JobRecord


IT_TITLE_KEYWORDS = {
    "software",
    "developer",
    "entwickler",
    "programmer",
    "programmierer",
    "data engineer",
    "data analyst",
    "data scientist",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai engineer",
    "backend",
    "back-end",
    "frontend",
    "front-end",
    "full stack",
    "fullstack",
    "devops",
    "cloud engineer",
    "cloud developer",
    "cybersecurity",
    "cyber security",
    "database",
    "software engineer",
    "web developer",
    "webentwickler",
    "mobile developer",
    "android developer",
    "ios developer",
    "qa engineer",
    "test automation",
    "site reliability",
    "sre",
    "network engineer",
    "system administrator",
    "systems engineer",
    "it specialist",
}


IT_DESCRIPTION_KEYWORDS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "golang",
    "sql",
    "react",
    "vue",
    "node.js",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "rest api",
    "git",
    "github",
}


NON_IT_TITLE_KEYWORDS = {
    "sales",
    "account executive",
    "marketing",
    "recruiter",
    "recruiting",
    "talent acquisition",
    "human resources",
    "hr manager",
    "finance",
    "financial",
    "accounting",
    "controller",
    "legal",
    "lawyer",
    "designer",
    "graphic designer",
    "bauleiter",
    "construction",
    "consultant",
    "customer success",
    "customer service",
    "business development",
    "country lead",
    "venture development",
    "revops",
    "gtm",
}


def calculate_it_score(job: JobRecord) -> int:
    """
    Calculate a deterministic IT relevance score.
    """
    title = job.title.lower()
    description = job.description.lower()

    score = 0

    for keyword in IT_TITLE_KEYWORDS:
        if keyword in title:
            score += 3

    for keyword in IT_DESCRIPTION_KEYWORDS:
        if keyword in description:
            score += 1

    for keyword in NON_IT_TITLE_KEYWORDS:
        if keyword in title:
            score -= 5

    return score


def is_it_job(
    job: JobRecord,
    threshold: int = 3,
) -> bool:
    """
    Return True when the job reaches the IT relevance threshold.
    """
    return calculate_it_score(job) >= threshold


def filter_it_jobs(
    jobs: list[JobRecord],
) -> list[JobRecord]:
    """
    Keep jobs that are sufficiently relevant to IT.
    """
    return [
        job
        for job in jobs
        if is_it_job(job)
    ]