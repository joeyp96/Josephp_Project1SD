Instructions on how to run the program:
# requirements to run:
# Python 3.11
# google-generativeai - pip install google-generativeai
# grpcio - pip install grpcio
# grpcio-tools - pip install grpcio-tools

# Required libraries:
# import os
# import google.generativeai as genai

using my API key:
you must add the secret.txt file that i've emailed you to the project directory.
If there are issues downloading the file due to BSU restrictions, you must create one by: 
in pycharm, create a new file in the CWD and name it secret.txt. Then copy and paste the API key on to
line 1 with no spaces or extra characters. You DO NOT need to assign it a varible name like API_KEY =. 
just paste the key ive provided (via email) into the first line of secret.txt

To run the program: 
use pycharm and python 3.11. It may work on another IDE or python version, but use these to ensure stability.
Once the proper libraries and packages are imported/installed, (listed above) you may simply click "run" within pycharm. 
the code should execute without errors. It will overwrite the created_resume.txt file everytime. However, if no
changes are made to the prompt, the same resume will be created each time. 

Why I chose googles gemini AI:
I chose this AI because google has become a household name in the tech industry. I felt that there would be enhanced support
when debugging issues as well as a surplus of documentation for me to reference throughout the project. Lastly, i have no previous
experience working with google's AI and I thought this would be a great opportunity to explore it.

How changes in the prompt effected program output:
When i started this program initially, my prompts were to vague. This resulted in the AI not knowing exactly what I was looking for.
to enhance the response, I told the AI that they are an expert in creating resumes and I wanted it to genereate a resume based on the
job description and personal description I provided in markdown format. These changes immediately gave me the proper response that I 
was looking for. Upon reviewing the file my program created, I discovered that I hadn't given specific projects i've worked on 
for the AI to add to the resume in my personal description. I simply updated my personal description with three projects i've completed
in the past to resolve this issue. This resulted in my final prompt for the AI to work with. I purposely left out certain personal
information like my address, phone number, and social media accounts to ensure security and privacy as responses from these models may 
be used to train other AI models. 
