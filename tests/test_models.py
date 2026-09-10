import unittest
from src.models import Job


class TestModels(unittest.TestCase):
    def test_job_model_creation(self):
        job = Job(
            title="Software Engineer",
            company="Acme Corp",
            location="Remote",
            url="https://example.com/job/1",
        )
        self.assertEqual(job.title, "Software Engineer")
        self.assertEqual(job.company, "Acme Corp")
        self.assertEqual(job.location, "Remote")
        self.assertEqual(job.url, "https://example.com/job/1")

    def test_job_model_equality(self):
        job1 = Job("Dev", "Corp", "NY", "https://example.com")
        job2 = Job("Dev", "Corp", "NY", "https://example.com")
        self.assertEqual(job1, job2)


if __name__ == "__main__":
    unittest.main()
