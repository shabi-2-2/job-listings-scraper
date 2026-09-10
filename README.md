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

## Current Development Phase
- **Phase 01 — Project Setup & Web Fundamentals**: COMPLETE
- **Phase 02 — Fetch Webpage**: COMPLETE
- **Phase 03 — Parse HTML & Job Extraction**: COMPLETE
- **Phase 04 — Job Data Model & Clean Data Flow**: COMPLETE
- **Phase 05 — CSV Export**: COMPLETE

## Project Roadmap
- [x] **Phase 01 — Project Setup & Web Fundamentals** (COMPLETE)
- [x] **Phase 02 — Fetch Webpage** (COMPLETE)
- [x] **Phase 03 — Parse HTML** (COMPLETE)
- [x] **Phase 04 — Job Data Model** (COMPLETE)
- [x] **Phase 05 — CSV Export** (COMPLETE)
- [ ] **Phase 06 — Refactoring & Error Handling**
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

`main.py` coordinates this pipeline end-to-end.

---

## CSV Export Concepts (Phase 05)

### What is CSV?
CSV (Comma-Separated Values) is a plain-text file format for storing tabular data. Each line in a CSV file corresponds to a data record/row, and each record contains one or more fields separated by commas.

### Why CSV is Useful for Scraped Data
- **Portability**: Plain-text format compatible with spreadsheet software (Excel, Google Sheets) and data tools (Pandas, SQL databases).
- **Simplicity**: Does not require external server software, binary codecs, or relational database setup.
- **Human-Readable**: Easy to inspect, verify, and version control.

### How Python's `csv` Module Works
Python's standard library `csv` module provides `csv.writer` and `csv.DictWriter` to serialize collections of objects into RFC 4180-compliant CSV lines. It automatically handles:
- Quoting strings that contain commas, quotes, or newlines.
- Consistent UTF-8 encoding and newline handling across operating systems (`newline=""`).

### Role of `exporter.py`
`src/exporter.py` exposes `export_jobs(jobs, output_path)`:
1. Ensures the target destination directory exists (`mkdir(parents=True, exist_ok=True)`).
2. Opens the destination file safely with `utf-8` encoding.
3. Writes the header row (`title,company,location,url`).
4. Iterates over `Job` instances and writes row values mapped from object fields.
5. Handles empty job lists gracefully by producing a valid CSV containing only the headers.

---

## Data Modeling Concepts (Phase 04)

### What is a Data Model?
A data model defines the logical structure, fields, and types of data within an application. Instead of passing around untyped dictionaries or raw tuples, a data model establishes a formal contract for what attributes an entity contains.

### Why Use a Dataclass?
Python's built-in `@dataclass` decorator automatically generates boilerplate methods such as `__init__`, `__repr__`, and `__eq__` based on class field annotations. It ensures type clarity, immutability options, and IDE autocompletion without external dependencies.

### What `Job` Represents
The `Job` dataclass represents a single job posting extracted from the website with normalized fields:
- `title` (str): Title of the position
- `company` (str): Hiring organization
- `location` (str): Location of the role
- `url` (str): Full absolute link to job details / application

---

## Web & HTTP Concepts (Phase 02)

### What is HTTP?
HTTP (Hypertext Transfer Protocol) is the foundational protocol used for transmitting data across the World Wide Web. It operates on a client-server model where a client (e.g., a web browser or Python script) sends a request to a server, and the server returns a response containing data such as HTML, JSON, or media files.

### What is an HTTP GET Request?
An HTTP GET request is a method used to retrieve or "get" data from a specified resource on a web server. It does not modify server state and simply asks the server to send back the document located at the given URL.

### What is the `requests` Library?
`requests` is an HTTP library for Python designed to make sending HTTP/1.1 requests simple and human-friendly. It handles connection pooling, URL encoding, session management, SSL verification, and decoding response content automatically.

### What is an HTTP Status Code?
An HTTP status code is a three-digit integer returned by the server indicating the outcome of the request:
- **2xx (Success)**: e.g., `200 OK` — The request succeeded and data was returned.
- **3xx (Redirection)**: e.g., `301 Moved Permanently` — The resource is located elsewhere.
- **4xx (Client Error)**: e.g., `404 Not Found` — The requested page does not exist.
- **5xx (Server Error)**: e.g., `500 Internal Server Error` — The server encountered an issue while processing the request.

---

## HTML Parsing & Extraction Concepts (Phase 03)

### What is HTML Parsing?
HTML parsing is the process of taking a raw string of HTML text and converting it into a structured, navigable hierarchical tree structure (Document Object Model) in memory so individual elements, text nodes, and attributes can be queried and extracted programmatically.

### What is BeautifulSoup?
`BeautifulSoup` (`bs4`) is a Python parsing library that traverses and searches HTML and XML documents. It abstracts parser implementations (such as Python's standard `html.parser`) and provides intuitive methods (`find`, `find_all`, `select`) for navigating document trees.

### What is a CSS Selector?
A CSS selector is a pattern used to select elements within an HTML document based on tag names (`h2`), classes (`.title`), IDs (`#ResultsContainer`), or attributes (`[href]`).

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
