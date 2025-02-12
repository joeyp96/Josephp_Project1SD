"""
test_code.py

This file has automated tests for checking the job processing functionality
in json_database.py. It ensures correct JSON extraction and database insertion.
"""

import os
import unittest
import sqlite3
import json
from json_database import create_database, import_json_data

TEST_DB = "test.db"
TEST_JSON_FILE = "test.json"


class TestJobDatabase(unittest.TestCase):
    """Unit tests for verifying database creation and job insertion in test.db."""

    def setUp(self):
        """Set up a separate test database (test.db) before each test."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)  # Ensure an empty database each time

        self.conn = sqlite3.connect(TEST_DB)
        self.cursor = self.conn.cursor()

        # Create the table in test.db
        create_database(TEST_DB)

    def tearDown(self):
        """Close connection after each test."""
        self.conn.close()

    def test_import_json_data_insertion(self):
        """Test processing test.json and inserting into test.db."""
        print("\ntesting_import_json_data_insertion.")

        # Process test.json and insert into the test database
        import_json_data(TEST_JSON_FILE, "test_source", TEST_DB)

        # Verify that the one job was inserted
        self.cursor.execute("SELECT COUNT(*) FROM jobs")
        job_count = self.cursor.fetchone()[0]
        print(f"Job count in test.db: {job_count}")
        self.assertEqual(job_count, 1, "Incorrect number of jobs in test.db.")

    def test_json_data_extraction(self):
        """Tests that import_json_data correctly extracts data from test.json (the known file)."""
        print("\nRunning test_json_data_extraction.")

        # Confirm JSON file is correctly formatted
        with open(TEST_JSON_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                print(f"Loaded test.json successfully: {data}")
            except json.JSONDecodeError as e:
                self.fail(f"Invalid JSON format in test.json: {e}")

        # Run import_json_data
        extracted_jobs = import_json_data(TEST_JSON_FILE, "test_source", TEST_DB)

        # Verify at least one job was extracted
        self.assertEqual(len(extracted_jobs), 1, "No jobs extracted from file.")

        # Verify the extracted job data matches expected values
        # A.I. was used to generate "junk" data
        job = extracted_jobs[0]
        self.assertEqual(job["id"], "job_001")
        self.assertEqual(job["title"], "Software Engineer")
        self.assertEqual(job["company"], "TechCorp")
        self.assertEqual(job["location"], "Remote")
        self.assertEqual(job["job_url"], "https://test.com/job_001")


if __name__ == "__main__":
    unittest.main()
