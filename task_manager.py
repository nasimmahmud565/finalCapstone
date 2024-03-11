# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def write_to_task_file(tasks):
    '''Writing to Task file'''

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")

    while new_username in username_password.keys():
        print("User Already Exists... Try New One")
        new_username = input("Re-Enter Username: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    '''Allow a user to add a new task to task.txt file
                Prompt a user for the following:
                 - A username of the person whom the task is assigned to,
                 - A title of a task,
                 - A description of the task and
                 - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        task_username = input("ReEnter the Name of person assigned to task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)

    write_to_task_file(task_list)

    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the
               format of Output 2 presented in the task pdf (i.e. includes spacing
               and labelling)
            '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the
               format of Output 2 presented in the task pdf (i.e. includes spacing
               and labelling)
            '''
    user_tasks = []
    all_tasks = []
    for t in task_list:
        if t['username'] == curr_user:
            user_tasks.append(t)
        else:
            all_tasks.append(t)
    if len(user_tasks) > 0:
        i = 1
        for t in user_tasks:
            disp_str = f"Task {i} : {t['title']}\n"
            disp_str += f"\tAssigned to:  {t['username']}\n"
            disp_str += f"\tDate Assigned: " \
                        f"{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\tDue Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\tTask Description: \n {t['description']}\n"
            print(disp_str)
            i+=1
        while True:
            #Get Input to edit the task or return to Main Mene
            task_num = int(input("Enter Task Number to Edit or -1 to return to Main Menu : "))
            if task_num == -1:
                break
            if len(user_tasks) >= task_num > 0:
                if not user_tasks[task_num - 1]['completed']:
                    edit_input = int(input("""Enter \n\t 1 to Mark the Task as Complete
    \n\t 2 to Edit the Task \n\t: """))
                    if edit_input == 1:
                        user_tasks[task_num-1]['completed'] = True
                    elif edit_input == 2:
                        edit_input2 = int(input("""Enter \n\t 1 to Change the User Assigned
\n\t 2 to Edit the Due Date \n\t: """))
                        if edit_input2 == 1:
                            new_username = input("Enter the New UserName: ")
                            while new_username not in username_password.keys():
                                print("User Not Exists... Try Again")
                                new_username = input("Re-Enter Username: ")
                            user_tasks[task_num - 1]['username'] = new_username
                        elif edit_input2 == 2:
                            while True:
                                try:
                                    task_due_date = input("Due date of task (YYYY-MM-DD): ")
                                    due_date_time = datetime.strptime(task_due_date,
                                                                      DATETIME_STRING_FORMAT)
                                    break

                                except ValueError:
                                    print(
                                        "Invalid datetime format. Please use the format specified")
                            user_tasks[task_num-1]['duedate'] = due_date_time
                        else:
                            print("Invalid Entry... Retry")
                    else:
                        print("Invalid Entry... Retry")
                else:
                    print("Task Already Completed , Can't Modify")
            else:
                print("Invalid Entry... Retry")
    else:
        print("You Have no Tasks Assigned......")
    for t in user_tasks:
        all_tasks.append(t)

    write_to_task_file(all_tasks)

def generate_reports():
    task_completed = 0
    task_overdue = 0
    user_stat = {}
    curr_time = datetime.now()
    for t in task_list:
        if t['completed'] == True :
            task_completed += 1
        else:
            if t['due_date'] < curr_time :
                task_overdue += 1

        if t['username'] not in user_stat:
            user_stat[t['username']] = {}
            user_stat[t['username']]['total_tasks'] = 0
            user_stat[t['username']]['overdue_tasks'] = 0
            user_stat[t['username']]['completed_tasks'] = 0

        user_stat[t['username']]['total_tasks'] += 1
        if t['completed']:
            user_stat[t['username']]['completed_tasks'] += 1
        else:
            if t['due_date'] < curr_time:
                user_stat[t['username']]['overdue_tasks'] += 1

    task_overview_str = f"""
******** TASKS MANAGER OVERVIEW ********

Total Number of Tasks That have been generated and tracked : {len(task_list)}
Total Number of Completed Tasks : {task_completed}
Total Number of Uncompleted Tasks : {len(task_list) - task_completed}
Total Number of Tasks that haven't been Completed and Overduew : {task_overdue}
Percentage of Tasks that are incomplete : {round(((len(task_list) - task_completed)/len(task_list))*100, 2)}
Percentage of Tasks that are Overdue :{round((task_overdue/len(task_list))*100, 2)} 

********************************************
"""
    user_overview_str = f"""
******** USERS OVERVIEW Who Were Assigned TASKS********

Total Number of Users Registered : {len(user_data)}
Total Number of Tasks That have been generated and tracked : {len(task_list)}
"""
    for user in user_stat :
        str = f"""
STAT for USER - {user}
Total Number of Tasks That have been assigned : {user_stat[user]['total_tasks']}
Percentage of the total number of tasks that have been assigned to that user : {round((user_stat[user]['total_tasks']/len(task_list))*100,2)}
Percentage of the tasks assigned to that user that have been completed : {round((user_stat[user]['completed_tasks']/len(task_list))*100,2)}
Percentage of the tasks assigned to that user that must still be completed :  {round(((user_stat[user]['total_tasks']-user_stat[user]['completed_tasks'])/user_stat[user]['total_tasks'])*100,2)}
Percentage of the tasks assigned to that user that must still be completed and Overdue:  {round(((user_stat[user]['overdue_tasks'])/user_stat[user]['total_tasks'])*100,2)}
"""
        user_overview_str += str

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(task_overview_str)
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(user_overview_str)


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    options_text = '''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: '''
    admin_options_text = '''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate Reports
ds - Display statistics
e - Exit
: '''
    menu = input(admin_options_text if curr_user == 'admin' else options_text).lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        #calling reg_user method which handles the add the new user
        reg_user()

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file'''
        add_task()


    elif menu == 'va':
        '''View all tasks to the user'''
        view_all()


    elif menu == 'vm':
        '''Display tasks releated to the current user'''
        view_mine()
                
    elif menu == 'gr' and curr_user == 'admin':
        '''Generate Reports for the Admin in txt files '''
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")