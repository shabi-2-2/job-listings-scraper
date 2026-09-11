import logging
from src.models import Job

logger = logging.getLogger(__name__)


def filter_jobs(
    jobs: list[Job],
    keyword: str | None = None,
    location: str | None = None,
    company: str | None = None,
) -> list[Job]:
    if not any([keyword, location, company]):
        return jobs

    filtered: list[Job] = []
    for job in jobs:
        matches = True

        if keyword:
            if keyword.lower() not in job.title.lower():
                matches = False

        if location:
            if location.lower() not in job.location.lower():
                matches = False

        if company:
            if company.lower() not in job.company.lower():
                matches = False

        if matches:
            filtered.append(job)

    logger.info(
        "Filtered %d -> %d jobs (keyword=%s, location=%s, company=%s)",
        len(jobs),
        len(filtered),
        keyword,
        location,
        company,
    )
    return filtered
