import unittest
from unittest.mock import MagicMock, patch
import requests
from src.scraper import build_page_url, fetch_page, scrape_pages

HTML_JOB_1 = """
<div class="card">
    <div class="card-content">
        <h2 class="title">Dev 1</h2>
        <h3 class="company">Company 1</h3>
        <p class="location">Location 1</p>
        <footer class="card-footer"><a href="https://example.com/1">Apply</a></footer>
    </div>
</div>
"""

HTML_JOB_2 = """
<div class="card">
    <div class="card-content">
        <h2 class="title">Dev 2</h2>
        <h3 class="company">Company 2</h3>
        <p class="location">Location 2</p>
        <footer class="card-footer"><a href="https://example.com/2">Apply</a></footer>
    </div>
</div>
"""


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

    def test_build_page_url_first_page(self):
        url = build_page_url("https://example.com/jobs", 1)
        self.assertEqual(url, "https://example.com/jobs")

    def test_build_page_url_subsequent_pages(self):
        url = build_page_url("https://example.com/jobs", 2)
        self.assertEqual(url, "https://example.com/jobs?page=2")

    def test_build_page_url_existing_query_params(self):
        url = build_page_url("https://example.com/jobs?cat=dev", 3)
        self.assertEqual(url, "https://example.com/jobs?cat=dev&page=3")

    def test_build_page_url_invalid(self):
        with self.assertRaises(ValueError):
            build_page_url("https://example.com/jobs", 0)

    @patch("src.scraper.fetch_page")
    def test_scrape_pages_single_page(self, mock_fetch):
        mock_resp = MagicMock()
        mock_resp.text = HTML_JOB_1
        mock_fetch.return_value = mock_resp

        jobs = scrape_pages("https://example.com/jobs", pages=1)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, "Dev 1")
        mock_fetch.assert_called_once_with("https://example.com/jobs", timeout=10.0)

    @patch("src.scraper.fetch_page")
    def test_scrape_pages_multiple_pages(self, mock_fetch):
        resp1 = MagicMock()
        resp1.text = HTML_JOB_1
        resp2 = MagicMock()
        resp2.text = HTML_JOB_2
        mock_fetch.side_effect = [resp1, resp2]

        jobs = scrape_pages("https://example.com/jobs", pages=2)
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0].title, "Dev 1")
        self.assertEqual(jobs[1].title, "Dev 2")
        self.assertEqual(mock_fetch.call_count, 2)

    @patch("src.scraper.fetch_page")
    def test_scrape_pages_handles_failed_page(self, mock_fetch):
        resp1 = MagicMock()
        resp1.text = HTML_JOB_1
        mock_fetch.side_effect = [
            resp1,
            requests.exceptions.ConnectionError("Failed page 2"),
        ]

        jobs = scrape_pages("https://example.com/jobs", pages=2)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].title, "Dev 1")

    def test_scrape_pages_invalid_pages(self):
        with self.assertRaises(ValueError):
            scrape_pages("https://example.com/jobs", pages=0)


if __name__ == "__main__":
    unittest.main()
