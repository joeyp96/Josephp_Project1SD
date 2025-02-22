"""
test_code.py

This file contains automated tests for checking:
1. JSON data extraction from test.json.
2. Correct insertion of jobs into test.db.
3. Correct retrieval of full job details when a job is selected in the GUI.
4. Correct information is stored in jobs.db entered by user.
"""

import os
import unittest
import sqlite3
import json
from json_database import create_database, import_json_data, create_user_profiles_table
from user_interface import get_job_info, save_user  # Import function from GUI module

TEST_DB = "test.db"
TEST_JSON_FILE = "../test.json"
DB_NAME = "jobs.db"  # Use the real jobs database for GUI testing


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
        print("\nRunning test_import_json_data_insertion...")

        # Process test.json and insert into the test database
        import_json_data(TEST_JSON_FILE, "test_source", TEST_DB)

        # Check that one job was inserted
        self.cursor.execute("SELECT COUNT(*) FROM jobs")
        job_count = self.cursor.fetchone()[0]
        print(f"Job count in test.db: {job_count}")
        self.assertEqual(job_count, 1, "Incorrect number of jobs in test.db.")

    def test_json_data_extraction(self):
        """Tests that import_json_data correctly extracts data from test.json."""
        print("\nRunning test_json_data_extraction...")

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
        job = extracted_jobs[0]
        self.assertEqual(job["id"], "job_001")
        self.assertEqual(job["title"], "Software Engineer")
        self.assertEqual(job["company"], "TechCorp")
        self.assertEqual(job["location"], "Remote")
        self.assertEqual(job["job_url"], "https://test.com/job_001")


class TestJobSelection(unittest.TestCase):
    """Unit test for checking job selection in the GUI returns full info."""

    def setUp(self):
        """checks that jobs.db has at least one job before running the test."""
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

        # Check if there's at least one job in jobs.db
        self.cursor.execute("SELECT COUNT(*) FROM jobs")
        job_count = self.cursor.fetchone()[0]

        if job_count == 0:
            print("No jobs found in jobs.db. Adding a test job for testing purposes.")
            # Insert a test job if the database is empty
            self.cursor.execute('''
                INSERT INTO jobs (id, title, company, location, employment_type, date_posted, 
                                  salary_min, salary_max, salary_currency, is_remote, job_description, 
                                  job_url, source, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "job_001", "Software Engineer", "TechCorp", "Remote", "Full-time", "2024-01-15",
                80000, 120000, "USD", True, "Develop software applications.",
                "https://test.com/job_001", "test_source", "hr@techcorp.com"
            ))
            self.conn.commit()

    def tearDown(self):
        """Close the database connection after each test."""
        self.conn.close()

    def test_get_job_details_from_gui(self):
        """Test that selecting a job in the GUI returns the correct info."""
        print("\nRunning test_get_job_details_from_gui...")

        # pull a job from the database
        self.cursor.execute("SELECT id FROM jobs LIMIT 1")
        job = self.cursor.fetchone()

        # Ensure there is at least one job in the database
        self.assertIsNotNone(job, "No jobs found in jobs.db.")

        job_id = job[0]  # get job ID

        # Use GUI to get job details
        job_details = get_job_info(job_id)

        # Ensure job details are retrieved
        self.assertIsNotNone(job_details, "Job details should not be empty.")

        # Debugging print to check for errors
        print(f"Retrieved job details: {job_details}")

        # Check that important fields are correctly retrieved
        self.assertEqual(job_details[0], job_id)  # ID should match
        self.assertIsInstance(job_details[1], str)  # Title should be a string
        self.assertIsInstance(job_details[2], str)  # All other fields should be a string
        self.assertIsInstance(job_details[3], str)
        self.assertIsInstance(job_details[10], str)
        self.assertIsInstance(job_details[11], str)

        print("job selection test passed!")


class TestUserProfileStorage(unittest.TestCase):
    """Unit tests for checking user profile data is correctly stored in jobs.db."""

    def setUp(self):
        """Ensure the user_profiles table exists and clear existing user profiles before testing."""
        self.conn = sqlite3.connect(DB_NAME)  # Use jobs.db
        self.cursor = self.conn.cursor()

        # Call the function from json_database to create the table if it doesn't exist
        create_user_profiles_table()

        # Clear any existing test data before running tests
        self.cursor.execute("DELETE FROM user_profiles")
        self.conn.commit()

        # Clear any existing test data
        self.cursor.execute("DELETE FROM user_profiles")
        self.conn.commit()

        # Insert test user data (generated with AI)
        self.test_user = {
            "-NAME-": "John Doe",
            "-EMAIL-": "johndoe@example.com",
            "-PHONE-": "123-456-7890",
            "-GITHUB-": "https://github.com/johndoe",
            "-PROJECTS-": "Developed a Python automation tool.",
            "-CLASSES-": "CS101, CS102",
            "-OTHER-": "Open-source contributor."
        }
        save_user(self.test_user)  # Insert into jobs.db for testing

    def tearDown(self):
        """Close the database connection after each test."""
        self.conn.close()

    def test_user_basic_info(self):
        """Test that the name, email, phone, and GitHub/LinkedIn are stored correctly."""
        print("\nRunning test_user_basic_info...")

        self.cursor.execute(
            "SELECT name, email, phone, github_linkedin FROM user_profiles WHERE name=?",
            (self.test_user["-NAME-"],)
        )

        data = self.cursor.fetchone()

        self.assertIsNotNone(data, "User profile not found in jobs.db.")
        self.assertEqual(data[0], self.test_user["-NAME-"])
        self.assertEqual(data[1], self.test_user["-EMAIL-"])
        self.assertEqual(data[2], self.test_user["-PHONE-"])
        self.assertEqual(data[3], self.test_user["-GITHUB-"])

        print("Name, email, phone, and GitHub/LinkedIn stored correctly")

    def test_user_projects(self):
        """Test that projects are stored correctly."""
        print("\nRunning test_user_projects...")

        self.cursor.execute(
            "SELECT projects FROM user_profiles WHERE name=?",
            (self.test_user["-NAME-"],)
        )

        data = self.cursor.fetchone()

        self.assertIsNotNone(data, "Projects field not found in jobs.db.")
        self.assertEqual(data[0], self.test_user["-PROJECTS-"])

        print("Projects field stored correctly!")

    def test_user_classes(self):
        """Test that classes are stored correctly."""
        print("\nRunning test_user_classes...")

        self.cursor.execute(
            "SELECT classes FROM user_profiles WHERE name=?",
            (self.test_user["-NAME-"],)
        )

        data = self.cursor.fetchone()

        self.assertIsNotNone(data, "Classes field not found in jobs.db.")
        self.assertEqual(data[0], self.test_user["-CLASSES-"])

        print("Classes field stored correctly!")

    def test_user_other(self):
        """Test that the 'other' field is stored correctly."""
        print("\nRunning test_user_other...")

        self.cursor.execute(
            "SELECT other FROM user_profiles WHERE name=?",
            (self.test_user["-NAME-"],)
        )

        data = self.cursor.fetchone()

        self.assertIsNotNone(data, "Other field not found in jobs.db.")
        self.assertEqual(data[0], self.test_user["-OTHER-"])

        print("Other field stored correctly!")


# Run all tests when executing this file
if __name__ == "__main__":
    unittest.main()
