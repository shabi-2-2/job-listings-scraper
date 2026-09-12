import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence
import requests
from src.analyzer import (
    clean_data,
    generate_visualizations,
    get_top_companies,
    get_top_job_titles,
    get_top_locations,
    get_total_jobs,
    get_unique_companies,
    get_unique_locations,
    load_jobs,
)
from src.dedup import deduplicate_jobs
from src.exporter import export_jobs, export_jobs_json
from src.filter import filter_jobs
from src.models import Job
from src.scraper import (
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT,
    fetch_page,
    scrape_pages,
)

DEFAULT_URL: str = "https://realpython.github.io/fake-jobs/"
DEFAULT_OUTPUT: Path = Path("data/jobs.csv")
DEFAULT_PLOTS_DIR: Path = Path("data/plots")
DEFAULT_LOG_LEVEL: int = logging.INFO

LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(__name__)


def setup_logging(level: int = DEFAULT_LOG_LEVEL) -> None:
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    root = logging.getLogger()
    root.setLevel(level)
    for handler in root.handlers:
        handler.setLevel(level)


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Job Listings Scraper & Analyzer: Extract, export, and analyze job postings."
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
        help="Path where the CSV file will be written or read from (default: %(default)s)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Number of pages to scrape (default: %(default)s)",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default=None,
        help="Filter jobs by keyword in title (case-insensitive)",
    )
    parser.add_argument(
        "--location",
        type=str,
        default=None,
        help="Filter jobs by location (case-insensitive)",
    )
    parser.add_argument(
        "--company",
        type=str,
        default=None,
        help="Filter jobs by company name (case-insensitive)",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze existing job CSV data and generate charts",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Additionally export jobs as JSON next to the CSV output file",
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug-level logging output",
    )
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress log output below the WARNING level",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Request timeout in seconds per attempt (default: %(default)s)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help="Maximum number of retries for transient request failures (default: %(default)s)",
    )
    parsed = parser.parse_args(args)
    if not parsed.url.strip():
        parser.error("The --url argument must not be empty.")
    if parsed.pages < 1:
        parser.error("The --pages argument must be a positive integer (>= 1).")
    if parsed.timeout <= 0:
        parser.error("The --timeout argument must be a positive number.")
    if parsed.retries < 0:
        parser.error("The --retries argument must be a non-negative integer (>= 0).")
    return parsed


def export_results(jobs: list[Job], output: Path, json_output: bool = False) -> None:
    export_jobs(jobs, output)
    print(f"Exported {len(jobs)} jobs to {output}\n")
    if json_output:
        json_path = output.with_suffix(".json")
        export_jobs_json(jobs, json_path)
        print(f"Exported {len(jobs)} jobs to {json_path}\n")


def run_scraper(
    url: str,
    output: Path,
    pages: int = 1,
    keyword: str | None = None,
    location: str | None = None,
    company: str | None = None,
    json_output: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> None:
    logger.info(
        "Starting job scraping pipeline (target=%s, pages=%d, output=%s)",
        url,
        pages,
        output,
    )
    logger.debug(
        "Pipeline configuration: keyword=%s, location=%s, company=%s, json_output=%s, timeout=%s, retries=%s",
        keyword,
        location,
        company,
        json_output,
        timeout,
        retries,
    )
    print("Starting job scraper...\n")
    print(f"Target: {url}")
    if pages > 1:
        print(f"Pages: {pages}")
    if keyword:
        print(f"Keyword: {keyword}")
    if location:
        print(f"Location: {location}")
    if company:
        print(f"Company: {company}")
    print(f"Output: {output}\n")

    jobs = scrape_pages(
        start_url=url, pages=pages, timeout=timeout, retries=retries
    )
    logger.info("Scraping complete: found %d job listings", len(jobs))
    if not jobs:
        logger.warning("No job listings were found for %s", url)
        print("Warning: No job listings were found.")
        export_results(jobs, output, json_output)
        logger.info("Pipeline completed: exported 0 jobs to %s", output)
        print("Completed successfully.")
        return

    print(f"Found {len(jobs)} job listings.\n")

    jobs = deduplicate_jobs(jobs)

    jobs = filter_jobs(jobs, keyword=keyword, location=location, company=company)

    if keyword or location or company:
        if not jobs:
            logger.info("No jobs matched the specified filters")
            print("No jobs matched the specified filters.")
            export_results(jobs, output, json_output)
            logger.info("Pipeline completed: exported 0 jobs to %s", output)
            print("Completed successfully.")
            return
        print(f"After filtering: {len(jobs)} jobs.\n")

    export_results(jobs, output, json_output)
    logger.info(
        "Pipeline completed successfully: exported %d jobs to %s", len(jobs), output
    )
    print("Completed successfully.")


def run_analysis(csv_path: Path, plots_dir: Path = DEFAULT_PLOTS_DIR) -> None:
    df = load_jobs(csv_path)
    df = clean_data(df)

    total_jobs = get_total_jobs(df)
    unique_companies = get_unique_companies(df)
    unique_locations = get_unique_locations(df)

    top_companies = get_top_companies(df, n=5)
    top_locations = get_top_locations(df, n=5)
    top_titles = get_top_job_titles(df, n=5)

    generate_visualizations(df, output_dir=plots_dir)

    print("Job Statistics")
    print("==============")
    print(f"\nTotal jobs: {total_jobs}")
    print(f"Unique companies: {unique_companies}")
    print(f"Unique locations: {unique_locations}\n")

    print("Top companies:")
    for idx, (company, count) in enumerate(top_companies.items(), 1):
        print(f"{idx}. {company} — {count} jobs")

    print("\nTop locations:")
    for idx, (location, count) in enumerate(top_locations.items(), 1):
        print(f"{idx}. {location} — {count} jobs")

    print("\nTop job titles:")
    for idx, (title, count) in enumerate(top_titles.items(), 1):
        print(f"{idx}. {title} — {count} jobs")

    print(f"\nVisualizations saved to {plots_dir}")
    logger.info("Analysis complete: %d jobs from %s", total_jobs, csv_path)


def main(args: Sequence[str] | None = None) -> None:
    try:
        parsed_args = parse_args(args)
        if parsed_args.verbose:
            level = logging.DEBUG
        elif parsed_args.quiet:
            level = logging.WARNING
        else:
            level = DEFAULT_LOG_LEVEL
        setup_logging(level)
        if parsed_args.analyze:
            run_analysis(csv_path=parsed_args.output)
        else:
            run_scraper(
                url=parsed_args.url,
                output=parsed_args.output,
                pages=parsed_args.pages,
                keyword=parsed_args.keyword,
                location=parsed_args.location,
                company=parsed_args.company,
                json_output=parsed_args.json,
                timeout=parsed_args.timeout,
                retries=parsed_args.retries,
            )
    except (FileNotFoundError, ValueError) as err:
        logger.error("Analysis error: %s", err)
        print(f"Error during analysis: {err}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        logger.error("Scraper encountered a network error: %s", err)
        print(f"Error fetching webpage: {err}", file=sys.stderr)
        sys.exit(1)
    except OSError as err:
        logger.error("File system error: %s", err)
        print(f"Error accessing file system: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        logger.error("Unexpected error occurred: %s", err)
        print(f"Unexpected error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
