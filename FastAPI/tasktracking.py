import os
from fastapi import FastAPI
from pymongo import MongoClient
client = MongoClient("mongodb+srv://priyanka:HelloWorld@practice.lgxcjgh.mongodb.net/")
db = client["task_system"]

tasks = db["tasks"]
users=db["users"]
user_id = ""
app = FastAPI()

# this one doesn't need to be an API because it'll only be called in the code not by any users
def return_user_id():
    return user_id


#@app.post("/{userid}/")
#def get_user(userid : str):
 #   user_id = userid
  #  return {"User id is" : user_id}

#make new users and tasks 
@app.post("/new_user/")
def make_new_user(user_id : str, username: str):
    insert = {
        "username": username,
        "user_id" : user_id,
        "completed": db.tasks.count_documents({"user_id":user_id,"complete":True}),
        "in_progress" : db.tasks.count_documents({"user_id":user_id,"in_progress":True}),
        "incomplete": db.tasks.count_documents({"user_id":user_id,"complete":False}),
    }
    db.users.insert_one(insert)
    return {"output" : "user made"}

@app.post("/new_task/")
def new_task(user_id: str, task:str ): 
    insert = {
        "task": task,
        "complete" : False,
        "in_progress" : False,
        "user_id": user_id
    }
    db.tasks.insert_one(insert)
    return {"output" : "task made"}


# /////////////////////////////////////////////////

# update and find tasks
@app.get("/get_tasks/")
def get_user_tasks(user_id:str):
    tasks = []
    findtasks = db.tasks.find({"user_id":user_id}, {"_id" : 0})
    for i in findtasks:
        tasks.append(i)
    return {"tasks" : tasks}

@app.get("/in_progress/")
def get_in_progess(user_id:str): 
    in_progress = []
    findtasks = db.tasks.find({"user_id":user_id, "in_progress":True},{"_id":0})
    for i in findtasks:
        in_progress.append(i)
    return {"in progress tasks": in_progress}

@app.put("/change_progress/")
def change_progress(user_id:str, change: str):
    get_user_tasks(user_id)
    #if (input("Would you like to A: Mark a task as complete or B: Mark a tasks as in progress: ") == "A"):
    #    db.tasks.find_one_and_update({"user_id":user_id, "task": to_change},{"$set":{"complete":True, "in_progress":False}})
    db.tasks.find_one_and_update({"user_id":user_id, "task":change},{"$set":{"in_progress":True}})
    return {"output" : "marked as in progress"}

@app.put("/change_completion/")
def change_completion(user_id:str, change:str):
    get_user_tasks(user_id)
    db.tasks.find_one_and_update({"user_id":user_id, "task": change},{"$set":{"complete":True, "in_progress":False}})
    return {"output" : "marked as completed"}


@app.delete("/delete_tasks/")
def delete_tasks(user_id:str):
    db.tasks.delete_many({"user_id":user_id, "complete":True})
    #print ("Completed tasks deleted")
    return {"output" : "tasks deleted"}
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////

#profile and accounts

#display users 

@app.get("/display_users/")
def display_users():
    a = []
    findusers = list(db.users.find({},{"_id":0}))
    for i in findusers:
        a.append(i)
    return {"users": findusers}


#display profile
@app.get("/display_profile/")
def display_profile(user_id:str):
    a = []
    finduser = list(db.users.find({"user_id":user_id}, {"_id":0}))
    for i in finduser:
        a.append(i)
    return {"profile" : finduser}

#delete user
@app.delete("/deactivate/")
def deactivate_user(user_id:str):
    db.tasks.delete_many({"user_id":user_id})
    db.users.find_one_and_delete({"user_is":user_id})
    return {"output" : "usere deleted"}
# log in
@app.get("/log_in/")
def log_in(user_id:str):
    display_profile(user_id)
    user_id = return_user_id
    return {"output" : "logged in"}
    



