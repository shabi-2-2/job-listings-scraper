import logging
from src.models import Job

logger = logging.getLogger(__name__)


def deduplicate_jobs(jobs: list[Job]) -> list[Job]:
    seen_urls: set[str] = set()
    unique: list[Job] = []
    for job in jobs:
        if job.url not in seen_urls:
            seen_urls.add(job.url)
            unique.append(job)
    logger.info(
        "Deduplicated %d jobs -> %d unique jobs", len(jobs), len(unique)
    )
    return unique
