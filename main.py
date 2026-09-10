import sys
import requests
from src.scraper import fetch_page

TARGET_URL = "https://realpython.github.io/fake-jobs/"


def main():
    try:
        response = fetch_page(TARGET_URL)
        print("Successfully fetched webpage.")
        print(f"Status code: {response.status_code}")
        print(f"Downloaded: {len(response.text)} characters.")
    except requests.exceptions.RequestException as err:
        print(f"Error fetching webpage: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
