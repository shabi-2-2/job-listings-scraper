import logging
import time
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import requests
from src.models import Job
from src.parser import parse_jobs

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT: float = 10.0
DEFAULT_RETRIES: int = 2
RETRY_DELAY: float = 0.5
RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({500, 501, 502, 503, 504})


def _should_retry(err: requests.exceptions.RequestException) -> bool:
    if isinstance(
        err, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)
    ):
        return True
    if isinstance(err, requests.exceptions.HTTPError):
        response = getattr(err, "response", None)
        if response is not None and getattr(
            response, "status_code", None
        ) in RETRYABLE_STATUS_CODES:
            return True
    return False


def fetch_page(
    url: str,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    delay: float = RETRY_DELAY,
) -> requests.Response:
    logger.info("Fetching webpage from %s", url)
    attempts = 0
    while True:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            logger.info(
                "Successfully fetched %s (status code %d)",
                url,
                response.status_code,
            )
            return response
        except requests.exceptions.RequestException as err:
            attempts += 1
            if attempts > retries or not _should_retry(err):
                logger.error(
                    "Failed to fetch %s after %d attempt(s): %s", url, attempts, err
                )
                raise err
            logger.warning(
                "Attempt %d failed for %s (%s); retrying in %.1fs",
                attempts,
                url,
                err,
                delay,
            )
            time.sleep(delay)


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
    start_url: str,
    pages: int = 1,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> list[Job]:
    if pages < 1:
        raise ValueError("The number of pages must be a positive integer (>= 1).")

    all_jobs: list[Job] = []
    for page_num in range(1, pages + 1):
        page_url = build_page_url(start_url, page_num)
        logger.info("Scraping page %d of %d from %s", page_num, pages, page_url)
        try:
            response = fetch_page(page_url, timeout=timeout, retries=retries)
            page_jobs = parse_jobs(response.text, base_url=page_url)
            all_jobs.extend(page_jobs)
            logger.info(
                "Page %d parsed successfully: found %d jobs",
                page_num,
                len(page_jobs),
            )
        except requests.exceptions.RequestException as err:
            logger.error(
                "Skipping page %d from %s after failed requests: %s",
                page_num,
                page_url,
                err,
            )

    return all_jobs
