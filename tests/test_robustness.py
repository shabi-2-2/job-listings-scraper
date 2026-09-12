import logging
from unittest.mock import MagicMock, patch
import requests
import pytest
from src.parser import parse_jobs
from src.scraper import (
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT,
    RETRYABLE_STATUS_CODES,
    _should_retry,
    fetch_page,
    scrape_pages,
)

HTML_JOB = """
<div class="card">
    <div class="card-content">
        <h2 class="title">Dev</h2>
        <h3 class="company">Company</h3>
        <p class="location">Location</p>
        <footer class="card-footer"><a href="https://example.com/1">Apply</a></footer>
    </div>
</div>
"""


def _response(status_code: int = 200, text: str = HTML_JOB) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.raise_for_status.return_value = None
    return resp


def _http_error(status_code: int) -> requests.exceptions.HTTPError:
    err = requests.exceptions.HTTPError(f"{status_code} Server Error")
    err.response = _response(status_code=status_code)
    return err


class TestShouldRetry:
    def test_timeout_is_retryable(self):
        assert _should_retry(requests.exceptions.Timeout()) is True

    def test_connection_error_is_retryable(self):
        assert _should_retry(requests.exceptions.ConnectionError()) is True

    def test_http_5xx_is_retryable(self):
        for status in RETRYABLE_STATUS_CODES:
            assert _should_retry(_http_error(status)) is True

    def test_http_4xx_is_not_retryable(self):
        assert _should_retry(_http_error(404)) is False

    def test_generic_request_exception_is_not_retryable(self):
        assert _should_retry(requests.exceptions.RequestException()) is False


