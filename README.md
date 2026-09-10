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
- **Data Export & CLI**: Built-in `csv` module, standard library / `argparse`

## Current Development Phase
- **Phase 01 — Project Setup & Web Fundamentals**: COMPLETE
- **Phase 02 — Fetch Webpage**: COMPLETE

## Project Roadmap
- [x] **Phase 01 — Project Setup & Web Fundamentals** (COMPLETE)
- [x] **Phase 02 — Fetch Webpage** (COMPLETE)
- [ ] **Phase 03 — Parse HTML**
- [ ] **Phase 04 — Job Data Model**
- [ ] **Phase 05 — CSV Export**
- [ ] **Phase 06 — Refactoring & Error Handling**
- [ ] **Phase 07 — CLI**
- [ ] **Phase 08 — Data Analysis**
- [ ] **Phase 09 — Advanced Features**

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

### Why Are Request Timeouts Important?
Without a timeout specified, network requests can hang indefinitely if the server is unreachable or fails to respond, causing the scraper to freeze. Setting a reasonable timeout (e.g., 10 seconds) guarantees that the program fails cleanly and predictably when connection problems arise.

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

### 4. Useful CSS Selectors & Attributes for Scraping
- `id="ResultsContainer"`: Locate the main grid of job cards.
- `div.card` / `div.card-content`: Select all individual job listing blocks.
- `h2.title`: Extract the job title text.
- `h3.company`: Extract the company name text.
- `p.location`: Extract location text.
- `time`: Extract publication date from text or `datetime` attribute.
- `footer.card-footer a`: Filter anchors where text is "Apply" or index `[1]` to extract `href`.

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
python -m unittest discover -s tests
```
