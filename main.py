import sys
import requests
from src.parser import parse_jobs
from src.scraper import fetch_page

TARGET_URL = "https://realpython.github.io/fake-jobs/"


def main():
    try:
        response = fetch_page(TARGET_URL)
        print("Successfully fetched webpage.")
        print(f"Status code: {response.status_code}")
        print(f"Downloaded: {len(response.text)} characters.")

        jobs = parse_jobs(response.text, base_url=TARGET_URL)
        print(f"\nFound {len(jobs)} job listings.\n")

        print("First few jobs:\n")
        for idx, job in enumerate(jobs[:5], 1):
            print(f"{idx}. {job.title}")
            print(f"   Company: {job.company}")
            print(f"   Location: {job.location}")
            print(f"   URL: {job.url}\n")
    except requests.exceptions.RequestException as err:
        print(f"Error fetching webpage: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
