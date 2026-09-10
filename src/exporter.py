import csv
from pathlib import Path
from typing import Iterable
from src.models import Job


def export_jobs(jobs: Iterable[Job], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "company", "location", "url"])
        for job in jobs:
            writer.writerow([job.title, job.company, job.location, job.url])
