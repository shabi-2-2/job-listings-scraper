# Job Listings Scraper

## Objective
A Python-based web scraping application designed to extract, parse, model, export, and analyze job listing data from the Fake Jobs practice website.

## Target Website
- **URL**: https://realpython.github.io/fake-jobs/
- **Description**: A static mock job board provided by Real Python specifically designed for practicing web scraping techniques without rate limits or dynamic JavaScript rendering hurdles.

## Planned Technology Stack
- **Language**: Python 3.10+
- **HTTP Client**: `requests` (Phase 02)
- **HTML Parsing**: `beautifulsoup4` (Phase 03)
- **Data Modeling**: Standard library `dataclasses` (Phase 04)
- **Data Export**: Built-in `csv` module (Phase 05)
- **Logging & Error Handling**: Standard library `logging` (Phase 06)
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

## Project Roadmap
- [x] **Phase 01 — Project Setup & Web Fundamentals** (COMPLETE)
- [x] **Phase 02 — Fetch Webpage** (COMPLETE)
- [x] **Phase 03 — Parse HTML** (COMPLETE)
- [x] **Phase 04 — Job Data Model** (COMPLETE)
- [x] **Phase 05 — CSV Export** (COMPLETE)
- [x] **Phase 06 — Refactoring & Error Handling** (COMPLETE)
- [x] **Phase 07 — CLI** (COMPLETE)
- [x] **Phase 08 — Data Analysis** (COMPLETE)
- [ ] **Phase 09 — Advanced Features**
  - [x] **Phase 09.1 — Pagination / Multi-Page Scraping** (COMPLETE)
  - [x] **Phase 09.2 — Job Filtering** (COMPLETE)
  - [x] **Phase 09.3 — Job Deduplication** (COMPLETE)

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
`scrape_pages(start_url, pages)` handles per-page request failures gracefully. If an individual page encounters a network error, a warning is logged and scraping continues for the remaining pages, preventing the entire batch from crashing.

---

## Application Data Flow

The scraper follows a clean, decoupled data pipeline:

```
Command-Line Arguments (argparse: --url, --pages, --keyword/--location/--company, --output, --analyze)
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
src/exporter.py (export_jobs)                → CSV formatting & file export
    ↓
data/jobs.csv                                → Persisted tabular dataset
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
- **WARNING**: Non-fatal anomalies (empty HTML input, missing listing cards, failed page fetch).
- **ERROR**: Actionable failures (network timeouts, connection loss, file system permission errors).

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
