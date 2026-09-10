from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from main import DEFAULT_OUTPUT, DEFAULT_URL, main, parse_args
from src.models import Job


def test_parse_args_defaults():
    args = parse_args([])
    assert args.url == DEFAULT_URL
    assert args.output == DEFAULT_OUTPUT
    assert args.analyze is False


def test_parse_args_custom_url():
    args = parse_args(["--url", "https://example.com/jobs"])
    assert args.url == "https://example.com/jobs"
    assert args.output == DEFAULT_OUTPUT


def test_parse_args_custom_output():
    args = parse_args(["--output", "custom_data/out.csv"])
    assert args.url == DEFAULT_URL
    assert args.output == Path("custom_data/out.csv")


def test_parse_args_analyze_flag():
    args = parse_args(["--analyze"])
    assert args.analyze is True


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
    assert "--analyze" in captured.out


@patch("main.fetch_page")
@patch("main.parse_jobs")
@patch("main.export_jobs")
def test_main_execution_flow(mock_export, mock_parse, mock_fetch, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html></html>"
    mock_fetch.return_value = mock_response

    mock_jobs = [Job("Dev", "Corp", "Remote", "https://example.com")]
    mock_parse.return_value = mock_jobs

    main(["--url", "https://custom.com", "--output", "out.csv"])

    mock_fetch.assert_called_once_with("https://custom.com", timeout=10.0)
    mock_parse.assert_called_once_with("<html></html>", base_url="https://custom.com")
    mock_export.assert_called_once_with(mock_jobs, Path("out.csv"))

    captured = capsys.readouterr()
    assert "Starting job scraper..." in captured.out
    assert "Completed successfully." in captured.out


@patch("main.run_analysis")
def test_main_analyze_flow(mock_analysis):
    main(["--analyze", "--output", "data/custom.csv"])
    mock_analysis.assert_called_once_with(csv_path=Path("data/custom.csv"))
