# Joseph Pignatone
# Senior Design Section 002
# Project / Sprint 1
# GitHub: joeyp96

# Requirements to run:
# Python 3.11
# google-generativeai - pip install google-generativeai
# grpcio - pip install grpcio
# grpcio-tools - pip install grpcio-tools

# Required libraries:
# import os
# import google.generativeai as genai
# import unittest
# import sqlite3
# import json

"""
program for creating resumes using Google Gemini AI.

This program reads a job description, personal description, and generates a resume using AI,
then saves the response to a file.
"""

import os
import google.generativeai as genai
import markdown
from xhtml2pdf import pisa
from json_database import create_database, import_json_data

with open("secret.txt", "r", encoding="utf-8") as api_file:
    api_key = api_file.read().strip()

genai.configure(api_key=api_key)

# altered from python dictionary to resolve error
generation_config = genai.types.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])


def create_resume(job_desc: str, personal_desc: str) -> str:
    """Creates a resume using AI based on job and personal descriptions."""

    prompt = f"""
    You are a professional resume creator. Create a sample resume in markdown format that will be designed for the
    skills and job description provided.

    Job Description:
    {job_desc}

    Personal Description:
    {personal_desc}

    Format the resume in a structured, professional way.
    Do not include any additional information like suggestions. 
    """

    response = chat_session.send_message(prompt)
    return response.text


def save_resume(resume_output: str) -> None:
    """Saves the created resume to a file in the current working directory."""

    file_name = "created_resume.txt"
    file_path = os.path.join(os.getcwd(), file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(resume_output)

    print(f"Resume saved to: {file_path}")


# pylint: disable=too-many-locals

def generate_resume_and_cover_letter(user_data, job_data, doc_type):
    """
    Generates a resume or cover letter using Gemini AI and saves it as a PDF.
    :param user_data: Dictionary containing user information.
    :param job_data: Dictionary containing job details.
    :param doc_type: "resume" or "cover_letter" to specify document type.
    :return: File path to the generated PDF.
    """
    # Get user details
    name = user_data[1]
    email = user_data[2]
    phone = user_data[3]
    github_linkedin = user_data[4]
    projects = user_data[5]
    classes = user_data[6]
    other = user_data[7]

    # Get job details
    job_title = job_data.get("title", "[Insert Job Title]")
    company_name = job_data.get("company", "[Insert Company Name]")
    job_location = job_data.get("location", "[Insert Job Location]")
    job_description = job_data.get("description", "[Insert Job Description]")

    # AI prompt
    if doc_type == "resume":
        prompt = f"""
        You are an expert resume writer. Create a professional resume in Markdown format for the following individual:

        Name: {name}
        Email: {email}
        Phone: {phone}
        GitHub/LinkedIn: {github_linkedin}

        Applying for: {job_title} at {company_name}
        Location: {job_location}

        Job Description:
        {job_description}

        **Projects & Experience:**
        {projects}

        **Relevant Classes:**
        {classes}

        **Additional Information:**
        {other}

        Format the resume in a structured way.
        """
    elif doc_type == "cover_letter":
        prompt = f"""
        You are an expert cover letter writer. Create a professional cover letter in Markdown format for the following 
        individual:

        **{name}**
        {email}
        {phone}
        {github_linkedin}

        **{company_name}**
        {job_title}
        {job_location}

        Dear Hiring Manager,

        I am excited to apply for the {job_title} position at {company_name}.
        With my background in {classes},I am eager to bring my expertise to your team. 
        My experience includes:

        **Projects & Experience:**
        {projects}

        **Additional Information:**
        {other}

        I would love the opportunity to discuss how my skills can contribute to {company_name}.
        Thank you for your time and consideration.

        Best regards,  
        **{name}**
        """
    else:
        raise ValueError("Invalid document type. Use 'resume' or 'cover_letter'.")

    # Generate AI response
    response = chat_session.send_message(prompt)
    markdown_content = response.text.strip()

    # Convert markdown to HTML
    # I used this method due to macOS issues for pdf conversions
    html_content = markdown.markdown(markdown_content)

    # Define output PDF file path
    output_dir = "generated_pdfs"
    os.makedirs(output_dir, exist_ok=True)
    pdf_filename = os.path.join(output_dir, f"{name}_{doc_type}.pdf")

    # Convert HTML to PDF using xhtml2pdf
    with open(pdf_filename, 'wb') as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)

    return pdf_filename


if __name__ == "__main__":
    create_database()  # Check the database exists

    # import JSON files
    import_json_data("rapid_jobs2.json", "file1")
    import_json_data("rapidResults.json", "file2")

    print("Database update complete! No duplicate jobs inserted.")
