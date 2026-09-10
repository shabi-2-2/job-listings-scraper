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

---

## Command-Line Interface (CLI) Usage (Phase 07 & 08)

Command-line arguments allow users and automated workflows to configure the scraper and data analysis dynamically at runtime.

### 1. Default Run (Scrape & Export)
Scrapes the default target URL and writes to `data/jobs.csv`:
```bash
python main.py
```

### 2. Custom Output File
Exports scraped jobs to a custom destination path:
```bash
python main.py --output data/python_jobs.csv
```

### 3. Custom Target URL and Output
Overrides both target URL and export destination:
```bash
python main.py --url https://realpython.github.io/fake-jobs/ --output data/jobs.csv
```

### 4. Data Analysis Mode
Analyzes the existing `data/jobs.csv` dataset and generates charts in `data/plots/`:
```bash
python main.py --analyze
```

### 5. Analyze Custom CSV File
```bash
python main.py --analyze --output data/custom_jobs.csv
```

### 6. Display Help & Options
```bash
python main.py --help
```

---

## Application Data Flow

The scraper follows a clean, decoupled data pipeline:

```
Website (https://realpython.github.io/fake-jobs/)
    ↓
src/scraper.py (fetch_page)       → HTTP GET request, timeout & error handling
    ↓
HTML Response Text
    ↓
src/parser.py (parse_jobs)        → BeautifulSoup parsing & whitespace normalization
    ↓
src/models.py (list[Job])         → Strongly typed, structured Job objects
    ↓
src/exporter.py (export_jobs)     → CSV formatting & file export
    ↓
data/jobs.csv                     → Persisted tabular dataset
    ↓
src/analyzer.py (run_analysis)    → Pandas aggregation & Matplotlib visualizations
    ↓
data/plots/ (*.png)               → Exported chart figures
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
- **WARNING**: Non-fatal anomalies (empty HTML input, missing listing cards).
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
python main.py
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
