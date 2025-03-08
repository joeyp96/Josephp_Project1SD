"""
test_code.py

This file contains automated tests for checking:
1. JSON data extraction from test.json.
2. Correct insertion of jobs into test.db.
3. Correct retrieval of full job details when a job is selected in the GUI.
4. Correct information is stored in jobs.db entered by user.
5. 200/ok is returned from gemini.
6. checks prompt contains user/job description.
7. checks for URL in job listing in multiple cases.
"""
import os
import sqlite3
import json
import unittest
from unittest.mock import patch, MagicMock

from json_database import create_database, import_json_data, create_user_profiles_table, get_job_url
from user_interface import get_job_info, save_user
from main import create_resume


TEST_DB = "test.db"
TEST_JSON_FILE = "test.json"
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

        # Delete only test users, leaving real users intact
        self.cursor.execute("DELETE FROM user_profiles WHERE name=?", ("John Doe",))
        self.conn.commit()

        # Clear any existing test data
        # self.cursor.execute("DELETE FROM user_profiles")
        # self.conn.commit()

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


# test 1 sprint 4
# testing that I get a 200/ok from AI when I query it
class TestResponse(unittest.TestCase):
    """A test to ensure a response is returned from Google AI"""
    def test_response(self):
        """
        This test verifies a response is returned
        from Google AI.
        """
        # Skip the test if the API key DNE.
        if not os.path.exists("secret.txt"):
            self.skipTest("secret.txt not found")

        job_desc = "Software Engineer at TechCorp."
        personal_desc = "Experienced developer with Python skills."

        # Call function that sends a query to google gemini.
        response_text = create_resume(job_desc, personal_desc)

        # check that there is a response from the AI.
        self.assertIsInstance(response_text, str, "No string found from LLM.")
        self.assertTrue(response_text.strip(), "Response is empty from LLM.")


# test 2 sprint 4
# test that prompt contains job info and personal info
class TestCreateResumePrompt(unittest.TestCase):
    """A test to ensure the auto created prompt contains job/personal info """
    @patch("main.chat_session.send_message")
    # I utilized AI to come up with the mock message / dummy response strategy
    # I did this to avoid refactoring code from sprint 1
    def test_prompt_contents(self, mock_send_message):
        """test the prompt using dummy data"""
        job_desc = "This is a test job description."
        personal_desc = "This is a test personal description."

        # Create a dummy response so create_resume runs without error.
        dummy_response = MagicMock()
        dummy_response.text = "dummy resume text"
        mock_send_message.return_value = dummy_response

        # Call create_resume to send the prompt.
        create_resume(job_desc, personal_desc)

        # Extract the automatically created prompt from the patched call.
        prompt = mock_send_message.call_args[0][0]

        # Verify that the prompt contains the job description.
        self.assertIn(job_desc, prompt, "Job description not found.")
        # Verify that the prompt contains the personal description.
        self.assertIn(personal_desc, prompt, "Personal description not found.")


# test 3 sprint 4
# tests for URLs in the job listings
class TestUrl(unittest.TestCase):
    """test cases for each URL situation"""
    def test_direct_url(self):
        """Test that get_job_url returns the URL when 'job_url' is present."""
        job = {"job_url": "https://example.com/job_001"}
        self.assertEqual(get_job_url(job), "https://example.com/job_001")

    def test_url_from_job_providers(self):
        """Test that get_job_url returns the URL from 'jobProviders' when 'job_url' is absent."""
        job = {"jobProviders": [{"url": "https://example.com/job_002"}]}
        self.assertEqual(get_job_url(job), "https://example.com/job_002")

    def test_no_url_found(self):
        """Test that get_job_url returns None when no URL is available."""
        job = {}
        self.assertIsNone(get_job_url(job))


# Run all tests when executing this file
if __name__ == "__main__":
    unittest.main()
