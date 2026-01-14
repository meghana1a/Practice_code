import pprint
from pymongo import MongoClient
client = MongoClient("mongodb+srv://priyanka:******@practice.lgxcjgh.mongodb.net/")
db = client["migration_system"]

tasklist = db["tasks"] # each task is an induvidual document
users = db["users"] # each user is an induvidual document
user_id = ""
# function to add tasks to the tasks collection 
def get_input_task (user_id):
    #global user_id
    task = input("Please enter a task: ")
    add_task(task, user_id)

# add's a user to the user collection 
def get_input_user ():
    
    username = input("Please enter user name: ")
    get_id()
    add_user(username, user_id)
    return user_id
    
    

#adds task to task collection (only called within get_input_task)
def add_task (task, user_id):
    insert = {
        "task" : task,
        "user_id" : user_id,
        "completed" : False,
    }
    db.tasks.insert_one(insert)

# adds users to user collection (only called within get_input_user)
def add_user (username, user_id):
    insert = {
        "username" : username,
        "user_id" : user_id,
        "completed_tasks" : 0,
        "incomplete_tasks" : 0,
    }
    db.users.insert_one(insert)
    

#function that goes through task list and retrives all the tasks for a specific user 
def find_user_tasks (user_id):
    #user_id = input("Please enter your user id: ")
    finduser = db.tasks.find({"user_id" : user_id })
    for i in finduser:
        print(i)


#function to mark a task complete or incomplete 
def update_task_status(user_id):
   # user_id = input("Please enter your user id: ")
    #find way to do this without entering user id twice
    find_user_tasks()
    task = input("What is the name of the task you'd like to update to show compleation: ")
    db.tasks.find_one_and_update({"user_id" : user_id , "task":task}, {"$set":{"completed" : True}})
    count_compleation(user_id)

# function that counts complete and incomplete tasks

#has error must fix
def count_compleation(user_id):
    count = 0
    total = 0
    finduser = db.tasks.find({"user_id" : user_id, "completed" : True })
    for i in finduser:
        count = count + 1 
    findusertotal = db.tasks.find({"user_id" : user_id })
    for k in findusertotal:
        total = total + 1
    incomplete = total - count
    db.users.find_one_and_update({"user_id": user_id},{"$set": {"completed_tasks" : count}})
    db.users.find_one_and_update({"user_id": user_id},{ "$set":{ "incomplete_tasks" : incomplete}})

    

# function to display user profile 
def display_profile(user_id):
    #global user_id
    #user_id = input("Please enter your user id: ")
    profile = db.users.find({"user_id":user_id})
    for i in profile:
        pprint.pprint(i)
   

# improvements 
#get user id function 
def get_id():
    global user_id
    user_id = input("Please enter your user id: ")
    return user_id



# Possible additions: Log in function, verify that user_id is unique

def menu():
    a = input("would you like to create an account enter yes or no: ")
    
    if a == "yes":
            get_input_user()
            
            
            
    else:
            display_profile(get_id())
            
            
    while True:
        a = input("What would you like to do A: add a task, B: update the status of a task, C: View your tasks, D: View your profile, or E: Exit program . Please enter the corresponding letter of what you'd like to do:  ")
        if a == "A":
            get_input_task(user_id)
        elif a == "B":
            update_task_status(user_id)
        elif a == "C":
            find_user_tasks(user_id)
        elif a == "D":
            display_profile(user_id)
        elif a == "E":
            break



menu()
