Instructions on how to run the program:
- requirements to run:
- Python 3.11
- google-generativeai - pip install google-generativeai (included on github actions)
- grpcio - pip install grpcio
- grpcio-tools - pip install grpcio-tools

- Required libraries:
- import os
- import google.generativeai as genai
- 
- sprint 2 update!
- import unittest
- import sqlite3
- import json

- sprint 3 update!
- import PySimpleGUI as sg

# Sprint 3
To run the program on the sprint 3 update you may follow the same instructions as before with one small change to 
run and use the GUI. Once pysimpleGUI is imported into your IDE (prefereably pycharm), navigate to the 
user_interface file. From the frop down menu at the top of pycharm, select "from current file". At this point
you may run the file and utilize the GUI, you'll see all the jobs within the previously created database
and when you click on a job, more information about the job will be displayed in the window to the right side. 
Additionally, you may fill out the fields that prompt you for your personal information and store that information
into the jobs.db within a new table.

Autmated testing:
To run the automated tests, navigate to the test_code.py file and ensure that "from current file" is selected. from here just click "run" at the top of your screen and all the tests will pass. 

utilization of AI: 
I once again used AI to create fake information to test on one of my users stored within the database. I also used it to help me with creating some of the elements of my automated tests as I found this to be the most diffifuclt part of the program once again.  

# Sprint 2

To run the program:
To run this program on the sprint 2 update, you dont need to do anything new aside from importing the new libraries listed above.
once the new libraries are imported, you may click run from the main.py file and a few things will happen:
In addition to the previous functionality, the program will now take in job listings from two different .json files in different formats.
The two formats are then unified and joined to a single table and stored in an sqlite database for the user to view. 
Because there is not yet a GUI implemented, I reccomend using DB browser to open the database and run the query:
select * from jobs; to view the full database of job listings and their fields.

Automated testing:
Automated tests have now been added. While they run automatically on github, you may do so from your ide.
Navigate to the tests folder and open the test_code.py file. Then, run from the if __name__ function to
run both tests together. Upon execution, a test.db is created. This takes in information from a fake
job listing I generated in the same format as one of the .json files I was given for this project. 
This file is called test.json. Test 1 confirms my import_json_data proprley extracts data from these
file formats and test 2 confirms that my program properly stores this information afterwards. 
You may view the test.db file as well by opening it in DB browser and running select * from jobs;
you'll be met with one job listing with "junk" test data. 

Utilization of A.I:
I used A.I. for a few things on this project.
- determining the differences in the .json file formats. This helped me code accordingly to extract data from both files.
- Gave me the idea for dynamic database names which allow me to test multiple databases with ease. (jobs.db and test.db)
- determining the differences in handling the URLs from each .json file. This again, helped me code accordingly to get the data I wanted in my database.
- Generating fake information for my test.json file. 


# Sprint 1 
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
