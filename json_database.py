"""
json_database.py

This file handles job listings to be stored in a SQLite database.
It creates a jobs database, inserts job fields, and processes job listings
from two JSON files.
"""

import sqlite3
import json

DB_NAME = "jobs.db"


# A.I. gave me the idea for dynamic database names.
# This helped when setting up my automated tests.
def create_database(db_name=DB_NAME):
    """Creates the specified database and jobs table if they don't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            employment_type TEXT,
            date_posted TEXT,
            salary_min REAL,
            salary_max REAL,
            salary_currency TEXT,
            is_remote BOOLEAN,
            job_description TEXT,
            job_url TEXT,
            source TEXT,
            email TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def insert_job(job, db_name=DB_NAME):
    """Inserts a job into the specified database, with no duplicates."""
    conn = sqlite3.connect(db_name)  # Use dynamic database name for testing
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR IGNORE INTO jobs (
            id, title, company, location, employment_type, date_posted, salary_min,
            salary_max, salary_currency, is_remote, job_description, job_url, source, email
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            job.get("id"),
            job.get("title"),
            job.get("company"),
            job.get("location"),
            job.get("employment_type"),
            job.get("date_posted"),
            job.get("salary_min"),
            job.get("salary_max"),
            job.get("salary_currency"),
            job.get("is_remote"),
            job.get("description"),
            job.get("job_url"),
            job.get("source"),
            job.get("email"),
        ),
    )
    conn.commit()
    conn.close()


def import_json_data(file_path, source, db_name=DB_NAME):
    """Reads job listings from a JSON file and inserts them into the specified database."""
    extracted_jobs = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                job_data = json.loads(line.strip())
                # A.I. was used to pinpoint the differences in the file formats
                # This helped me program accordingly
                if isinstance(job_data, list):  # List of jobs
                    for job in job_data:
                        transformed_job = unify_job_data(job, source)
                        extracted_jobs.append(transformed_job)
                        insert_job(
                            transformed_job, db_name
                        )  # Insert into the specified database

                elif isinstance(job_data, dict):  # Single job
                    transformed_job = unify_job_data(job_data, source)
                    extracted_jobs.append(transformed_job)
                    insert_job(
                        transformed_job, db_name
                    )  # Insert into the specified database

            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON line in {file_path}: {e}")

    return extracted_jobs  # Used only for testing


def unify_job_data(job, source):
    """Transforms job data into the unified schema to utilize one table."""
    return {
        "id": job.get("id"),
        "title": job.get("title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "employment_type": job.get("employmentType") or job.get("job_type"),
        "date_posted": job.get("datePosted") or job.get("date_posted"),
        "salary_min": job.get("min_amount"),
        "salary_max": job.get("max_amount"),
        "salary_currency": job.get("currency"),
        "is_remote": job.get("is_remote", False),
        "description": job.get("description"),
        "job_url": get_job_url(job),
        "source": source,
        "email": job.get("emails"),
    }


def get_job_url(job):
    """gets the job URL from different formats."""
    # A.I. was used to show me handling different URL formats
    if "job_url" in job:
        return job["job_url"]
    if (
            "jobProviders" in job
            and isinstance(job["jobProviders"], list)
            and len(job["jobProviders"]) > 0
    ):
        return job["jobProviders"][0].get("url")
    return None


def create_user_profiles_table():
    """Creates the user_profiles table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            email TEXT,
            phone TEXT,
            github_linkedin TEXT,
            projects TEXT,
            classes TEXT,
            other TEXT
        )
    ''')
    conn.commit()
    conn.close()
