import unittest
from unittest.mock import MagicMock, patch
import requests
from src.scraper import fetch_page


class TestScraper(unittest.TestCase):
    @patch("src.scraper.requests.get")
    def test_fetch_page_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Fake Jobs</h1></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = "https://realpython.github.io/fake-jobs/"
        result = fetch_page(url)

        mock_get.assert_called_once_with(url, timeout=10.0)
        self.assertEqual(result, mock_response)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, "<html><body><h1>Fake Jobs</h1></body></html>")

    @patch("src.scraper.requests.get")
    def test_fetch_page_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        with self.assertRaises(requests.exceptions.Timeout):
            fetch_page("https://example.com")

    @patch("src.scraper.requests.get")
    def test_fetch_page_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with self.assertRaises(requests.exceptions.ConnectionError):
            fetch_page("https://example.com")

    @patch("src.scraper.requests.get")
    def test_fetch_page_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            fetch_page("https://example.com")

    @patch("src.scraper.requests.get")
    def test_fetch_page_generic_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Generic request error")

        with self.assertRaises(requests.exceptions.RequestException):
            fetch_page("https://example.com")


if __name__ == "__main__":
    unittest.main()
