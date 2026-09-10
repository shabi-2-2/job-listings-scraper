import requests


def fetch_page(url: str, timeout: float = 10.0) -> str:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout as err:
        raise requests.exceptions.Timeout(f"Request timed out while connecting to {url}") from err
    except requests.exceptions.ConnectionError as err:
        raise requests.exceptions.ConnectionError(f"Failed to connect to {url}") from err
    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(
            f"HTTP error {response.status_code} occurred while requesting {url}"
        ) from err
    except requests.exceptions.RequestException as err:
        raise requests.exceptions.RequestException(
            f"Failed to fetch {url}: {err}"
        ) from err
