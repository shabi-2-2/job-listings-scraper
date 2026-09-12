# Job Listings Scraper

A modular, fault-tolerant Python web scraper that extracts job listings from the fake-jobs practice board, parses and normalizes each listing into a typed model, and runs it through a configurable pipeline — pagination, URL-based deduplication, case-insensitive filtering, and CSV/JSON export. The pipeline is driven by a validated CLI with structured logging and retry/backoff handling, and exported datasets can be analyzed and visualized with pandas and Matplotlib.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2C8EBB)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-266b45)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)
![tests](https://img.shields.io/badge/tests-134%20passing-2EA043)

## Key Features
- **Multi-page scraping** — paginated fetching with per-page fault tolerance.
- **URL-based deduplication** — removes duplicate listings while preserving order.
- **Case-insensitive filtering** — by keyword, location, and company (AND logic).
- **CSV + JSON export** — default CSV, optional JSON, automatic directory creation.
- **Configurable output paths** — custom destinations via `--output`.
- **Structured logging** — INFO/DEBUG/WARNING levels via `-v` and `-q`.
- **Retry/backoff & timeouts** — bounded retries for timeouts, connection errors, and HTTP 5xx.
- **CLI configuration** — pages, filters, timeouts, retries, output, and analysis flags.
- **Analysis & visualization** — pandas statistics and Matplotlib charts in `data/plots/`.

## Target Website
- **URL**: https://realpython.github.io/fake-jobs/
- **Description**: A static mock job board provided by Real Python specifically designed for practicing web scraping techniques without rate limits or dynamic JavaScript rendering hurdles.

## Technology Stack
- **Language**: Python 3.10+
- **HTTP Client**: `requests` (Phase 02)
- **HTML Parsing**: `beautifulsoup4` (Phase 03)
- **Data Modeling**: Standard library `dataclasses` (Phase 04)
- **Data Export**: Built-in `csv` and `json` modules (Phases 05, 09.4)
- **Logging & Error Handling**: Standard library `logging` with structured application logging, CLI verbosity controls, and fault-tolerant request handling (Phases 06, 09.5, 09.6)
- **Command-Line Interface**: Standard library `argparse` (Phase 07)
- **Data Analysis & Visualization**: `pandas`, `matplotlib` (Phase 08)

## Current Development Phase
- **Phase 01 — Project Setup & Web Fundamentals**: COMPLETE
- **Phase 02 — Fetch Webpage**: COMPLETE
- **Phase 03 — Parse HTML & Job Extraction**: COMPLETE
- **Phase 04 — Job Data Model & Clean Data Flow**: COMPLETE
- **Phase 05 — CSV Export**: COMPLETE
- **Phase 06 — Refactoring & Error Handling**: COMPLETE
- **Phase 07 — Command-Line Interface (CLI)**: COMPLETE
- **Phase 08 — Data Analysis & Visualization**: COMPLETE
- **Phase 09.1 — Pagination / Multi-Page Scraping**: COMPLETE
- **Phase 09.2 — Job Filtering**: COMPLETE
- **Phase 09.3 — Job Deduplication**: COMPLETE
- **Phase 09.4 — Configurable Output**: COMPLETE
- **Phase 09.5 — Application Logging**: COMPLETE
- **Phase 09.6 — Robustness & Fault Tolerance**: COMPLETE
- **Phase 09.7 — Final Testing, Polish & Documentation**: COMPLETE

## Project Roadmap
- [x] **Phase 01 — Project Setup & Web Fundamentals** (COMPLETE)
- [x] **Phase 02 — Fetch Webpage** (COMPLETE)
- [x] **Phase 03 — Parse HTML** (COMPLETE)
- [x] **Phase 04 — Job Data Model** (COMPLETE)
- [x] **Phase 05 — CSV Export** (COMPLETE)
- [x] **Phase 06 — Refactoring & Error Handling** (COMPLETE)
- [x] **Phase 07 — CLI** (COMPLETE)
- [x] **Phase 08 — Data Analysis** (COMPLETE)
- [x] **Phase 09 — Advanced Features**
  - [x] **Phase 09.1 — Pagination / Multi-Page Scraping** (COMPLETE)
  - [x] **Phase 09.2 — Job Filtering** (COMPLETE)
  - [x] **Phase 09.3 — Job Deduplication** (COMPLETE)
  - [x] **Phase 09.4 — Configurable Output** (COMPLETE)
  - [x] **Phase 09.5 — Application Logging** (COMPLETE)
  - [x] **Phase 09.6 — Robustness & Fault Tolerance** (COMPLETE)
  - [x] **Phase 09.7 — Final Testing & Documentation** (COMPLETE)

---

## Command-Line Interface (CLI) Usage

Command-line arguments allow users and automated workflows to configure the scraper and data analysis dynamically at runtime.

### 1. Default Run (Scrape & Export)
Scrapes the default target URL and writes to `data/jobs.csv`:
```bash
python main.py
```

### 2. Multi-Page Scraping (Phase 09.1)
Scrapes multiple pages and combines results into one dataset:
```bash
python main.py --pages 3
```

### 3. Filtering by Keyword (Phase 09.2)
Filters jobs whose title contains the keyword (case-insensitive):
```bash
python main.py --keyword python
```

### 4. Filtering by Location
Filters jobs matching the location field (case-insensitive):
```bash
python main.py --location remote
```

### 5. Filtering by Company
Filters jobs matching the company name (case-insensitive):
```bash
python main.py --company microsoft
```

### 6. Combining Filters with Pagination
Multiple filters combine with AND logic and work alongside `--pages`:
```bash
python main.py --pages 3 --keyword python --location remote
```

### 7. Custom Output File
Exports scraped jobs to a custom destination path:
```bash
python main.py --output data/python_jobs.csv
```

### 8. Custom Target URL and Output
Overrides target URL, page count, and export destination:
```bash
python main.py --url https://realpython.github.io/fake-jobs/ --pages 2 --output data/jobs.csv
```

### 9. Data Analysis Mode
Analyzes the existing `data/jobs.csv` dataset and generates charts in `data/plots/`:
```bash
python main.py --analyze
```

### 10. Analyze Custom CSV File
```bash
python main.py --analyze --output data/custom_jobs.csv
```

### 11. Display Help & Options
```bash
python main.py --help
```

### 12. Export Jobs as JSON (Phase 09.4)
Additionally exports the processed jobs to a JSON file placed next to the CSV output:
```bash
python main.py --json
```

Combined with a custom output path (parent directories are created automatically):
```bash
python main.py --output data/results/jobs.csv --json
```
Writes both `data/results/jobs.csv` and `data/results/jobs.json`.

### 13. Verbose Debug Logging
Enables DEBUG-level diagnostic output (network internals, pipeline configuration):
```bash
python main.py --verbose
# or
python main.py -v
```

### 14. Quiet Mode
Suppresses log output below the WARNING level; only user-facing results remain:
```bash
python main.py --quiet
# or
python main.py -q
```

### 15. Timeout and Retry Configuration (Phase 09.6)
Controls the per-attempt request timeout and how many retries are attempted for transient failures (timeouts, connection errors, HTTP 5xx):
```bash
python main.py --timeout 15 --retries 3
```
Defaults: `--timeout 10` (seconds), `--retries 2`.

---

## Robustness & Fault Tolerance (Phase 09.6)

### Request Timeouts
Every HTTP request carries an explicit timeout (`--timeout`, default 10 seconds) so no request can hang indefinitely. The timeout applies per attempt.

### Retry with Backoff
`fetch_page()` retries transient failures only:
- Request timeouts and connection errors.
- HTTP 5xx server responses (`500/501/502/503/504`).

Permanent failures such as ordinary 4xx responses are never retried. Retries are bounded (`--retries`, default 2, for a maximum of `retries + 1` attempts), with a small fixed backoff delay between attempts (`RETRY_DELAY`, 0.5s). Each retry is logged at WARNING level; an ultimate failure is logged at ERROR.

### Page-Level Fault Tolerance
`scrape_pages()` processes each page independently. If a page still fails after its retry attempts are exhausted, that page is logged and skipped, and the scraper continues with the remaining pages. Jobs from successful pages are always retained.

### Graceful Parsing
`parse_jobs()` never crashes on malformed or incomplete HTML:
- Empty or blank HTML returns an empty list.
- No job cards (or unexpected structure) returns an empty list.
- Cards missing title/company/location/url fields produce an empty record (never invented data) with a WARNING log.

### Logging Integration
Retry attempts and request failures use the Phase 09.5 logging system: DEBUG for detailed diagnostics, WARNING for recoverable (retried) failures, ERROR when an operation ultimately fails and pages are skipped.

---

## Application Logging (Phase 09.5)

### Why Logging?
Logging gives operators a structured, timestamped record of what the scraper did — which pages were fetched, how many jobs were parsed, deduplicated, filtered, and exported — without mixing diagnostic detail into the user-facing results that go to stdout.

### Central Configuration
Logging is configured once in `main.py` via `setup_logging(level)`. Every module (`src/scraper.py`, `src/parser.py`, `src/dedup.py`, `src/filter.py`, `src/exporter.py`, `src/analyzer.py`) declares its own module-level `logger = logging.getLogger(__name__)` and never configures root logging itself.

### Log Levels
- **INFO (default)**: Pipeline milestones — scraping start, per-page progress, job counts, deduplication/filtering results, exports, and completion.
- **DEBUG (`--verbose`/`-v`)**: Detailed diagnostics including pipeline configuration and HTTP internals.
- **WARNING (`--quiet`/`-q`)** or higher: Only warnings and errors — failed page fetches, missing job cards, and similar recoverable issues.

### Logged Pipeline Milestones
1. `Starting job scraping pipeline` with target URL, page count, and output path.
2. Per-page scraping and parse results (from `src.scraper` / `src.parser`).
3. `Scraping complete: found N job listings`.
4. Deduplication results (`src.dedup` logs `N -> M unique jobs`).
5. Filtering results (`src.filter` logs input/output counts).
6. CSV/JSON export results (`src.exporter` logs destination paths).
7. `Pipeline completed successfully` with the final exported count.

### Example Output
```text
2026-09-12 23:54:47 [INFO] __main__: Starting job scraping pipeline (target=https://realpython.github.io/fake-jobs/, pages=1, output=data/jobs.csv)
2026-09-12 23:54:47 [INFO] src.scraper: Scraping page 1 of 1 from https://realpython.github.io/fake-jobs/
2026-09-12 23:54:47 [INFO] src.parser: Successfully parsed 100 job listings.
2026-09-12 23:54:47 [INFO] src.dedup: Deduplicated 100 jobs -> 100 unique jobs
2026-09-12 23:54:47 [INFO] src.exporter: Successfully exported 100 jobs to data/jobs.csv
```

---

## Configurable Output (Phase 09.4)

### Custom CSV Output Path
`--output` accepts any file path. The default remains `data/jobs.csv`. If the parent directory does not exist, it is created automatically using `pathlib.Path.mkdir(parents=True, exist_ok=True)`.

### Optional JSON Export
Passing `--json` additionally writes the same processed jobs as a JSON file whose path is derived from the CSV output by replacing the `.csv` suffix with `.json`. Each JSON object contains the exact `Job` model fields: `title`, `company`, `location`, and `url`.

### Where JSON Export Lives in the Pipeline
JSON export happens at the same stage as CSV export — after deduplication and filtering — so both files always contain the same processed dataset.

---

## Job Filtering Concepts (Phase 09.2)

### Filtering Layer
`filter_jobs(jobs, keyword=None, location=None, company=None)` lives in `src/filter.py` and is applied between scraping/parsing and exporting:
1. Jobs are scraped across all requested pages.
2. `filter_jobs()` keeps only jobs matching every supplied criteria.
3. The filtered list is exported to CSV.

### Matching Rules
- **Keyword**: Case-insensitive substring match against the job title.
- **Location**: Case-insensitive substring match against the job location field.
- **Company**: Case-insensitive substring match against the company name.

### AND Logic
When multiple filters are supplied, a job must satisfy all of them to be kept. For example, `--keyword python --location remote` keeps only jobs whose title contains *python* **and** whose location contains *remote*.

### No Matches
Filtering that produces zero results is not an error. The application reports `No jobs matched the specified filters.` and still writes a valid CSV containing only the header row.

---

## Job Deduplication (Phase 09.3)

### Why Deduplication?
When scraping multiple pages, the same job listing can appear on multiple pages (e.g., a featured job that's pinned, or overlapping page boundaries). Without deduplication, the final dataset would contain duplicate records, distorting export counts, analysis statistics, and visualizations.

### URL as Unique Identifier
Each `Job` object has a `url` field pointing to the job's detail page. This URL is the canonical unique identifier — two `Job` objects with the same `url` represent the same listing, regardless of whether their `title`, `company`, or `location` fields differ.

### Automatic Deduplication
`deduplicate_jobs(jobs)` in `src/dedup.py` is applied after multi-page scraping and before filtering:
1. Jobs are scraped across all requested pages.
2. `deduplicate_jobs()` removes any records with duplicate URLs, keeping only the first occurrence.
3. The deduplicated list proceeds to filtering and export.

### Preserves Order
Deduplication preserves the order in which jobs first appeared. The first occurrence of each unique URL is kept; subsequent duplicates are discarded.

---

## Multi-Page Scraping Concepts (Phase 09.1)

### What is Multi-Page Scraping?
Most real-world websites divide large datasets across multiple paginated pages. Multi-page scraping systematically requests each successive page, extracts records using the core parser, and aggregates the results into a single dataset.

### URL Generation Strategy
`build_page_url(base_url, page)` standardizes query parameter handling:
- **Page 1**: Requests the initial base URL directly.
- **Page > 1**: Appends or updates the `page` query parameter (e.g. `https://realpython.github.io/fake-jobs/?page=2`) using Python's standard `urllib.parse` module.

### Fault-Tolerant Scraping
`scrape_pages(start_url, pages)` processes each page independently: if a page still fails after its retry attempts are exhausted, it is logged and skipped, and scraping continues with the remaining pages — the entire batch never crashes because of one page.

---

## Application Data Flow

The scraper follows a clean, decoupled data pipeline:

```
Command-Line Arguments (argparse: --url, --pages, --keyword/--location/--company,
--output, --json, --timeout, --retries, --analyze, --verbose/--quiet)
    ↓
Target URL, Page Count, Filters & Output Path
    ↓
src/scraper.py (scrape_pages -> fetch_page)  → Multi-page HTTP requests & fault tolerance
    ↓
HTML Response Text (per page)
    ↓
src/parser.py (parse_jobs)                   → BeautifulSoup parsing & whitespace normalization
    ↓
src/models.py (list[Job])                    → Strongly typed, aggregated Job objects
    ↓
src/dedup.py (deduplicate_jobs)              → URL-based duplicate removal
    ↓
src/filter.py (filter_jobs)                  → Case-insensitive keyword/location/company filtering
    ↓
src/exporter.py (export_jobs, export_jobs_json)  → CSV & optional JSON file export
    ↓
data/jobs.csv (+ data/jobs.json with --json)     → Persisted datasets
    ↓
src/analyzer.py (run_analysis)               → Pandas aggregation & Matplotlib visualizations
    ↓
data/plots/ (*.png)                          → Exported chart figures
```

`main.py` coordinates this pipeline end-to-end with centralized logging, argument validation, and safe exception handling.

---

## Data Analysis & Visualization (Phase 08)

### Why Pandas is Useful
`pandas` provides high-performance data structures and analytical functions optimized for tabular data. It simplifies aggregation, filtering, missing value handling, and frequency analysis without manual iteration.

### What is a DataFrame?
A `DataFrame` is a two-dimensional, size-mutable, tabular data structure with labeled axes (rows and columns). In our pipeline, the CSV is loaded directly into a DataFrame where each row corresponds to a job listing.

### Generated Statistics
1. **Total Jobs**: Total volume of job postings analyzed.
2. **Unique Companies**: Number of distinct hiring companies.
3. **Unique Locations**: Number of distinct job locations.
4. **Top Companies**: Companies offering the highest number of listings.
5. **Top Locations**: Geographic locations with the highest concentration of openings.
6. **Top Job Titles**: Most frequently posted job titles.

### Generated Visualizations
Visualizations are automatically saved to `data/plots/`:
- `data/plots/top_locations.png`: Bar chart of the top job locations.
- `data/plots/top_companies.png`: Bar chart of the top hiring companies.
- `data/plots/top_titles.png`: Bar chart of the most common job titles.

---

## Refactoring & Error Handling Concepts (Phase 06)

### Logging Strategy
The application uses Python's standard `logging` library with structured module-level loggers (`logging.getLogger(__name__)`). Operations are categorized with appropriate severity levels:
- **DEBUG**: Fine-grained diagnostic information.
- **INFO**: Milestones in execution (fetching URLs, parse counts, export completion).
- **WARNING**: Non-fatal anomalies (empty HTML input, missing listing cards, retried request failures).
- **ERROR**: Actionable failures (requests that fail after retries, file system permission errors).

### Layer-Appropriate Error Handling
Errors are captured and reported close to where they occur:
1. **Scraper (`scraper.py`)**: Intercepts `Timeout`, `ConnectionError`, and `HTTPError`.
2. **Parser (`parser.py`)**: Handles malformed HTML, missing nodes, and empty inputs gracefully.
3. **Exporter (`exporter.py`)**: Catches `OSError` / file write issues.
4. **Analyzer (`analyzer.py`)**: Validates CSV existence, content, and required columns.
5. **Orchestrator (`main.py`)**: Catches expected layer exceptions and exits cleanly with code `1`.

---

## CSV Export Concepts (Phase 05)

### What is CSV?
CSV (Comma-Separated Values) is a plain-text file format for storing tabular data. Each line in a CSV file corresponds to a data record/row, and each record contains one or more fields separated by commas.

### Why CSV is Useful for Scraped Data
- **Portability**: Plain-text format compatible with spreadsheet software (Excel, Google Sheets) and data tools (Pandas, SQL databases).
- **Simplicity**: Does not require external server software, binary codecs, or relational database setup.
- **Human-Readable**: Easy to inspect, verify, and version control.

---

## Data Modeling Concepts (Phase 04)

### What is a Data Model?
A data model defines the logical structure, fields, and types of data within an application.

### Why Use a Dataclass?
Python's built-in `@dataclass` decorator automatically generates boilerplate methods such as `__init__`, `__repr__`, and `__eq__` based on class field annotations.

### What `Job` Represents
The `Job` dataclass represents a single job posting extracted from the website with normalized fields:
- `title` (str): Title of the position
- `company` (str): Hiring organization
- `location` (str): Location of the role
- `url` (str): Full absolute link to job details / application

---

## Web & HTTP Concepts (Phase 02)

### What is HTTP?
HTTP (Hypertext Transfer Protocol) is the foundational protocol used for transmitting data across the World Wide Web.

### What is an HTTP GET Request?
An HTTP GET request is a method used to retrieve data from a specified resource on a web server without modifying server state.

### What is the `requests` Library?
`requests` is an HTTP library for Python designed to make sending HTTP/1.1 requests simple and human-friendly.

### What is an HTTP Status Code?
An HTTP status code is a three-digit integer returned by the server indicating the outcome of the request (`200 OK`, `404 Not Found`, `500 Internal Server Error`).

---

## HTML Parsing & Extraction Concepts (Phase 03)

### What is HTML Parsing?
HTML parsing is the process of taking a raw string of HTML text and converting it into a structured, navigable hierarchical tree structure (Document Object Model) in memory.

### What is BeautifulSoup?
`BeautifulSoup` (`bs4`) is a Python parsing library that traverses and searches HTML and XML documents using methods like `find` and `find_all`.

---

## Website Structure & Inspection

Inspection of `https://realpython.github.io/fake-jobs/` identified the following HTML architecture:

### 1. Overall Container & Multiple Listings
- All job cards reside inside a parent `div` element with `id="ResultsContainer"` (`<div id="ResultsContainer" class="columns is-multiline">`).
- Each individual listing is wrapped in a `<div class="column is-half">`.

### 2. Individual Job Listing Card
- Each listing is encapsulated in a Bulma card component: `<div class="card"><div class="card-content">...</div></div>`.

### 3. Key Data Elements
| Field | HTML Element & Selector | Example Content / Attribute |
| :--- | :--- | :--- |
| **Job Title** | `<h2 class="title is-5">` | `Senior Python Developer` |
| **Company Name** | `<h3 class="subtitle is-6 company">` | `Payne, Roberts and Davis` |
| **Location** | `<p class="location">` | `Stewartbury, AA` |
| **Date Posted** | `<time datetime="YYYY-MM-DD">` | `2021-04-08` |
| **Job Detail / Apply URL** | Second `<a>` tag inside `<footer class="card-footer">` (`class="card-footer-item"`) | `href="https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html"` |

---

## Project Structure

```
main.py                 # CLI entry point: argument parsing, logging setup, pipeline orchestration
requirements.txt        # Runtime dependencies
data/jobs.csv           # Default scraped dataset
data/plots/             # Generated analysis charts
src/
├── scraper.py          # HTTP fetching, retries, multi-page scraping
├── parser.py           # HTML -> Job objects
├── models.py           # Job dataclass
├── dedup.py            # URL-based deduplication
├── filter.py           # Keyword/location/company filtering
├── exporter.py         # CSV & JSON export
└── analyzer.py         # pandas statistics & Matplotlib charts
tests/                  # Test suite (one file per module)
```

---

## Getting Started

### 1. Virtual Environment Setup
Activate the `.venv` environment:

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Entry Point (Scrape & Export)
```bash
# Default (1 page)
python main.py

# Multi-page
python main.py --pages 3

# Multi-page with filters
python main.py --pages 3 --keyword python --location remote
```

### 4. Run Analysis Mode
```bash
python main.py --analyze
```

### 5. Run Tests
```bash
pytest
# or
python -m unittest discover -s tests
```
