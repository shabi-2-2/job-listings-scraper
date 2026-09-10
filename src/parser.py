from dataclasses import dataclass
from urllib.parse import urljoin
from bs4 import BeautifulSoup


@dataclass
class Job:
    title: str
    company: str
    location: str
    url: str


def parse_jobs(html: str, base_url: str = "") -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="card")
    jobs: list[Job] = []

    for card in cards:
        title_elem = card.find("h2", class_="title")
        company_elem = card.find("h3", class_="company")
        location_elem = card.find("p", class_="location")

        title = title_elem.get_text(strip=True) if title_elem else ""
        company = company_elem.get_text(strip=True) if company_elem else ""
        location = location_elem.get_text(strip=True) if location_elem else ""

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
