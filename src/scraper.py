import logging
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import requests
from src.models import Job
from src.parser import parse_jobs

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT: float = 10.0


def fetch_page(url: str, timeout: float = DEFAULT_TIMEOUT) -> requests.Response:
    logger.info("Fetching webpage from %s", url)
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        logger.info("Successfully fetched %s (status code %d)", url, response.status_code)
        return response
    except requests.exceptions.Timeout as err:
        logger.error("Request timed out while connecting to %s", url)
        raise requests.exceptions.Timeout(
            f"Request timed out while connecting to {url}"
        ) from err
    except requests.exceptions.ConnectionError as err:
        logger.error("Connection error occurred while connecting to %s", url)
        raise requests.exceptions.ConnectionError(
            f"Failed to connect to {url}"
        ) from err
    except requests.exceptions.HTTPError as err:
        status = response.status_code if "response" in locals() else "unknown"
        logger.error("HTTP error %s occurred for %s", status, url)
        raise requests.exceptions.HTTPError(
            f"HTTP error {status} occurred while requesting {url}"
        ) from err
    except requests.exceptions.RequestException as err:
        logger.error("Request error occurred for %s: %s", url, err)
        raise requests.exceptions.RequestException(
            f"Failed to fetch {url}: {err}"
        ) from err


def build_page_url(base_url: str, page: int) -> str:
    if page < 1:
        raise ValueError("The page number must be a positive integer (>= 1).")
    if page == 1:
        return base_url

    parsed = urlparse(base_url)
    query_dict = dict(parse_qsl(parsed.query))
    query_dict["page"] = str(page)
    new_query = urlencode(query_dict)
    return urlunparse(parsed._replace(query=new_query))


def scrape_pages(
    start_url: str, pages: int = 1, timeout: float = DEFAULT_TIMEOUT
) -> list[Job]:
    if pages < 1:
        raise ValueError("The number of pages must be a positive integer (>= 1).")

    all_jobs: list[Job] = []
    for page_num in range(1, pages + 1):
        page_url = build_page_url(start_url, page_num)
        logger.info("Scraping page %d of %d from %s", page_num, pages, page_url)
        try:
            response = fetch_page(page_url, timeout=timeout)
            page_jobs = parse_jobs(response.text, base_url=page_url)
            all_jobs.extend(page_jobs)
            logger.info(
                "Page %d parsed successfully: found %d jobs",
                page_num,
                len(page_jobs),
            )
        except requests.exceptions.RequestException as err:
            logger.warning(
                "Failed to fetch page %d from %s: %s",
                page_num,
                page_url,
                err,
            )

    return all_jobs
