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

"""
program for creating resumes using Google Gemini AI.

This program reads a job description, personal description, and generates a resume using AI,
then saves the response to a file.
"""


import os
import google.generativeai as genai

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
    """Creates a resume using AI based on the provided job and personal descriptions."""

    prompt = f"""
    you are a professional resume creator. Create a sample resume in markdown format that will be designed for the
    skills and job description provided.

    Job Description:
    {job_desc}

    Personal Description:
    {personal_desc}

    Format the resume in a structured, professional way.
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


if __name__ == "__main__":
    JOB_DESCRIPTION = (
        "Links Technology Solutions is looking for a Software Developer to join their team! "
        "This role requires a strong foundation in .NET development with a focus on building and "
        "maintaining robust applications within an Agile team environment. "
        "Your Day-to-Day: "
        "• Design, develop, test, and maintain multiple applications using Microsoft .NET "
        "  and related technologies. "
        "• Participate in daily standups."
    )

    PERSONAL_DESCRIPTION = """\
    My name is Joey, and I'm set to graduate in Spring 2025 with a Bachelor's degree in Computer Science 
    from Bridgewater State University, Bridgewater, MA. My skills include Java programming, 
    full-stack web development, experience with databases, and knowledge of computer networks 
    and operating systems. I’m currently learning about computer forensics, data mining, and modern AI systems.

    I have no hands-on experience in the field but I’m eager to enter the industry and apply my skills. 
    In terms of projects, I developed a full-stack web authentication system using HTML, Bootstrap, 
    JavaScript, Node.js, and PostgresSQL to store user information.

    Additionally, I built a database containing all 151 original Pokémon, along with a front-end web 
    application to display their statistics clearly. Lastly, I created a file transfer protocol (FTP) 
    program in Java that enables a client and server to communicate and transfer files back and forth.

    I am passionate about technology and excited to take my first steps into the software engineering industry.
    """

    resume_text = create_resume(JOB_DESCRIPTION, PERSONAL_DESCRIPTION)
    save_resume(resume_text)
    print(resume_text)
