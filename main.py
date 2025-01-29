def print_resume():
    resume_text = """
    Joey [Last Name]
    [Your Phone Number] | [Your Email] | [Your LinkedIn Profile URL] | [Your GitHub Profile URL]

    **Summary**
    Highly motivated and detail-oriented Computer Science student graduating in Spring 2025, eager to apply a strong foundation in software development and a growing understanding of artificial intelligence to build innovative solutions. Possessing a diverse skillset including Java programming, full-stack web development, and database management, complemented by a passion for AI, data mining, and computer forensics. Seeking an entry-level role where I can contribute to meaningful projects while continuously expanding my technical expertise.

    **Education**
    - **[Your University Name]** - [City, State]
      - Bachelor of Science in Computer Science, Expected Graduation: Spring 2025
      - Relevant Coursework: Data Structures and Algorithms, Object-Oriented Programming, Database Systems, Computer Networks, Operating Systems, Artificial Intelligence, Machine Learning, Data Mining

    **Technical Skills**
    - **Programming Languages:** Java, Python (Currently Learning), JavaScript
    - **Web Development:** HTML, CSS, JavaScript, React, REST APIs
    - **Databases:** MySQL, PostgreSQL
    - **AI/ML Tools/Concepts:** TensorFlow, PyTorch, scikit-learn, Machine Learning Algorithms, Data Mining Techniques, Data Preprocessing
    - **Other:** Git, Linux, CLI, Computer Networks, Operating Systems

    **Projects**
    - **[Project Name 1]** - [Project Date]
      - **Description:** A brief but informative description of your project.
      - **Technologies:** List the technologies you used.
      - Example: Developed a sentiment analysis tool using Python and scikit-learn to classify text reviews. Achieved 85% accuracy on a test dataset.

    - **[Project Name 2]** - [Project Date]
      - **Description:** A brief but informative description of your project.
      - **Technologies:** List the technologies you used.
      - Example: Developed a personal website displaying personal projects and contact information using HTML, CSS, and JavaScript.

    **Relevant Experience** (If applicable)
    - **[Job Title]** - [Company Name], [City, State] | [Dates of Employment]
      - [Brief description of responsibilities and achievements]

    **Awards & Recognition** (Optional)
    - [Award Name] - [Year]
      - [Brief description]

    **Activities & Interests** (Optional)
    - [List extracurricular activities or interests]
    """
    print(resume_text)


def print_job_description():
    print(f'job description: We are seeking a motivated Entry-Level AI Developer '
          f'to join our team and help build innovative A.I solutions. '
          f'In this role, you will work alongside more experienced developers '
          f'to develop, train, and deploy machine learning models, '
          f'as well as integrate AI into applications. '
          f'This is an excellent opportunity for recent graduates or aspiring AI engineers '
          f'looking to gain hands-on experience in a fast-growing field.')


def print_intro(name):
    print(f'{name}')

if __name__ == '__main__':
    print_intro('hello, my name is joseph and this is the starter code for project 1 in senor design')


print_job_description()

print_resume()