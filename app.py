from gitlab import Gitlab, MAINTAINER_ACCESS
from functools import wraps
from os import getenv
from csv import reader
from datetime import datetime


# Decorator for creating the results log
def log( func ):
    @wraps( func )
    def wrapper( *args, **kwargs ):
        # Creates the log file
        logFile = open('log.txt','a')
        result = func(*args)
        # Log the result
        logFile.write(f'{datetime.now()} - {result} \n')
        # Close the file
        logFile.close()
        return result
    return wrapper


@log
def create_repo( student ):
    ''' This function creates a repo from a template for a specific student '''
    try:
        year = student[0]
        division = student[1]
        name = student[2].lower()
        token = student[3]

        # Establishes the connection and get the authenticated user
        gl = Gitlab('https://gitlab.com', private_token=token)
        gl.auth()
        
        #print(gl.users.list(search='td3')[0])
    
        # Creates the repo
        student_project = gl.projects.create({'name': f'td3-{year}-{division}-{name}'})
        # Push the template into the repo
        data = {
            'branch': 'master',
            'commit_message': 'TD3 Template',
            'actions': [
                {
                    'action': 'create',
                    'file_path': '1-Informes/README.md',
                    'content': open('template/1-Informes/README.md', encoding="utf-8").read(),
                },
                {
                    'action': 'create',
                    'file_path': '2-Software/README.md',
                    'content': open('template/2-Software/README.md', encoding="utf-8").read(),
                },
                {
                    'action': 'create',
                    'file_path': '3-Hardware/README.md',
                    'content': open('template/3-Hardware/README.md', encoding="utf-8").read(),
                },
                {
                    'action': 'create',
                    'file_path': '4-Anexos/README.md',
                    'content': open('template/4-Anexos/README.md', encoding="utf-8").read(),
                },
                {
                    'action': 'create',
                    'file_path': '5-Video/README.md',
                    'content': open('template/5-Video/README.md', encoding="utf-8").read(),
                }
            ]
        }
        student_project.commits.create(data)
            
        # Add teachers as members with admin rights
        student_project.members.create({'user_id': getenv("gl_id_me"), 'access_level':MAINTAINER_ACCESS})
        student_project.members.create({'user_id': getenv("gl_id_td3"), 'access_level':MAINTAINER_ACCESS})

        print(f'{name} OK')
        return f'{name} OK'

    except Exception as e:
        print(f'{name} ERROR: {e}')
        return f'{name} ERROR: {e}'



# Iterates over the students csv creating the repos
with open('students.csv', 'r') as file:
    content = reader(file)
    for index, row in enumerate(content):
        if index > 0:
            create_repo(row)
        else:
            pass
