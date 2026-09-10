import csv
from pathlib import Path
import pytest
from src.exporter import export_jobs
from src.models import Job


def test_export_creates_file_and_headers(tmp_path: Path):
    output_file = tmp_path / "jobs.csv"
    export_jobs([], output_file)

    assert output_file.exists()
    with open(output_file, mode="r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        assert len(reader) == 1
        assert reader[0] == ["title", "company", "location", "url"]


def test_export_single_job(tmp_path: Path):
    output_file = tmp_path / "jobs.csv"
    job = Job(
        title="Python Developer",
        company="Tech Corp",
        location="New York",
        url="https://example.com/job/1",
    )
    export_jobs([job], output_file)

    with open(output_file, mode="r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        assert len(reader) == 2
        assert reader[0] == ["title", "company", "location", "url"]
        assert reader[1] == [
            "Python Developer",
            "Tech Corp",
            "New York",
            "https://example.com/job/1",
        ]


def test_export_multiple_jobs(tmp_path: Path):
    output_file = tmp_path / "jobs.csv"
    jobs = [
        Job("Title 1", "Company 1", "Location 1", "https://example.com/1"),
        Job("Title 2", "Company 2", "Location 2", "https://example.com/2"),
        Job("Title 3", "Company 3", "Location 3", "https://example.com/3"),
    ]
    export_jobs(jobs, output_file)

    with open(output_file, mode="r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        assert len(reader) == 4
        assert reader[0] == ["title", "company", "location", "url"]
        assert reader[1] == ["Title 1", "Company 1", "Location 1", "https://example.com/1"]
        assert reader[2] == ["Title 2", "Company 2", "Location 2", "https://example.com/2"]
        assert reader[3] == ["Title 3", "Company 3", "Location 3", "https://example.com/3"]


def test_export_creates_nested_directories(tmp_path: Path):
    output_file = tmp_path / "nested" / "subfolder" / "jobs.csv"
    assert not output_file.parent.exists()

    job = Job("Dev", "Corp", "Remote", "https://example.com")
    export_jobs([job], output_file)

    assert output_file.exists()


def test_export_escapes_special_characters(tmp_path: Path):
    output_file = tmp_path / "jobs.csv"
    job = Job(
        title='Senior "Lead" Developer, Core Team',
        company="Payne, Roberts and Davis",
        location="Stewartbury, AA",
        url="https://example.com/job/special?a=1&b=2",
    )
    export_jobs([job], output_file)

    with open(output_file, mode="r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        assert len(reader) == 2
        assert reader[1] == [
            'Senior "Lead" Developer, Core Team',
            "Payne, Roberts and Davis",
            "Stewartbury, AA",
            "https://example.com/job/special?a=1&b=2",
        ]