class TestFetchPageRetries:
    @patch("src.scraper.requests.get")
    def test_success_single_attempt(self, mock_get):
        mock_get.return_value = _response()

        result = fetch_page("https://example.com", timeout=5.0, retries=2)

        mock_get.assert_called_once_with("https://example.com", timeout=5.0)
        assert result.status_code == 200

    @patch("src.scraper.requests.get")
    def test_retry_success_after_initial_failure(self, mock_get, caplog):
        mock_get.side_effect = [
            requests.exceptions.Timeout("t1"),
            requests.exceptions.ConnectionError("c1"),
            _response(),
        ]

        with caplog.at_level(logging.DEBUG):
            result = fetch_page("https://example.com", retries=2, delay=0)

        assert result.status_code == 200
        assert mock_get.call_count == 3
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 2
        assert all("retrying" in w.getMessage() for w in warnings)
        assert not any(
            r.levelno == logging.ERROR for r in caplog.records
        )

    @patch("src.scraper.requests.get")
    def test_retries_exhausted_raises_and_logs(self, mock_get, caplog):
        mock_get.side_effect = [
            requests.exceptions.Timeout("t1"),
            requests.exceptions.Timeout("t2"),
            requests.exceptions.Timeout("t3"),
        ]

        with caplog.at_level(logging.DEBUG):
            with pytest.raises(requests.exceptions.Timeout):
                fetch_page("https://example.com", retries=2, delay=0)

        assert mock_get.call_count == 3
        warn_msgs = [
            r.getMessage() for r in caplog.records if r.levelno == logging.WARNING
        ]
        assert len(warn_msgs) == 2
        errors = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert len(errors) == 1
        assert "after 3 attempt(s)" in errors[0].getMessage()

    @patch("src.scraper.requests.get")
    def test_retry_count_exactly(self, mock_get):
        mock_get.side_effect = [
            requests.exceptions.ConnectionError("c1"),
            _response(),
        ]

        result = fetch_page("https://example.com", retries=1, delay=0)

        assert mock_get.call_count == 2
        assert result.status_code == 200

    @patch("src.scraper.requests.get")
    def test_no_retry_on_404(self, mock_get, caplog):
        resp_wrong = _response(status_code=404)
        resp_wrong.raise_for_status.side_effect = _http_error(404)
        mock_get.return_value = resp_wrong

        with pytest.raises(requests.exceptions.HTTPError):
            fetch_page("https://example.com", retries=2, delay=0)

        assert mock_get.call_count == 1
        assert not any(
            r.levelno == logging.WARNING and "retrying" in r.getMessage()
            for r in caplog.records
        )

    @patch("src.scraper.requests.get")
    def test_retries_on_5xx_then_success(self, mock_get):
        resp_wrong = _response(status_code=503)
        resp_wrong.raise_for_status.side_effect = _http_error(503)
        mock_get.side_effect = [resp_wrong, _response()]

        result = fetch_page("https://example.com", retries=1, delay=0)

        assert mock_get.call_count == 2
        assert result.status_code == 200

    @patch("src.scraper.requests.get")
    def test_retries_zero_disables_retry_loop(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("t1")

        with pytest.raises(requests.exceptions.Timeout):
            fetch_page("https://example.com", retries=0, delay=0)

        assert mock_get.call_count == 1


class TestScrapePagesFaultTolerance:
    @patch("src.scraper.fetch_page")
    def test_failed_page_does_not_block_other_pages(self, mock_fetch, caplog):
        mock_fetch.side_effect = [
            _response(text=HTML_JOB),
            requests.exceptions.ConnectionError("page 2 down"),
            _response(text=HTML_JOB.replace("/1", "/3")),
        ]

        with caplog.at_level(logging.ERROR):
            jobs = scrape_pages("https://example.com/jobs", pages=3, retries=0)

        assert mock_fetch.call_count == 3
        assert len(jobs) == 2
        assert [j.url for j in jobs] == [
            "https://example.com/1",
            "https://example.com/3",
        ]
        errors = [r for r in caplog.records if r.levelno == logging.ERROR]
        assert any("Skipping page 2" in e.getMessage() for e in errors)

    @patch("src.scraper.fetch_page")
    def test_successful_pages_contribute_jobs(self, mock_fetch):
        mock_fetch.side_effect = [_response(), _response(text=HTML_JOB.replace("/1", "/2"))]

        jobs = scrape_pages("https://example.com/jobs", pages=2, retries=1)

        assert len(jobs) == 2
        assert [j.url for j in jobs] == [
            "https://example.com/1",
            "https://example.com/2",
        ]

    @patch("src.scraper.fetch_page")
    def test_all_pages_fail_returns_empty(self, mock_fetch, caplog):
        mock_fetch.side_effect = requests.exceptions.Timeout("all down")

        jobs = scrape_pages("https://example.com/jobs", pages=2, retries=0)

        assert jobs == []
        assert sum(
            1 for r in caplog.records if r.levelno == logging.ERROR
        ) == 2


class TestParserGracefulHandling:
    def test_malformed_html_no_offset_records(self):
        jobs = parse_jobs("<html><body><div><<<not valid html>>></div></body></html>")
        assert jobs == []

    def test_empty_page_returns_empty_list(self):
        assert parse_jobs("") == []
        assert parse_jobs("   \n  ") == []

    def test_unexpected_structure_returns_empty_list(self):
        html = (
            "<html><body><table><tr><td>Not a job card structure</td></tr></table>"
            "</body></html>"
        )
        assert parse_jobs(html) == []

    def test_missing_fields_logs_warning_keeps_record(self, caplog):
        html = '<div class="card"><div class="card-content"><p>junk</p></div></div>'

        with caplog.at_level(logging.WARNING):
            jobs = parse_jobs(html)

        assert len(jobs) == 1
        assert jobs[0].title == ""
        assert jobs[0].company == ""
        assert jobs[0].location == ""
        assert jobs[0].url == ""
        assert any("no extractable data" in r.getMessage() for r in caplog.records)


class TestTimeoutRetriesDefaults:
    def test_default_constants(self):
        assert DEFAULT_TIMEOUT == 10.0
        assert DEFAULT_RETRIES == 2