# Job Listings Scraper

## Objective
A Python-based web scraping application designed to extract, parse, model, and export job listing data from the Fake Jobs practice website.

## Target Website
- **URL**: https://realpython.github.io/fake-jobs/
- **Description**: A mock job board provided by Real Python for learning web scraping techniques.

## Planned Technology Stack
- **Language**: Python 3.10+
- **HTTP Client**: `requests` (Phase 02)
- **HTML Parsing**: `beautifulsoup4` (Phase 03)
- **Data Export & CLI**: Built-in `csv` module, standard library / `argparse`

## Current Development Phase
- **Active Phase**: `Phase 01 — Project Setup & Web Fundamentals`

## Project Roadmap
- [x] **Phase 01 — Project Setup & Web Fundamentals** (Current)
- [ ] **Phase 02 — Fetch Webpage**
- [ ] **Phase 03 — Parse HTML**
- [ ] **Phase 04 — Job Data Model**
- [ ] **Phase 05 — CSV Export**
- [ ] **Phase 06 — Refactoring & Error Handling**
- [ ] **Phase 07 — CLI**
- [ ] **Phase 08 — Data Analysis**
- [ ] **Phase 09 — Advanced Features**

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
Activate the pre-configured `.venv` environment:

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### 2. Verification
Run the entry point script to verify the environment:

```bash
python main.py
```
