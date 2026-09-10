import csv
import logging
from pathlib import Path
from typing import Iterable
from src.models import Job

logger = logging.getLogger(__name__)

CSV_FIELDNAMES = ["title", "company", "location", "url"]


def export_jobs(jobs: Iterable[Job], output_path: str | Path) -> None:
    path = Path(output_path)
    logger.info("Starting CSV export to %s", path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with open(path, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_FIELDNAMES)
            for job in jobs:
                writer.writerow([job.title, job.company, job.location, job.url])
                count += 1
        logger.info("Successfully exported %d jobs to %s", count, path)
    except OSError as err:
        logger.error("File system error occurred while exporting to %s: %s", path, err)
        raise
