import pprint
from pymongo import MongoClient
client = MongoClient("mongodb+srv://priyanka:HelloWorld@practice.lgxcjgh.mongodb.net/")
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
        "in progress": False,
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
    #user_id = input("Please enter your user id: ")
    finduser = db.tasks.find({"user_id" : user_id })
    for i in finduser:
        print(i)


#function to mark a task complete or incomplete 
def update_task_status(user_id):
   # user_id = input("Please enter your user id: ")
    #find way to do this without entering user id twice
    find_user_tasks(user_id)
    task = input("What is the name of the task you'd like to update: ")
    if (input("Would you like to A: Mark as completed or B: Mark as in_progress. Please type the corresponding letter: ") == "A"):
     db.tasks.find_one_and_update({"user_id" : user_id , "task":task}, {"$set":{"completed" : True}})
     count_compleation(user_id)
    else:
        db.tasks.find_one_and_update({"user_id" : user_id , "task":task}, {"$set":{"in progress" : True}})

def get_in_progress(user_id):
    finduser = db.tasks.find({"user_id" : user_id ,"in progress" : True})
    for i in finduser:
        print(i)
    

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



# Possible additions: Log in function, verify that user_id is unique



def menu():
    global user_id
    
            
    while True:
        a = input("What would you like to do A: add a task, B: update the status of a task, C: View your tasks, D: View your profile, E: Exit program, F: Create a new account or log in, G: log out, H: See in progress tasks, I: Deactivate Account, J: Delete Completed Tasks, K: See all users. Please enter the corresponding letter of what you'd like to do:  ")
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
        elif a == "F":
            account_creation()
        elif a == "G":
            user_id = 0
            print("")
        elif a == "H":
            get_in_progress(user_id)
        elif a == "I":
            deactivate(user_id)
        elif a == "J":
            delete_completed_tasks(user_id)
        elif a == "K":
            get_users()


        
        



menu()
