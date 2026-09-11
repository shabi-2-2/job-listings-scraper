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
from src.exporter import export_jobs
from src.filter import filter_jobs
from src.scraper import DEFAULT_TIMEOUT, fetch_page, scrape_pages

DEFAULT_URL: str = "https://realpython.github.io/fake-jobs/"
DEFAULT_OUTPUT: Path = Path("data/jobs.csv")
DEFAULT_PLOTS_DIR: Path = Path("data/plots")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


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
    parsed = parser.parse_args(args)
    if not parsed.url.strip():
        parser.error("The --url argument must not be empty.")
    if parsed.pages < 1:
        parser.error("The --pages argument must be a positive integer (>= 1).")
    return parsed


def run_scraper(
    url: str,
    output: Path,
    pages: int = 1,
    keyword: str | None = None,
    location: str | None = None,
    company: str | None = None,
) -> None:
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

    jobs = scrape_pages(start_url=url, pages=pages, timeout=DEFAULT_TIMEOUT)
    if not jobs:
        print("Warning: No job listings were found.")
        export_jobs(jobs, output)
        print(f"Exported {len(jobs)} jobs to {output}\n")
        print("Completed successfully.")
        return

    print(f"Found {len(jobs)} job listings.\n")

    jobs = filter_jobs(jobs, keyword=keyword, location=location, company=company)

    if keyword or location or company:
        if not jobs:
            print("No jobs matched the specified filters.")
            export_jobs(jobs, output)
            print(f"Exported {len(jobs)} jobs to {output}\n")
            print("Completed successfully.")
            return
        print(f"After filtering: {len(jobs)} jobs.\n")

    export_jobs(jobs, output)
    print(f"Exported {len(jobs)} jobs to {output}\n")
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


def main(args: Sequence[str] | None = None) -> None:
    try:
        parsed_args = parse_args(args)
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
