import logging
import sys
from pathlib import Path
import requests
from src.exporter import export_jobs
from src.parser import parse_jobs
from src.scraper import DEFAULT_TIMEOUT, fetch_page

TARGET_URL: str = "https://realpython.github.io/fake-jobs/"
OUTPUT_PATH: Path = Path("data/jobs.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    try:
        response = fetch_page(TARGET_URL, timeout=DEFAULT_TIMEOUT)
        print("Successfully fetched webpage.")
        print(f"Status code: {response.status_code}")
        print(f"Downloaded: {len(response.text)} characters.\n")

        jobs = parse_jobs(response.text, base_url=TARGET_URL)
        if not jobs:
            print("Warning: No job listings were found.")
        print(f"Found {len(jobs)} job listings.\n")

        export_jobs(jobs, OUTPUT_PATH)
        print(f"Exported {len(jobs)} jobs to {OUTPUT_PATH}")
    except requests.exceptions.RequestException as err:
        logger.error("Scraper encountered a network error: %s", err)
        print(f"Error fetching webpage: {err}", file=sys.stderr)
        sys.exit(1)
    except OSError as err:
        logger.error("Exporter encountered a file system error: %s", err)
        print(f"Error exporting data: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        logger.error("Unexpected error occurred: %s", err)
        print(f"Unexpected error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
