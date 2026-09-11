import unittest
from src.filter import filter_jobs
from src.models import Job


SAMPLE_JOBS = [
    Job("Python Developer", "Tech Corp", "New York, NY", "https://example.com/1"),
    Job("Senior Python Engineer", "Python Inc", "Remote", "https://example.com/2"),
    Job("Data Scientist", "Data LLC", "Chicago, IL", "https://example.com/3"),
    Job("Backend Developer", "Tech Corp", "Remote", "https://example.com/4"),
    Job("Full Stack Engineer", "Web Co", "Austin, TX", "https://example.com/5"),
    Job("Junior Python Dev", "StartupXYZ", "New York, NY", "https://example.com/6"),
    Job("Software Engineer", "Big Tech", "Seattle, WA", "https://example.com/7"),
]


class TestFilterJobs(unittest.TestCase):
    def test_no_filters_returns_all(self):
        result = filter_jobs(SAMPLE_JOBS)
        self.assertEqual(len(result), len(SAMPLE_JOBS))

    def test_keyword_match(self):
        result = filter_jobs(SAMPLE_JOBS, keyword="python")
        self.assertEqual(len(result), 3)
        titles = [j.title for j in result]
        self.assertIn("Python Developer", titles)
        self.assertIn("Senior Python Engineer", titles)
        self.assertIn("Junior Python Dev", titles)

    def test_keyword_case_insensitive(self):
        result = filter_jobs(SAMPLE_JOBS, keyword="PYTHON")
        self.assertEqual(len(result), 3)

    def test_keyword_no_matches(self):
        result = filter_jobs(SAMPLE_JOBS, keyword="kubernetes")
        self.assertEqual(len(result), 0)

    def test_location_match(self):
        result = filter_jobs(SAMPLE_JOBS, location="remote")
        self.assertEqual(len(result), 2)
        titles = [j.title for j in result]
        self.assertIn("Senior Python Engineer", titles)
        self.assertIn("Backend Developer", titles)

    def test_location_case_insensitive(self):
        result = filter_jobs(SAMPLE_JOBS, location="REMOTE")
        self.assertEqual(len(result), 2)

    def test_location_no_matches(self):
        result = filter_jobs(SAMPLE_JOBS, location="Paris")
        self.assertEqual(len(result), 0)

    def test_company_match(self):
        result = filter_jobs(SAMPLE_JOBS, company="tech corp")
        self.assertEqual(len(result), 2)
        titles = [j.title for j in result]
        self.assertIn("Python Developer", titles)
        self.assertIn("Backend Developer", titles)

    def test_company_case_insensitive(self):
        result = filter_jobs(SAMPLE_JOBS, company="Tech Corp")
        self.assertEqual(len(result), 2)

    def test_company_no_matches(self):
        result = filter_jobs(SAMPLE_JOBS, company="Nonexistent")
        self.assertEqual(len(result), 0)

    def test_multiple_filters_and_logic(self):
        result = filter_jobs(SAMPLE_JOBS, keyword="python", location="remote")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Senior Python Engineer")

    def test_multiple_filters_no_match(self):
        result = filter_jobs(SAMPLE_JOBS, keyword="python", location="chicago")
        self.assertEqual(len(result), 0)

    def test_all_three_filters(self):
        result = filter_jobs(
            SAMPLE_JOBS, keyword="dev", location="new york", company="tech corp"
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Python Developer")

    def test_partial_keyword_in_title(self):
        result = filter_jobs(SAMPLE_JOBS, keyword="engineer")
        self.assertEqual(len(result), 3)
        titles = [j.title for j in result]
        self.assertIn("Senior Python Engineer", titles)
        self.assertIn("Full Stack Engineer", titles)
        self.assertIn("Software Engineer", titles)

    def test_empty_job_list(self):
        result = filter_jobs([], keyword="python")
        self.assertEqual(len(result), 0)

    def test_empty_job_list_no_filters(self):
        result = filter_jobs([])
        self.assertEqual(len(result), 0)
