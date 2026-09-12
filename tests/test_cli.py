from pathlib import Path
from unittest.mock import patch
import pytest
from main import DEFAULT_OUTPUT, DEFAULT_URL, main, parse_args
from src.models import Job


def test_parse_args_defaults():
    args = parse_args([])
    assert args.url == DEFAULT_URL
    assert args.output == DEFAULT_OUTPUT
    assert args.pages == 1
    assert args.analyze is False
    assert args.keyword is None
    assert args.location is None
    assert args.company is None


def test_parse_args_custom_url():
    args = parse_args(["--url", "https://example.com/jobs"])
    assert args.url == "https://example.com/jobs"
    assert args.output == DEFAULT_OUTPUT


def test_parse_args_custom_output():
    args = parse_args(["--output", "custom_data/out.csv"])
    assert args.url == DEFAULT_URL
    assert args.output == Path("custom_data/out.csv")


def test_parse_args_custom_pages():
    args = parse_args(["--pages", "3"])
    assert args.pages == 3


def test_parse_args_invalid_pages_zero():
    with pytest.raises(SystemExit):
        parse_args(["--pages", "0"])


def test_parse_args_invalid_pages_negative():
    with pytest.raises(SystemExit):
        parse_args(["--pages", "-2"])


def test_parse_args_analyze_flag():
    args = parse_args(["--analyze"])
    assert args.analyze is True


def test_parse_args_json_flag():
    args = parse_args(["--json"])
    assert args.json is True


def test_parse_args_json_default_false():
    args = parse_args([])
    assert args.json is False


def test_parse_args_help_includes_json(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "--json" in captured.out


def test_parse_args_custom_url_and_output():
    args = parse_args(["--url", "https://example.com", "--output", "out.csv"])
    assert args.url == "https://example.com"
    assert args.output == Path("out.csv")


def test_parse_args_empty_url():
    with pytest.raises(SystemExit):
        parse_args(["--url", "   "])


def test_parse_args_unknown_argument():
    with pytest.raises(SystemExit):
        parse_args(["--unknown-flag"])


def test_parse_args_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "--url" in captured.out
    assert "--output" in captured.out
    assert "--pages" in captured.out
    assert "--keyword" in captured.out
    assert "--location" in captured.out
    assert "--company" in captured.out
    assert "--analyze" in captured.out


def test_parse_args_filter_keyword():
    args = parse_args(["--keyword", "python"])
    assert args.keyword == "python"
    assert args.location is None
    assert args.company is None


def test_parse_args_filter_location():
    args = parse_args(["--location", "remote"])
    assert args.location == "remote"
    assert args.keyword is None
    assert args.company is None


def test_parse_args_filter_company():
    args = parse_args(["--company", "google"])
    assert args.company == "google"
    assert args.keyword is None
    assert args.location is None


def test_parse_args_all_filters():
    args = parse_args(["--keyword", "python", "--location", "remote", "--company", "acme"])
    assert args.keyword == "python"
    assert args.location == "remote"
    assert args.company == "acme"


@patch("main.scrape_pages")
@patch("main.export_jobs")
def test_main_execution_flow(mock_export, mock_scrape, capsys):
    mock_jobs = [Job("Dev", "Corp", "Remote", "https://example.com")]
    mock_scrape.return_value = mock_jobs

    main(["--url", "https://custom.com", "--output", "out.csv", "--pages", "2"])

    mock_scrape.assert_called_once_with(
        start_url="https://custom.com", pages=2, timeout=10.0
    )
    mock_export.assert_called_once_with(mock_jobs, Path("out.csv"))

    captured = capsys.readouterr()
    assert "Starting job scraper..." in captured.out
    assert "Completed successfully." in captured.out


@patch("main.scrape_pages")
@patch("main.filter_jobs")
@patch("main.export_jobs")
def test_main_filters_with_pages(mock_export, mock_filter, mock_scrape, capsys):
    mock_jobs = [Job("Python Dev", "Corp", "Remote", "https://example.com")]
    mock_filtered = [mock_jobs[0]]
    mock_scrape.return_value = mock_jobs
    mock_filter.return_value = mock_filtered

    main(
        [
            "--url",
            "https://custom.com",
            "--pages",
            "3",
            "--keyword",
            "python",
            "--location",
            "remote",
        ]
    )

    mock_scrape.assert_called_once_with(
        start_url="https://custom.com", pages=3, timeout=10.0
    )
    mock_filter.assert_called_once_with(
        mock_jobs, keyword="python", location="remote", company=None
    )
    mock_export.assert_called_once_with(mock_filtered, Path("data/jobs.csv"))

    captured = capsys.readouterr()
    assert "Keyword: python" in captured.out
    assert "Location: remote" in captured.out
    assert "After filtering: 1 jobs." in captured.out


@patch("main.scrape_pages")
@patch("main.filter_jobs")
@patch("main.export_jobs")
def test_main_filters_zero_results(mock_export, mock_filter, mock_scrape, capsys):
    mock_jobs = [Job("Python Dev", "Corp", "Remote", "https://example.com")]
    mock_scrape.return_value = mock_jobs
    mock_filter.return_value = []

    main(["--keyword", "rust"])

    mock_export.assert_called_once_with([], Path("data/jobs.csv"))
    captured = capsys.readouterr()
    assert "No jobs matched the specified filters." in captured.out


@patch("main.run_analysis")
def test_main_analyze_flow(mock_analysis):
    main(["--analyze", "--output", "data/custom.csv"])
    mock_analysis.assert_called_once_with(csv_path=Path("data/custom.csv"))


@patch("main.scrape_pages")
@patch("main.export_jobs_json")
@patch("main.export_jobs")
def test_main_json_flag_exports_json(mock_export, mock_export_json, mock_scrape, capsys):
    mock_jobs = [Job("Dev", "Corp", "Remote", "https://example.com")]
    mock_scrape.return_value = mock_jobs

    main(["--url", "https://custom.com", "--output", "out.csv", "--json"])

    mock_export.assert_called_once_with(mock_jobs, Path("out.csv"))
    mock_export_json.assert_called_once_with(mock_jobs, Path("out.json"))
    captured = capsys.readouterr()
    assert "Exported 1 jobs to out.json" in captured.out


@patch("main.scrape_pages")
@patch("main.export_jobs_json")
@patch("main.export_jobs")
def test_main_no_json_flag_skips_json(mock_export, mock_export_json, mock_scrape):
    mock_jobs = [Job("Dev", "Corp", "Remote", "https://example.com")]
    mock_scrape.return_value = mock_jobs

    main(["--url", "https://custom.com", "--output", "out.csv"])

    mock_export.assert_called_once_with(mock_jobs, Path("out.csv"))
    mock_export_json.assert_not_called()


@patch("main.scrape_pages")
@patch("main.export_jobs_json")
@patch("main.export_jobs")
def test_main_json_flag_writes_empty_json(mock_export, mock_export_json, mock_scrape):
    mock_scrape.return_value = []

    main(["--json"])

    mock_export.assert_called_once_with([], Path("data/jobs.csv"))
    mock_export_json.assert_called_once_with([], Path("data/jobs.json"))
