import logging
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"title", "company", "location", "url"}


def load_jobs(csv_path: str | Path) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        logger.error("CSV file not found at %s", path)
        raise FileNotFoundError(f"CSV file not found: {path}")

    try:
        df = pd.read_csv(path, dtype=str)
    except pd.errors.EmptyDataError as err:
        logger.error("CSV file is empty: %s", path)
        raise ValueError(f"CSV file is empty: {path}") from err
    except Exception as err:
        logger.error("Failed to read CSV at %s: %s", path, err)
        raise ValueError(f"Failed to read CSV at {path}: {err}") from err

    if not REQUIRED_COLUMNS.issubset(set(df.columns)):
        missing = REQUIRED_COLUMNS - set(df.columns)
        logger.error("CSV missing required columns: %s", missing)
        raise ValueError(f"CSV file missing required columns: {missing}")

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    for col in REQUIRED_COLUMNS:
        cleaned[col] = cleaned[col].fillna("").astype(str).str.strip()

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    return cleaned


def get_total_jobs(df: pd.DataFrame) -> int:
    return len(df)


def get_unique_companies(df: pd.DataFrame) -> int:
    valid = df[df["company"] != ""]["company"]
    return int(valid.nunique())


def get_unique_locations(df: pd.DataFrame) -> int:
    valid = df[df["location"] != ""]["location"]
    return int(valid.nunique())


def get_top_companies(df: pd.DataFrame, n: int = 5) -> pd.Series:
    valid = df[df["company"] != ""]["company"]
    return valid.value_counts().head(n)


def get_top_locations(df: pd.DataFrame, n: int = 5) -> pd.Series:
    valid = df[df["location"] != ""]["location"]
    return valid.value_counts().head(n)


def get_top_job_titles(df: pd.DataFrame, n: int = 5) -> pd.Series:
    valid = df[df["title"] != ""]["title"]
    return valid.value_counts().head(n)


def generate_visualizations(
    df: pd.DataFrame, output_dir: str | Path = "data/plots"
) -> list[Path]:
    dir_path = Path(output_dir)
    dir_path.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    top_locs = get_top_locations(df, n=10)
    if not top_locs.empty:
        plt.figure(figsize=(10, 6))
        top_locs.sort_values().plot(kind="barh", color="#2b5c8f")
        plt.title("Top Job Locations")
        plt.xlabel("Number of Job Postings")
        plt.ylabel("Location")
        plt.tight_layout()
        loc_path = dir_path / "top_locations.png"
        plt.savefig(loc_path, dpi=150)
        plt.close()
        generated.append(loc_path)

    top_comps = get_top_companies(df, n=10)
    if not top_comps.empty:
        plt.figure(figsize=(10, 6))
        top_comps.sort_values().plot(kind="barh", color="#2a9d8f")
        plt.title("Top Companies by Job Postings")
        plt.xlabel("Number of Job Postings")
        plt.ylabel("Company")
        plt.tight_layout()
        comp_path = dir_path / "top_companies.png"
        plt.savefig(comp_path, dpi=150)
        plt.close()
        generated.append(comp_path)

    top_titles = get_top_job_titles(df, n=10)
    if not top_titles.empty:
        plt.figure(figsize=(10, 6))
        top_titles.sort_values().plot(kind="barh", color="#e76f51")
        plt.title("Top Job Titles")
        plt.xlabel("Number of Job Postings")
        plt.ylabel("Job Title")
        plt.tight_layout()
        title_path = dir_path / "top_titles.png"
        plt.savefig(title_path, dpi=150)
        plt.close()
        generated.append(title_path)

    logger.info("Generated %d visualizations in %s", len(generated), dir_path)
    return generated
