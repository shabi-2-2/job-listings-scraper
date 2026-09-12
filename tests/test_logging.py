import logging
from pathlib import Path
from unittest.mock import patch
import pytest
from main import main, parse_args, setup_logging
from src.models import Job


def _job(url: str = "https://example.com") -> Job:
    return Job("Dev", "Corp", "Remote", url)


def test_parse_args_verbosity_defaults():
    args = parse_args([])
    assert args.verbose is False
    assert args.quiet is False


def test_parse_args_verbose_short_flag():
    args = parse_args(["-v"])
    assert args.verbose is True
    assert args.quiet is False


def test_parse_args_verbose_long_flag():
    args = parse_args(["--verbose"])
    assert args.verbose is True


def test_parse_args_quiet_short_flag():
    args = parse_args(["-q"])
    assert args.quiet is True
    assert args.verbose is False


def test_parse_args_quiet_long_flag():
    args = parse_args(["--quiet"])
    assert args.quiet is True


def test_parse_args_verbose_and_quiet_conflict():
    with pytest.raises(SystemExit):
        parse_args(["--verbose", "--quiet"])


def test_parse_args_help_includes_verbosity_options(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--help"])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "--verbose" in captured.out
    assert "--quiet" in captured.out


def test_setup_logging_default_level_info():
    setup_logging(logging.INFO)
    assert logging.getLogger().getEffectiveLevel() == logging.INFO


def test_setup_logging_verbose_uses_debug():
    setup_logging(logging.DEBUG)
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG


def test_setup_logging_quiet_uses_warning():
    setup_logging(logging.WARNING)
    assert logging.getLogger().getEffectiveLevel() == logging.WARNING


def test_setup_logging_repeat_call_updates_level():
    setup_logging(logging.INFO)
    setup_logging(logging.DEBUG)
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG


@patch("main.scrape_pages")
@patch("main.export_jobs")
def test_pipeline_logs_info_milestones(mock_export, mock_scrape, caplog):
    mock_scrape.return_value = [_job()]

    main(["--url", "https://custom.com", "--output", "out.csv"])

    main_records = [r.getMessage() for r in caplog.records if r.name == "main"]
    assert any("Starting job scraping pipeline" in m for m in main_records)
    assert any("Scraping complete: found 1 job listings" in m for m in main_records)
    assert any("Pipeline completed successfully" in m for m in main_records)


@patch("main.scrape_pages")
@patch("main.export_jobs")
def test_pipeline_logs_warning_when_no_jobs(mock_export, mock_scrape, caplog):
    mock_scrape.return_value = []

    main(["--url", "https://custom.com", "--output", "out.csv"])

    assert any(
        rec.levelno == logging.WARNING
        and "No job listings were found" in rec.getMessage()
        for rec in caplog.records
    )


@patch("main.scrape_pages")
@patch("main.export_jobs")
def test_verbose_flag_emits_debug_records(mock_export, mock_scrape, caplog):
    mock_scrape.return_value = [_job()]

    main(["--verbose", "--url", "https://custom.com", "--output", "out.csv"])

    assert any(rec.levelno == logging.DEBUG for rec in caplog.records)
    assert any(
        rec.name == "main" and "Pipeline configuration" in rec.getMessage()
        for rec in caplog.records
        if rec.levelno == logging.DEBUG
    )


@patch("main.scrape_pages")
@patch("main.export_jobs")
def test_default_info_suppresses_debug_records(mock_export, mock_scrape, caplog):
    mock_scrape.return_value = [_job()]

    main(["--url", "https://custom.com", "--output", "out.csv"])

    assert not any(
        rec.levelno == logging.DEBUG and rec.name == "main"
        for rec in caplog.records
    )


@patch("main.scrape_pages")
@patch("main.export_jobs")
def test_logging_does_not_alter_exported_data(mock_export, mock_scrape, caplog):
    jobs = [_job(), _job("https://example.com/2")]
    mock_scrape.return_value = jobs

    main(["--url", "https://custom.com", "--output", "out.csv"])

    mock_export.assert_called_once_with(jobs, Path("out.csv"))
    assert len(caplog.records) > 0