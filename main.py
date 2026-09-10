import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence
import requests
from src.exporter import export_jobs
from src.parser import parse_jobs
from src.scraper import DEFAULT_TIMEOUT, fetch_page

DEFAULT_URL: str = "https://realpython.github.io/fake-jobs/"
DEFAULT_OUTPUT: Path = Path("data/jobs.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Job Listings Scraper: Extract, parse, and export job postings to CSV."
    )
    parser.add_argument(
        "--url",
        type=str,
        default=DEFAULT_URL,
        help="Target webpage to scrape (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path where the CSV file will be written (default: %(default)s)",
    )
    parsed = parser.parse_args(args)
    if not parsed.url.strip():
        parser.error("The --url argument must not be empty.")
    return parsed


def run(url: str, output: Path) -> None:
    print("Starting job scraper...\n")
    print(f"Target: {url}")
    print(f"Output: {output}\n")

    response = fetch_page(url, timeout=DEFAULT_TIMEOUT)
    print("Successfully fetched webpage.")
    print(f"Status code: {response.status_code}\n")

    jobs = parse_jobs(response.text, base_url=url)
    if not jobs:
        print("Warning: No job listings were found.")
    print(f"Found {len(jobs)} job listings.\n")

    export_jobs(jobs, output)
    print(f"Exported {len(jobs)} jobs to {output}\n")
    print("Completed successfully.")


def main(args: Sequence[str] | None = None) -> None:
    try:
        parsed_args = parse_args(args)
        run(url=parsed_args.url, output=parsed_args.output)
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
