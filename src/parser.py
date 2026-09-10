from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.models import Job


def _normalize_text(text: str) -> str:
    return " ".join(text.split())


def parse_jobs(html: str, base_url: str = "") -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="card")
    jobs: list[Job] = []

    for card in cards:
        title_elem = card.find("h2", class_="title")
        company_elem = card.find("h3", class_="company")
        location_elem = card.find("p", class_="location")

        title = _normalize_text(title_elem.get_text()) if title_elem else ""
        company = _normalize_text(company_elem.get_text()) if company_elem else ""
        location = _normalize_text(location_elem.get_text()) if location_elem else ""

        link_elem = next(
            (a for a in card.find_all("a") if a.get_text(strip=True).lower() == "apply"),
            None,
        )
        if not link_elem:
            links = card.find_all("a")
            link_elem = links[-1] if links else None

        raw_url = link_elem.get("href", "").strip() if link_elem else ""
        url = urljoin(base_url, raw_url) if raw_url else ""

        jobs.append(
            Job(
                title=title,
                company=company,
                location=location,
                url=url,
            )
        )

    return jobs
