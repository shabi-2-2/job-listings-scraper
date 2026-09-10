import unittest
from src.parser import Job, parse_jobs


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


class TestParser(unittest.TestCase):
    def test_parse_multiple_jobs(self):
        jobs = parse_jobs(SAMPLE_HTML)
        self.assertEqual(len(jobs), 2)

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

    def test_empty_html(self):
        jobs = parse_jobs("")
        self.assertEqual(jobs, [])


if __name__ == "__main__":
    unittest.main()
