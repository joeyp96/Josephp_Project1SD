"""User Interface file for displaying job listings and storing user profiles."""

import sqlite3
import PySimpleGUI as sg
from json_database import create_user_profiles_table
from main import generate_resume_and_cover_letter

DB_NAME = "jobs.db"


def get_jobs():
    """gets job listings from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def get_job_info(job_id):
    """gets job details from the database for a job ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id=?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job


def save_user(values):
    """Saves or updates the user's profile info in jobs.db."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ensure the user_profiles table exists
    create_user_profiles_table()

    cursor.execute('''
        INSERT OR REPLACE INTO user_profiles (name, email, phone, github_linkedin, projects, classes, other)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        values.get("-NAME-", ""), values.get("-EMAIL-", ""), values.get("-PHONE-", ""),
        values.get("-GITHUB-", ""), values.get("-PROJECTS-", ""), values.get("-CLASSES-", ""),
        values.get("-OTHER-", "")
    ))

    conn.commit()
    conn.close()

    if __name__ == "__main__":  # Only show the popup when running GUI
        sg.popup("User profile saved.", title="Success")


def get_user_profiles():
    """gets the list of saved user profiles from jobs.db."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM user_profiles")
    profiles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return profiles


def load_user_profile(selected_name):
    """gets a user's saved profile info when a profile is chosen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles WHERE name=?", (selected_name,))
    user = cursor.fetchone()
    conn.close()
    return user


# Convert job data for displaying in the GUI
job_headers = ["Title", "Company", "Location"]
job_data = get_jobs()
formatted_job_data = [[job[1], job[2], job[3]] for job in job_data]

# GUI theme
sg.theme("DarkBlue")


# pylint: disable=too-many-locals

def open_gui():
    """opens PySimpleGUI to display job listings and user profiles."""

    # Left side - Job List (Table with horizontal scrolling)
    job_list_column = [
        [sg.Text("Job Listings", font=("Helvetica", 14, "bold"))],
        [sg.Table(
            values=formatted_job_data,
            headings=job_headers,
            auto_size_columns=False,
            col_widths=[30, 20, 20],
            justification="left",
            num_rows=15,
            key="-JOB_TABLE-",
            enable_events=True,
            expand_x=True,
            expand_y=True,
            vertical_scroll_only=False  # Enables horizontal scrolling
        )]
    ]

    # Right side - Job Details (Displays job info)
    job_details_column = [
        [sg.Text("Job Details", font=("Helvetica", 14, "bold"))],
        [sg.Multiline("", size=(70, 12), key="-JOB_DETAILS-", disabled=True)]
    ]

    # User Information Entry
    user_info_column = [
        [sg.Text("User Information", font=("Helvetica", 14, "bold"))],
        [sg.Text("Select Saved Profile:"), sg.Combo(
            values=get_user_profiles(), key="-PROFILE_DROPDOWN-", enable_events=True, size=(35, 1)
        )],
        [sg.Text("Name:"), sg.Input(size=(40, 1), key="-NAME-")],
        [sg.Text("Email:"), sg.Input(size=(40, 1), key="-EMAIL-")],
        [sg.Text("Phone:"), sg.Input(size=(40, 1), key="-PHONE-")],
        [sg.Text("GitHub/LinkedIn:"), sg.Input(size=(40, 1), key="-GITHUB-")],
        [sg.Text("Projects:"), sg.Multiline(size=(40, 3), key="-PROJECTS-")],
        [sg.Text("Classes:"), sg.Multiline(size=(40, 3), key="-CLASSES-")],
        [sg.Text("Other:"), sg.Multiline(size=(40, 3), key="-OTHER-")],
        [sg.Button("Save User Info", size=(15, 1)),
         sg.Button("Generate Resume", key="-GENERATE_RESUME-", size=(20, 1)),
         sg.Button("Generate Cover Letter", key="-GENERATE_COVER_LETTER-", size=(20, 1)),
         sg.Button("Exit", size=(10, 1))]
    ]

    # Full Layout
    layout = [
        [sg.Column(job_list_column), sg.VSeparator(), sg.Column(job_details_column)],
        [sg.HSeparator()],
        [sg.Column(user_info_column)]
    ]

    # Create the Window
    window = sg.Window("Job Listings & User Info", layout, resizable=True)

    # Event Loop
    while True:
        event, values = window.read()

        if event in {sg.WINDOW_CLOSED, "Exit"}:
            break

        if event == "Save User Info":
            save_user(values)
            window["-PROFILE_DROPDOWN-"].update(values=get_user_profiles())

        if event == "-PROFILE_DROPDOWN-" and values["-PROFILE_DROPDOWN-"]:
            selected_profile = values["-PROFILE_DROPDOWN-"]
            user_info = load_user_profile(selected_profile)

            if user_info:
                window["-NAME-"].update(user_info[1] if user_info[1] else "")
                window["-EMAIL-"].update(user_info[2] if user_info[2] else "")
                window["-PHONE-"].update(user_info[3] if user_info[3] else "")
                window["-GITHUB-"].update(user_info[4] if user_info[4] else "")
                window["-PROJECTS-"].update(user_info[5] if user_info[5] else "")
                window["-CLASSES-"].update(user_info[6] if user_info[6] else "")
                window["-OTHER-"].update(user_info[7] if user_info[7] else "")

        # Fill in Job Details when a job is selected
        if event == "-JOB_TABLE-":
            if values["-JOB_TABLE-"]:
                selected_index = values["-JOB_TABLE-"][0]
                job_id = job_data[selected_index][0]
                job_details = get_job_info(job_id)
                if job_details:
                    details_text = (
                        f"ID: {job_details[0]}\n"
                        f"Title: {job_details[1]}\n"
                        f"Company: {job_details[2]}\n"
                        f"Location: {job_details[3]}\n\n"
                        f"Description:\n{job_details[10]}"
                    )
                    window["-JOB_DETAILS-"].update(details_text)
                else:
                    window["-JOB_DETAILS-"].update("Job details not found.")

        if event in ("-GENERATE_RESUME-", "-GENERATE_COVER_LETTER-"):
            selected_user = values["-PROFILE_DROPDOWN-"]
            if not selected_user:
                sg.popup("Please select a user.", title="Error")
                continue

            user_data = load_user_profile(selected_user)
            selected_job = values["-JOB_TABLE-"]
            if not selected_job:
                sg.popup("Please select a job.", title="Error")
                continue

            job_details = get_job_info(job_data[selected_job[0]][0])

            pdf_path = generate_resume_and_cover_letter(user_data, {
                "title": job_details[1],
                "company": job_details[2],
                "location": job_details[3],
                "description": job_details[10]
            }, "resume" if event == "-GENERATE_RESUME-" else "cover_letter")

            sg.popup(f"PDF generated: {pdf_path}", title="Success")

    # Close the window
    window.close()


if __name__ == "__main__":
    open_gui()
