import unittest
from src.models import Job
from src.parser import parse_jobs

SAMPLE_HTML = """
<div id="ResultsContainer">
    <div class="card">
        <div class="card-content">
            <h2 class="title is-5">Python Developer</h2>
            <h3 class="subtitle is-6 company">Tech Corp</h3>
            <div class="content">
                <p class="location">Remote, US</p>
            </div>
            <footer class="card-footer">
                <a class="card-footer-item" href="https://example.com/learn">Learn</a>
                <a class="card-footer-item" href="https://example.com/jobs/1">Apply</a>
            </footer>
        </div>
    </div>
    <div class="card">
        <div class="card-content">
            <h2 class="title is-5">Data Engineer</h2>
            <h3 class="subtitle is-6 company">Data LLC</h3>
            <div class="content">
                <p class="location">Austin, TX</p>
            </div>
            <footer class="card-footer">
                <a class="card-footer-item" href="https://example.com/jobs/2">Apply</a>
            </footer>
        </div>
    </div>
</div>
"""

WHITESPACE_HTML = """
<div class="card">
    <div class="card-content">
        <h2 class="title">
            Senior
            Python   Developer
        </h2>
        <h3 class="company">
            \t Tech   Corp \n
        </h3>
        <p class="location">
            \n   Remote,   US   \n
        </p>
        <footer class="card-footer">
            <a href="https://example.com/jobs/1">Apply</a>
        </footer>
    </div>
</div>
"""

RELATIVE_URL_HTML = """
<div class="card">
    <div class="card-content">
        <h2 class="title">Backend Engineer</h2>
        <h3 class="company">Startup Inc</h3>
        <p class="location">San Francisco, CA</p>
        <footer class="card-footer">
            <a href="jobs/backend-dev-0.html">Apply</a>
        </footer>
    </div>
</div>
"""

MISSING_FIELDS_HTML = """
<div class="card">
    <div class="card-content">
        <p>No header or company here</p>
    </div>
</div>
"""

MALFORMED_HTML = """
<html><body><div><<<not valid html>>></div><div class="card"></div></body></html>
"""


class TestParser(unittest.TestCase):
    def test_parse_jobs_returns_list_of_job_instances(self):
        jobs = parse_jobs(SAMPLE_HTML)
        self.assertIsInstance(jobs, list)
        self.assertEqual(len(jobs), 2)
        for job in jobs:
            self.assertIsInstance(job, Job)
            self.assertTrue(hasattr(job, "title"))
            self.assertTrue(hasattr(job, "company"))
            self.assertTrue(hasattr(job, "location"))
            self.assertTrue(hasattr(job, "url"))

    def test_job_fields_extraction(self):
        jobs = parse_jobs(SAMPLE_HTML)
        job = jobs[0]
        self.assertEqual(
            job,
            Job(
                title="Python Developer",
                company="Tech Corp",
                location="Remote, US",
                url="https://example.com/jobs/1",
            ),
        )

    def test_text_normalization(self):
        jobs = parse_jobs(WHITESPACE_HTML)
        self.assertEqual(len(jobs), 1)
        job = jobs[0]
        self.assertEqual(job.title, "Senior Python Developer")
        self.assertEqual(job.company, "Tech Corp")
        self.assertEqual(job.location, "Remote, US")
        self.assertEqual(job.url, "https://example.com/jobs/1")

    def test_relative_url_resolution(self):
        jobs = parse_jobs(
            RELATIVE_URL_HTML,
            base_url="https://realpython.github.io/fake-jobs/",
        )
        self.assertEqual(len(jobs), 1)
        self.assertEqual(
            jobs[0].url,
            "https://realpython.github.io/fake-jobs/jobs/backend-dev-0.html",
        )

    def test_missing_fields_graceful_handling(self):
        jobs = parse_jobs(MISSING_FIELDS_HTML)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(
            jobs[0],
            Job(
                title="",
                company="",
                location="",
                url="",
            ),
        )

    def test_malformed_html_handling(self):
        jobs = parse_jobs(MALFORMED_HTML)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(
            jobs[0],
            Job(
                title="",
                company="",
                location="",
                url="",
            ),
        )

    def test_empty_html(self):
        jobs = parse_jobs("")
        self.assertEqual(jobs, [])


if __name__ == "__main__":
    unittest.main()
