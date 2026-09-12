# Project Context

## Overview
Python web scraper that extracts, parses, models, deduplicates, filters, exports (CSV), and analyzes job listings from https://realpython.github.io/fake-jobs/. Clean, decoupled pipeline orchestrated by `main.py`.

## Completed Phases (all COMPLETE)
- Phase 01–08: project setup, fetch, parse, model, CSV export, logging/error handling, CLI, pandas/matplotlib analysis
- Phase 09.1: multi-page scraping (`scrape_pages`, `build_page_url`)
- Phase 09.2: filtering (`filter_jobs`) by keyword/location/company (case-insensitive, AND logic)
- Phase 09.3: deduplication (`deduplicate_jobs`) by job URL, order-preserving, applied before filtering
- Phase 09.4: configurable output (`--output` custom CSV path, `--json` optional JSON export via `export_jobs_json`, automatic parent-dir creation via pathlib)
- Phase 09.5: application logging (`setup_logging(level)` in main.py, module-level loggers everywhere, `-v/--verbose` -> DEBUG, `-q/--quiet` -> WARNING, default INFO)
- Phase 09.6: robustness & fault tolerance (retry with backoff in `fetch_page`, retryable = Timeout/ConnectionError/HTTP 5xx, `--timeout` and `--retries` CLI args, page-level skip after retries exhausted in `scrape_pages`, WARNING for empty job cards in `parse_jobs`)

There is NO current in-progress phase. Next work would be a new Phase (10).

## Architecture / Data Flow
```
main.py (argparse: --url --pages --keyword --location --company --output --analyze)
  -> src/scraper.py (scrape_pages -> fetch_page, fault-tolerant, DEFAULT_TIMEOUT=10.0)
  -> src/parser.py (parse_jobs: BeautifulSoup, whitespace normalization via _normalize_text)
  -> src/models.py (Job dataclass: title, company, location, url)
  -> src/dedup.py (deduplicate_jobs: URL-based, keeps first occurrence, preserves order)
  -> src/filter.py (filter_jobs: case-insensitive substring match on title/location/company)
  -> src/exporter.py (export_jobs -> data/jobs.csv)
  -> src/analyzer.py (load_jobs -> clean_data -> stats + data/plots/*.png)
```

## Key Files
- `main.py` — argparse CLI (`parse_args`), `setup_logging(level)`, `run_scraper`, `run_analysis`, `main` with centralized exception handling (exit code 1); verbosity flags `-v/--verbose` (DEBUG) and `-q/--quiet` (WARNING), default INFO
- `src/scraper.py` — `fetch_page` (retry w/ backoff, `DEFAULT_TIMEOUT=10.0`, `DEFAULT_RETRIES=2`, `RETRY_DELAY=0.5`, `_should_retry` = Timeout/ConnectionError/HTTP 5xx), `scrape_pages` (page-level skip on failure), `build_page_url`
- `src/parser.py` — `parse_jobs(html, base_url)`; handles empty HTML and missing cards gracefully
- `src/models.py` — `Job` dataclass
- `src/dedup.py` — `deduplicate_jobs(jobs)` (non-mutating, returns new list)
- `src/filter.py` — `filter_jobs(jobs, keyword, location, company)`
- `src/exporter.py` — `export_jobs(jobs, path)` (writes header row even for empty lists), `export_jobs_json(jobs, path)` (derives JSON path from `--output` suffix swap)
- `src/analyzer.py` — pandas/matplotlib; validates CSV existence/content/columns
- `data/jobs.csv` — current dataset; `data/plots/*.png` — charts (top_locations, top_companies, top_titles)

## Tests
- 81 tests across `tests/`: test_analyzer, test_cli, test_dedup, test_exporter, test_filter, test_models, test_parser, test_scraper
- Run: `source .venv/bin/activate && python -m pytest` (or `python -m unittest discover -s tests`)

## Commands
- Default scrape: `python main.py`
- Multi-page: `python main.py --pages 3`
- Robustness: `python main.py --timeout 15 --retries 3`
- Filters (AND): `python main.py --keyword python --location remote --company microsoft`
- Custom output: `python main.py --output data/x.csv`
- JSON export: `python main.py --json` (writes next to CSV; e.g. `data/x.json`)
- Analyze: `python main.py --analyze` (analyzes `--output` path's CSV; plots to `data/plots/`)

## Notes / Gotchas
- fake-jobs site ignores the `page` query param and returns the same 100 jobs per page, so multi-page runs rely on dedup (e.g. `--pages 2` -> 200 scraped -> 100 unique).
- Keep new features as small phases; update the README's "Current Development Phase" and "Project Roadmap" sections, pipeline diagram, and add unit tests for any new module.
- Filtering to zero matches is not an error; a header-only CSV is still written.