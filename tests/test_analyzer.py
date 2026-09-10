import csv
from pathlib import Path
import pandas as pd
import pytest
from src.analyzer import (
    clean_data,
    generate_visualizations,
    get_top_companies,
    get_top_job_titles,
    get_top_locations,
    get_total_jobs,
    get_unique_companies,
    get_unique_locations,
    load_jobs,
)


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    file_path = tmp_path / "jobs.csv"
    rows = [
        ["title", "company", "location", "url"],
        ["Software Engineer", "Tech Corp", "New York", "https://example.com/1"],
        ["Software Engineer", "Tech Corp", "New York", "https://example.com/1"],
        ["  Data Scientist  ", " Data LLC ", "  Austin, TX  ", "https://example.com/2"],
        ["Backend Developer", "Tech Corp", "Austin, TX", "https://example.com/3"],
        ["Frontend Developer", "Web Inc", "Chicago", "https://example.com/4"],
    ]
    with open(file_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return file_path


def test_load_jobs_success(sample_csv: Path):
    df = load_jobs(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert set(df.columns) == {"title", "company", "location", "url"}


def test_load_jobs_file_not_found(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_jobs(tmp_path / "non_existent.csv")


def test_load_jobs_empty_file(tmp_path: Path):
    empty_file = tmp_path / "empty.csv"
    empty_file.touch()
    with pytest.raises(ValueError):
        load_jobs(empty_file)


def test_load_jobs_missing_columns(tmp_path: Path):
    bad_csv = tmp_path / "bad.csv"
    with open(bad_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "location"])
    with pytest.raises(ValueError):
        load_jobs(bad_csv)


def test_clean_data(sample_csv: Path):
    df = load_jobs(sample_csv)
    cleaned = clean_data(df)
    assert len(cleaned) == 4
    row = cleaned[cleaned["url"] == "https://example.com/2"].iloc[0]
    assert row["title"] == "Data Scientist"
    assert row["company"] == "Data LLC"
    assert row["location"] == "Austin, TX"


def test_statistics(sample_csv: Path):
    df = clean_data(load_jobs(sample_csv))
    assert get_total_jobs(df) == 4
    assert get_unique_companies(df) == 3
    assert get_unique_locations(df) == 3

    top_companies = get_top_companies(df, n=2)
    assert top_companies.iloc[0] == 2
    assert top_companies.index[0] == "Tech Corp"

    top_locations = get_top_locations(df, n=2)
    assert top_locations.iloc[0] == 2
    assert top_locations.index[0] == "Austin, TX"

    top_titles = get_top_job_titles(df, n=2)
    assert len(top_titles) == 2


def test_generate_visualizations(sample_csv: Path, tmp_path: Path):
    df = clean_data(load_jobs(sample_csv))
    plots_dir = tmp_path / "plots"
    plots = generate_visualizations(df, output_dir=plots_dir)

    assert len(plots) == 3
    assert (plots_dir / "top_locations.png").exists()
    assert (plots_dir / "top_companies.png").exists()
    assert (plots_dir / "top_titles.png").exists()
