import unittest
from src.dedup import deduplicate_jobs
from src.models import Job


def _job(title: str, company: str, location: str, url: str) -> Job:
    return Job(title=title, company=company, location=location, url=url)


class TestDeduplicateJobs(unittest.TestCase):
    def test_no_duplicates_returns_same_list(self):
        jobs = [
            _job("Dev A", "Corp 1", "NY", "https://example.com/1"),
            _job("Dev B", "Corp 2", "LA", "https://example.com/2"),
        ]
        result = deduplicate_jobs(jobs)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, jobs)

    def test_duplicate_urls_removed(self):
        jobs = [
            _job("Python Dev", "Corp 1", "NY", "https://example.com/1"),
            _job("Python Dev", "Corp 1", "NY", "https://example.com/1"),
        ]
        result = deduplicate_jobs(jobs)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].url, "https://example.com/1")

    def test_multiple_duplicates_same_url(self):
        jobs = [
            _job("Python Dev", "Corp 1", "NY", "https://example.com/1"),
            _job("Python Dev", "Corp 1", "NY", "https://example.com/1"),
            _job("Python Dev", "Corp 1", "NY", "https://example.com/1"),
        ]
        result = deduplicate_jobs(jobs)
        self.assertEqual(len(result), 1)

    def test_preserves_first_seen_order(self):
        jobs = [
            _job("A", "Corp", "NY", "https://example.com/1"),
            _job("B", "Corp", "NY", "https://example.com/2"),
            _job("A", "Corp", "NY", "https://example.com/1"),  # duplicate of 1st
            _job("C", "Corp", "NY", "https://example.com/3"),
            _job("B", "Corp", "NY", "https://example.com/2"),  # duplicate of 2nd
        ]
        result = deduplicate_jobs(jobs)
        self.assertEqual(len(result), 3)
        urls = [j.url for j in result]
        self.assertEqual(urls, [
            "https://example.com/1",
            "https://example.com/2",
            "https://example.com/3",
        ])

    def test_different_urls_same_title_kept(self):
        jobs = [
            _job("Python Dev", "Corp 1", "NY", "https://example.com/1"),
            _job("Python Dev", "Corp 2", "LA", "https://example.com/2"),
        ]
        result = deduplicate_jobs(jobs)
        self.assertEqual(len(result), 2)

    def test_different_urls_same_company_location_kept(self):
        jobs = [
            _job("Dev A", "Corp", "NY", "https://example.com/1"),
            _job("Dev B", "Corp", "NY", "https://example.com/2"),
        ]
        result = deduplicate_jobs(jobs)
        self.assertEqual(len(result), 2)

    def test_empty_list(self):
        result = deduplicate_jobs([])
        self.assertEqual(result, [])

    def test_deduplication_across_pages(self):
        # Simulate paginated scraping where same job appears on multiple pages
        page1 = [
            _job("Dev 1", "Corp 1", "NY", "https://example.com/1"),
            _job("Dev 2", "Corp 2", "LA", "https://example.com/2"),
            _job("Dev 3", "Corp 3", "SF", "https://example.com/3"),
        ]
        page2 = [
            _job("Dev 2", "Corp 2", "LA", "https://example.com/2"),  # duplicate
            _job("Dev 3", "Corp 3", "SF", "https://example.com/3"),  # duplicate
            _job("Dev 4", "Corp 4", "TX", "https://example.com/4"),
        ]
        all_jobs = page1 + page2
        result = deduplicate_jobs(all_jobs)
        self.assertEqual(len(result), 4)
        urls = [j.url for j in result]
        self.assertEqual(urls, [
            "https://example.com/1",
            "https://example.com/2",
            "https://example.com/3",
            "https://example.com/4",
        ])

    def test_deduplication_then_filtering(self):
        # Deduplicate first, then filter - should work together
        from src.filter import filter_jobs

        jobs = [
            _job("Python Dev", "Corp 1", "Remote", "https://example.com/1"),
            _job("Python Dev", "Corp 1", "Remote", "https://example.com/1"),  # dup
            _job("Java Dev", "Corp 2", "NY", "https://example.com/2"),
            _job("Python Dev", "Corp 3", "NY", "https://example.com/3"),
        ]
        unique = deduplicate_jobs(jobs)
        self.assertEqual(len(unique), 3)

        # Now filter
        filtered = filter_jobs(unique, keyword="python")
        self.assertEqual(len(filtered), 2)

    def test_original_jobs_not_modified(self):
        jobs = [
            _job("Python Dev", "Corp", "NY", "https://example.com/1"),
            _job("Python Dev", "Corp", "NY", "https://example.com/1"),
        ]
        original_urls = [j.url for j in jobs]
        deduplicate_jobs(jobs)
        # Original list should be unchanged
        self.assertEqual([j.url for j in jobs], original_urls)


if __name__ == "__main__":
    unittest.main()