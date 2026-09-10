# Job Listings Scraper

## Objective
A Python-based web scraping application designed to extract, parse, model, and export job listing data from the Fake Jobs practice website.

## Target Website
- **URL**: https://realpython.github.io/fake-jobs/
- **Description**: A static mock job board provided by Real Python specifically designed for practicing web scraping techniques without rate limits or dynamic JavaScript rendering hurdles.

## Planned Technology Stack
- **Language**: Python 3.10+
- **HTTP Client**: `requests` (Phase 02)
- **HTML Parsing**: `beautifulsoup4` (Phase 03)
- **Data Modeling**: Standard library `dataclasses` (Phase 04)
- **Data Export & CLI**: Built-in `csv` module (Phase 05), standard library / `argparse`
- **Logging & Error Handling**: Standard library `logging` (Phase 06)

## Current Development Phase
- **Phase 01 — Project Setup & Web Fundamentals**: COMPLETE
- **Phase 02 — Fetch Webpage**: COMPLETE
- **Phase 03 — Parse HTML & Job Extraction**: COMPLETE
- **Phase 04 — Job Data Model & Clean Data Flow**: COMPLETE
- **Phase 05 — CSV Export**: COMPLETE
- **Phase 06 — Refactoring & Error Handling**: COMPLETE

## Project Roadmap
- [x] **Phase 01 — Project Setup & Web Fundamentals** (COMPLETE)
- [x] **Phase 02 — Fetch Webpage** (COMPLETE)
- [x] **Phase 03 — Parse HTML** (COMPLETE)
- [x] **Phase 04 — Job Data Model** (COMPLETE)
- [x] **Phase 05 — CSV Export** (COMPLETE)
- [x] **Phase 06 — Refactoring & Error Handling** (COMPLETE)
- [ ] **Phase 07 — CLI**
- [ ] **Phase 08 — Data Analysis**
- [ ] **Phase 09 — Advanced Features**

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
data/jobs.csv                     → Final persisted tabular dataset
```

`main.py` coordinates this pipeline end-to-end with centralized logging and safe exception handling.

---

## Refactoring & Error Handling Concepts (Phase 06)

### Logging Strategy
The application uses Python's standard `logging` library with structured module-level loggers (`logging.getLogger(__name__)`). Operations are categorized with appropriate severity levels:
- **DEBUG**: Fine-grained diagnostic information (e.g., HTML character length).
- **INFO**: Milestones in execution (fetching URLs, parse counts, export completion).
- **WARNING**: Non-fatal anomalies (empty HTML input, missing listing cards).
- **ERROR**: Actionable failures (network timeouts, connection loss, file system permission errors).

### Layer-Appropriate Error Handling
Errors are captured and reported close to where they occur:
1. **Scraper (`scraper.py`)**: Intercepts `Timeout`, `ConnectionError`, and `HTTPError`, logging clear diagnostic information and raising informative exceptions without returning fake responses.
2. **Parser (`parser.py`)**: Handles malformed HTML, missing nodes, and empty inputs gracefully without throwing uncaught exceptions, logging warnings and returning an empty list when no listings are found.
3. **Exporter (`exporter.py`)**: Catches `OSError` / file write issues, logs path-specific errors, and ensures directory trees are created cleanly.
4. **Orchestrator (`main.py`)**: Catches expected layer exceptions, presents user-friendly terminal output instead of raw stack traces, and terminates with a non-zero exit code (`sys.exit(1)`).

---

## CSV Export Concepts (Phase 05)

### What is CSV?
CSV (Comma-Separated Values) is a plain-text file format for storing tabular data. Each line in a CSV file corresponds to a data record/row, and each record contains one or more fields separated by commas.

### Why CSV is Useful for Scraped Data
- **Portability**: Plain-text format compatible with spreadsheet software (Excel, Google Sheets) and data tools (Pandas, SQL databases).
- **Simplicity**: Does not require external server software, binary codecs, or relational database setup.
- **Human-Readable**: Easy to inspect, verify, and version control.

### How Python's `csv` Module Works
Python's standard library `csv` module provides `csv.writer` and `csv.DictWriter` to serialize collections of objects into RFC 4180-compliant CSV lines. It automatically handles quoting strings that contain commas, quotes, or newlines, with consistent UTF-8 encoding.

---

## Data Modeling Concepts (Phase 04)

### What is a Data Model?
A data model defines the logical structure, fields, and types of data within an application. Instead of passing around untyped dictionaries or raw tuples, a data model establishes a formal contract for what attributes an entity contains.

### Why Use a Dataclass?
Python's built-in `@dataclass` decorator automatically generates boilerplate methods such as `__init__`, `__repr__`, and `__eq__` based on class field annotations. It ensures type clarity and IDE autocompletion without external dependencies.

### What `Job` Represents
The `Job` dataclass represents a single job posting extracted from the website with normalized fields:
- `title` (str): Title of the position
- `company` (str): Hiring organization
- `location` (str): Location of the role
- `url` (str): Full absolute link to job details / application

---

## Web & HTTP Concepts (Phase 02)

### What is HTTP?
HTTP (Hypertext Transfer Protocol) is the foundational protocol used for transmitting data across the World Wide Web. It operates on a client-server model where a client sends a request to a server, and the server returns a response containing data such as HTML.

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

### 3. Run Entry Point
```bash
python main.py
```

### 4. Run Tests
```bash
pytest
# or
python -m unittest discover -s tests
```
