import pprint
import os
from pymongo import MongoClient
client = MongoClient(os.enviorment.mongo_uri)
db = client["migration_system"]

tasklist = db["tasks"] # each task is an induvidual document
users = db["users"] # each user is an induvidual document
user_id = ""
# function to add tasks to the tasks collection 
def get_input_task (user_id):   
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
        "in_progress": False,
    }
    db.tasks.insert_one(insert)
    db.users.find_one_and_update({"user_id": user_id}, {"$inc":{"incomplete_tasks" : 1}})

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
    finduser = db.tasks.find({"user_id" : user_id })
    for i in finduser:
        print(i)


#function to mark a task complete or incomplete 
def update_task_status(user_id):
    find_user_tasks(user_id)
    task = input("What is the name of the task you'd like to update: ")
    if (input("Would you like to A: Mark as completed or B: Mark as in_progress. Please type the corresponding letter: ") == "A"):
     db.tasks.find_one_and_update({"user_id" : user_id , "task":task}, {"$set":{"completed" : True}})
     count_compleation(user_id)
    else:
        db.tasks.find_one_and_update({"user_id" : user_id , "task":task}, {"$set":{"in progress" : True}})
    count_compleation(get_user_id)

def get_in_progress(user_id):
    finduser = db.tasks.find({"user_id" : user_id ,"in progress" : True})
    for i in finduser:
        print(i)
    


def count_compleation(user_id):
    count = db.tasks.count_documents({"user_id":user_id, "completed":True})
    total = db.tasks.count_documents({"user_id":user_id})
    incomplete = total - count
    db.users.find_one_and_update({"user_id": user_id},{"$set": {"completed_tasks" : count}})
    db.users.find_one_and_update({"user_id": user_id},{ "$set":{ "incomplete_tasks" : incomplete}})

    

# function to display user profile 
def display_profile(user_id):
    profile = db.users.find({"user_id":user_id})
    for i in profile:
        pprint.pprint(i)
   


#improvment: get user id function 
def get_id():
    global user_id
    user_id = input("Please enter your user id: ")
    return user_id


#improvement: account creation function
def account_creation():
    a = input("would you like to A: log in or B: Create an account. Please enter the corresponding letter:  ")
    
    if a == "B":
            get_input_user()
                   
    else:
            display_profile(get_id())

# removes the loged in users account from the database           
def deactivate (user_id):
    db.tasks.delete_many({"user_id":user_id})
    db.users.find_one_and_delete({"user_id":user_id})


# deletes the loged in users completed tasks
def delete_completed_tasks(user_id):
    db.tasks.delete_many({"user_id":user_id, "completed":True})
    print("Done")


# gets all users in database
def get_users():
    findusers = db.users.find({})
    for i in findusers:
        pprint.pprint(i)


def get_user_id():
    return user_id

# Possible additions: Log in function (done), verify that user_id is unique



def menu():
    
            
    while True:
        a = input("What would you like to do: \n A: add a task,\n B: update the status of a task,\n C: View your tasks,\n D: View your profile,\n E: Exit program,\n F: Create a new account or log in,\n G: log out,\n H: See in progress tasks,\n I: Deactivate Account,\n J: Delete Completed Tasks,\n K: See all users. \n Please enter the corresponding letter of what you'd like to do:  ")
        if a == "A":
            get_input_task(get_user_id)
        elif a == "B":
            update_task_status(get_user_id)
        elif a == "C":
            find_user_tasks(get_user_id)
        elif a == "D":
            display_profile(get_user_id)
        elif a == "E":
            break
        elif a == "F":
            account_creation()
        elif a == "G":
            user_id = ""
            print("")
        elif a == "H":
            get_in_progress(get_user_id)
        elif a == "I":
            deactivate(get_user_id)
        elif a == "J":
            delete_completed_tasks(get_user_id)
        elif a == "K":
            get_users()


        
        



menu()
print("")