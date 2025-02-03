# Joseph Pignatone
# Senior Design Section 002
# Project / Sprint 1
# GitHub: joeyp96

# requirements to run:
# Python 3.11
# google-generativeai - pip install google-generativeai
# grpcio - pip install grpcio
# grpcio-tools - pip install grpcio-tools

# Required libraries:
# import os
# import google.generativeai as genai

# This comment serves to test pylint.

import os
import google.generativeai as genai

with open("secret.txt", "r") as api_file:
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


def create_resume(job_description: str, personal_description: str) -> str:
    prompt = f"""
    you are a professional resume creator. Create a sample resume in markdown format that will be designed for the
    skills and job description provided.

    Job Description:
    {job_description}

    Personal Description:
    {personal_description}

    Format the resume in a structured, professional way.
    """

    response = chat_session.send_message(prompt)
    return response.text


def save_resume(resume_output: str) -> None:
    file_name = "created_resume.txt"
    file_path = os.path.join(os.getcwd(), file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(resume_output)

    print(f"Resume saved to: {file_path}")


if __name__ == '__main__':
    # job description from .json file line 27 "Application Developer", "company": "Links Technology Solutions"

    user_job_description = """
Links Technology Solutions is looking for a Software Developer to join their team!

This role requires a strong foundation in .NET development with a focus on building
and maintaining robust applications within an Agile team environment.

Your Day-to-Day:
• Design, develop, test, and maintain multiple applications using Microsoft .NET 
  and related technologies
• Participate in daily standups
"""

    user_personal_description = """my name is joey, i'm set to graduate 
                                      in spring 2025 with a bachelors degree in computer science from bridgewater
                                      state university, bridgewater MA. my skills include: 
                                      java programming, full stack web development, experiences with databases, 
                                      knowledge in computer networks and operating systems, 
                                      and I’m currently learning about computer forensics, 
                                      data mining, and a deep understand of modern AI systems. 
                                      I have no hands on experience in the field 
                                      but I’m eager to make my way into the industry.
                                      Project 1: A full stack website with authentication for users to login.
                                      included html, bootstrap, javascript, and node. We stored user information
                                      into a database using postgres.
                                      Project 2: I built a database which stored all 151 original pokemon
                                      with their name and statistics about them. I then connected this to 
                                      a website as a front end to display all this information in a clear way.
                                      Project 3: I created a file transfer protocol program that involved a 
                                      client program and a server program that could connect to each other 
                                      and send files back and forth in java."""

    resume_text = create_resume(user_job_description, user_personal_description)

    save_resume(resume_text)

    print(resume_text)
