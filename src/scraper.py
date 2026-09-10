import logging
import requests

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
