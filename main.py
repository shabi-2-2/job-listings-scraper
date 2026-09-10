import sys
from pathlib import Path
import requests
from src.exporter import export_jobs
from src.parser import parse_jobs
from src.scraper import fetch_page

TARGET_URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_PATH = Path("data/jobs.csv")


def main():
    try:
        response = fetch_page(TARGET_URL)
        print("Successfully fetched webpage.")
        print(f"Status code: {response.status_code}")
        print(f"Downloaded: {len(response.text)} characters.\n")

        jobs = parse_jobs(response.text, base_url=TARGET_URL)
        print(f"Found {len(jobs)} job listings.\n")

        export_jobs(jobs, OUTPUT_PATH)
        print(f"Exported {len(jobs)} jobs to {OUTPUT_PATH}")
    except requests.exceptions.RequestException as err:
        print(f"Error fetching webpage: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
