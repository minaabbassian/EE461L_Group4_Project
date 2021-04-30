from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

import pymongo
from pymongo import MongoClient 

#Connect to MongoDB
cluster = MongoClient("mongodb+srv://test:test@finalprojectgroup8.frm2z.mongodb.net/logininfo?retryWrites=true&w=majority")

##########################################################################

#CODE FOR LOGIN INFO 
#Database: logininfo
login_db = cluster["logininfo"]

#Collection: userinfo
user_coll = login_db["userinfo"]

#Function to add new user information to collection "userinfo"
def addNewUser(username, password):
	#Create a new document to insert into my collection 
	personDocument = {
		#add a new famous person to my collection with all the fields 
		"username": username,
		"password": password
	}
	#insert the document into my collection 
	user_coll.insert_one(personDocument)

#Function that returns TRUE if a username has already been taken by another user, otherwise returns FALSE 
def isUsernameTaken(username):
	if user_coll.find_one({"username": username}) == None:
		return False
	else:
		return True
		
#Function that returns TRUE if the username and password matches, otherwise returns FALSE
def isUserInfoCorrect(username, password):
    if(isUsernameTaken(username)==False):
        return 'Username'
    else:
        user = user_coll.find_one({"username": username})
        if(user["password"]== password):
            return 'Found'
        else: return 'Password'
	
			
#Function that adds new user to "user_coll" if username is not already taken 
def addNewUserToCollection(username, password):
	if(isUsernameTaken(username)== False):
		addNewUser(username, password)
	else:
		print("This username is already taken")

##########################################################################

#CODE FOR PROJECT INFO 
#Database: projectinfo
project_db = cluster["projectinfo"]
#Collection: projectID
project_coll = project_db["projectID"]

#Function to add new project information to collection "projectID"
def addNewProject(name, description, id):
	#Create a new document to insert into my collection 
	projectDocument = {
		#add a new project with fields for name, description, projectID, #HWSet1, #HWSet2 
		"Name": name,
		"Description": description,
		"ID": id,
		"HWSet1": 0,
		"HWSet2": 0
	}
	#insert the document into my collection 
	project_coll.insert_one(projectDocument)

#Function that returns TRUE if a projectID has already been used for another project, otherwise returns FALSE 
def isProjectIDTaken(project_id):
	if project_coll.find_one({"ID": project_id}) == None:
		return False
	else:
		return True
		
#Function that adds new project to "project_coll" if project_id has not already been used for another project
def addNewProjectToCollection(project_name, project_description, project_id):
    if (isProjectIDTaken(project_id)== True):
        return "taken"
    else:
        addNewProject(project_name, project_description, project_id)
        return "worked"

#Function that gets info on an existing project by user entering an existing projectID: 
def getExistingProject(proj_id):
	if (isProjectIDTaken(proj_id) == False):
	    return "no"
	else:
		project_found = project_coll.find_one({"ID": proj_id})
		return project_found["Name"]

##########################################################################

#CODE FOR HW INFO 
#Database: HWinfo
hw_db = cluster["HWinfo"]
#Collection: HWSets
hw_coll = hw_db["HWSets"]

#Function to add a HWSet to the collection, each start with 100 available
def addHWSet(name):
	#Create a new document to insert into my collection 
	hwDocument = {
		#add HWSet1 and HWSet2 info
		"Name": name,
		"Available": 100,
	}
	#insert the document into my collection 
	hw_coll.insert_one(hwDocument)

#Function that adds HWSet1 and HWSet2 to the collection
def addHWSet1and2():
	addHWSet("HWSet1")
	addHWSet("HWSet2")

#Function that handles checking out a HWSet
#Updates availablility of the HWSet while checking out 
def checkoutHWSet(number, name):
	hw_found = hw_coll.find_one({"Name": name})
	num_remaining = hw_found["Available"]
	if(number > num_remaining):
		return "invalid"
	else:
		updated_num = num_remaining - number
		hw_coll.update_one({"Name": name}, {"$set": {"Available": updated_num}})
		return "valid"
		
#Function that asks user to enter how many of HWSet1 they want to check out
def checkoutHWSet1(projectID, number):
    name = "HWSet1"
    project_found = project_coll.find_one({"ID": projectID})
    num_checkedout = project_found["HWSet1"]
    valid= checkoutHWSet(number, name)
    if(valid=="valid"):
        updated_num = num_checkedout + number
        project_coll.update_one({"ID": projectID}, {"$set": {"HWSet1": updated_num}})
        return "valid"
    else: return "invalid"
    
#Function that asks user to enter how many of HWSet2 they want to check out
def checkoutHWSet2(projectID, number):
    name = "HWSet2"
    project_found = project_coll.find_one({"ID": projectID})
    num_checkedout = project_found["HWSet2"]
    valid= checkoutHWSet(number, name)
    if(valid=="valid"):
        updated_num = num_checkedout + number
        project_coll.update_one({"ID": projectID}, {"$set": {"HWSet2": updated_num}})
        return "valid"
    else: return "invalid"

#Function that handles checking in a HWSet
#Updates availablility of the HWSet while checking in 
def checkinHWSet(number, name):
    hw_found = hw_coll.find_one({"Name": name})
    num_remaining = hw_found["Available"]
    updated_num=num_remaining+number
    hw_coll.update_one({"Name": name}, {"$set": {"Available": updated_num}})
    return "valid"

#Function that gets the number of remaining sets for HWSet1
def remainingHWSet1():
    name = "HWSet1"
    hw_found = hw_coll.find_one({"Name": name})
    num_remaining = hw_found["Available"]
    return (num_remaining)

#Function that gets the number of remaining sets for HWSet2
def remainingHWSet2():
    name = "HWSet2"
    hw_found = hw_coll.find_one({"Name": name})
    num_remaining = hw_found["Available"]
    return (num_remaining)

#Function that gets the number of HWSet1 checked out by a projectID
def getCheckedOutHWSet1(projID):
    proj_id = projID
    project_found = project_coll.find_one({"ID": proj_id})
    hw_checked_out = project_found["HWSet1"]
    if(hw_checked_out == 0):
        return("none")
    return (hw_checked_out)

#Function that gets the number of HWSet2 checked out by a projectID
def getCheckedOutHWSet2(projID):
    proj_id = projID
    project_found = project_coll.find_one({"ID": proj_id})
    hw_checked_out = project_found["HWSet2"]
    if(hw_checked_out == 0):
        return("none")
    return (hw_checked_out)

#Function that asks user to enter how many of HWSet1 they want to check in
def checkinHWSet1(projectID, number):
    name = "HWSet1"
    project_found = project_coll.find_one({"ID": projectID})
    num_checkedout = project_found["HWSet1"]
    if (number > num_checkedout):
        return "invalid"
    else:
        updated_num = num_checkedout - number
        project_coll.update_one({"ID": projectID}, {"$set": {"HWSet1": updated_num}})
        return (checkinHWSet(number, name))
	
#Function that asks user to enter how many of HWSet2 they want to check in
def checkinHWSet2(projectID, number):
    name = "HWSet2"
    project_found = project_coll.find_one({"ID": projectID})
    num_checkedout = project_found["HWSet2"]
    if (number > num_checkedout):
        return "invalid"
    else:
        updated_num = num_checkedout - number 
        project_coll.update_one({"ID": projectID}, {"$set": {"HWSet2": updated_num}})
        return (checkinHWSet(number, name))


##########################################################################

#CODE FOR CURRENT INFO 
#Database: currentinfo
curr_db = cluster["currentinfo"]
#Collection: currentsession
curr_coll = curr_db["currentsession"]

#changes the username to the person in session 
def changeSessionUsername(name):
    curr_coll.update_one({"Session": "first"}, {"$set": {"Username": name}})

def getSessionUsername():
    session_found = curr_coll.find_one({"Session": "first"})
    user = session_found["Username"]
    return (user)

#changes the ID to the PROJECTID in session 
def changeSessionID(id):
    curr_coll.update_one({"Session": "first"}, {"$set": {"ID": id}})

def getSessionID():
    session_found = curr_coll.find_one({"Session": "first"})
    proj_id = session_found["ID"]
    return (proj_id)

#changes the ProjectName to the Project Name in session 
def changeSessionProjectName(projName):
    curr_coll.update_one({"Session": "first"}, {"$set": {"ProjectName": projName}})

def getSessionProjectName():
    session_found = curr_coll.find_one({"Session": "first"})
    proj_name = session_found["ProjectName"]
    return (proj_name)
##########################################################################

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("login.html")

#login method prompting username and password
@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']

    valid = isUserInfoCorrect(name1, pwd)
    if(valid== 'Found'):
        changeSessionUsername(name1)
        return render_template('home.html', name= name1)

    elif(valid== 'Password'):
        #display error
        return render_template('login.html', info='Invalid Password')
    else: 
        #display error
        return render_template('login.html', info='Invalid Username')
    

#registering a new user
@app.route('/form_signup',methods=['POST','GET'])
def signup():
    name1=request.form['username']
    pwd=request.form['password']

    if (isUsernameTaken(name1)):
        #display error code
        return render_template('login.html', info2='Username Taken')
    else:
        addNewUserToCollection(name1, pwd)
        changeSessionUsername(name1)
        return render_template('home.html', name=name1)
    

#creating a new project
@app.route('/form_createproject', methods=['POST', 'GET'])
def create():
    projName = request.form['projectName']
    projId = request.form['projectID']
    desc = request.form['description']
    name1 = getSessionUsername()

    if (projName == ""):
        return render_template('home.html', info="Please enter a Project Name", name=name1)

    if (projId == ""):
        return render_template('home.html', info="Please enter a Project ID", name=name1)

    if (desc == ""):
        return render_template('home.html', info="Please enter a Project Description", name=name1)

    check = addNewProjectToCollection(projName, desc, projId)
    if(check== "taken"):
        #display error code
        return render_template('home.html', info="ProjectID taken", name=name1)
    else:
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        changeSessionID(projId)
        changeSessionProjectName(projName)
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        return render_template('inproject.html', name=projName, id=projId, hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2) 
     


#signing into existing project
@app.route('/form_signintoproject', methods=['POST', 'GET'])
def signIn():
    projId = request.form['projectID']
    name1 = getSessionUsername()
    validate = getExistingProject(projId)
    if(validate== "no"):
        #display error code
        return render_template('home.html', info2='ProjectID not found', name=name1)
    else:
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        changeSessionID(projId)
        changeSessionProjectName(validate)
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        return render_template('inproject.html', name=validate, id=projId, hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2) 
        


#logout of session
@app.route('/logout')
def logout():
    #session.clear()
    changeSessionUsername("")
    changeSessionProjectName("")
    changeSessionID("")
    return render_template('login.html')

#switch to project pages
@app.route('/switch')
def switch():
    name1 = getSessionUsername()
    return render_template('home.html', name=name1)

#go to downloads page
@app.route('/download')
def download():
    return render_template('downloads.html')

#go to downloads page
@app.route('/return1')
def return1():
    hw_set1 = remainingHWSet1()
    hw_set2 = remainingHWSet2()
    projId = getSessionID()
    checked_set1 = getCheckedOutHWSet1(projId)
    checked_set2 = getCheckedOutHWSet2(projId)
    projName = getSessionProjectName()
    return render_template('inproject.html', name=projName, id=projId, hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)

#check out HWSet1
@app.route('/form_checkout1', methods=['POST', 'GET'])
def checkOut1():
    projID = request.form['projID']
    if (projID == ""):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info='Please enter Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    elif (projID != getSessionID()):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info='Please enter the correct Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)

    while True:
        try:
            set1 = int(request.form['set1amount'])
            break
        except:
            hw_set1 = remainingHWSet1()
            hw_set2 = remainingHWSet2()
            projId = getSessionID()
            checked_set1 = getCheckedOutHWSet1(projId)
            checked_set2 = getCheckedOutHWSet2(projId)
            projName = getSessionProjectName()
            return render_template('inproject.html', name=projName, id=projId, info='Please enter a Valid Number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2) 
    #check for negative integers
    if (set1 < 0):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info='Please enter a valid number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    projID = request.form['projID']
    validity = checkoutHWSet1(projID, set1)
    hw_set1 = remainingHWSet1()
    hw_set2 = remainingHWSet2()
    projId = getSessionID()
    checked_set1 = getCheckedOutHWSet1(projId)
    checked_set2 = getCheckedOutHWSet2(projId)
    projName = getSessionProjectName()
    return render_template('inproject.html', name=projName, id=projId, validity=validity, hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2) 

#check out HWSet2
@app.route('/form_checkout2', methods=['POST', 'GET'])
def checkOut2():
    projID = request.form['projID']
    if (projID == ""):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info='Please enter Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    elif (projID != getSessionID()):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info='Please enter the correct Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    while True:
        try:
            set2 = int(request.form['set2amount'])
            break
        except:
            hw_set1 = remainingHWSet1()
            hw_set2 = remainingHWSet2()
            projId = getSessionID()
            checked_set1 = getCheckedOutHWSet1(projId)
            checked_set2 = getCheckedOutHWSet2(projId)
            projName = getSessionProjectName()
            return render_template('inproject.html', name=projName, id=projId, info='Please enter a valid number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    #check for negative integers
    if (set2 < 0):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info='Please enter a valid number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    projID = request.form['projID']
    validity = checkoutHWSet2(projID, set2)
    hw_set1 = remainingHWSet1()
    hw_set2 = remainingHWSet2()
    projId = getSessionID()
    checked_set1 = getCheckedOutHWSet1(projId)
    checked_set2 = getCheckedOutHWSet2(projId)
    projName = getSessionProjectName()
    return render_template('inproject.html', name=projName, validity=validity, id=projId, hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)


#check in 1
@app.route('/form_checkin1', methods=['POST', 'GET'])
def checkIn1():
    projID = request.form['projID']
    if (projID == ""):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info2='Please enter Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    elif (projID != getSessionID()):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info2='Please enter the correct Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    while True:
        try:
            set1 = int(request.form['set1amount'])
            break
        except:
            hw_set1 = remainingHWSet1()
            hw_set2 = remainingHWSet2()
            projId = getSessionID()
            checked_set1 = getCheckedOutHWSet1(projId)
            checked_set2 = getCheckedOutHWSet2(projId)
            projName = getSessionProjectName()
            return render_template('inproject.html', name=projName, id=projId, info2='Please enter a valid number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    #check for negative integers
    if (set1 < 0):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info2='Please enter a valid number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    projID = request.form['projID']
    validity2 = checkinHWSet1(projID, set1)
    hw_set1 = remainingHWSet1()
    hw_set2 = remainingHWSet2()
    projId = getSessionID()
    checked_set1 = getCheckedOutHWSet1(projId)
    checked_set2 = getCheckedOutHWSet2(projId)
    projName = getSessionProjectName()
    return render_template('inproject.html', name=projName, validity2=validity2, id=projId, hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)

#check in 2
@app.route('/form_checkin2', methods=['POST', 'GET'])
def checkIn2():
    projID = request.form['projID']
    if (projID == ""):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info2='Please enter Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    elif (projID != getSessionID()):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info2='Please enter the correct Project ID', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    while True:
        try:
            set2 = int(request.form['set2amount'])
            break
        except:
            hw_set1 = remainingHWSet1()
            hw_set2 = remainingHWSet2()
            projId = getSessionID()
            checked_set1 = getCheckedOutHWSet1(projId)
            checked_set2 = getCheckedOutHWSet2(projId)
            projName = getSessionProjectName()
            return render_template('inproject.html', name=projName, id=projId, info2='Please enter a valid number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    #check for negative integers
    if (set2 < 0):
        hw_set1 = remainingHWSet1()
        hw_set2 = remainingHWSet2()
        projId = getSessionID()
        checked_set1 = getCheckedOutHWSet1(projId)
        checked_set2 = getCheckedOutHWSet2(projId)
        projName = getSessionProjectName()
        return render_template('inproject.html', name=projName, id=projId, info2='Please enter a valid number', hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)
    projID = request.form['projID']
    validity2 = checkinHWSet2(projID, set2)
    hw_set1 = remainingHWSet1()
    hw_set2 = remainingHWSet2()
    projId = getSessionID()
    checked_set1 = getCheckedOutHWSet1(projId)
    checked_set2 = getCheckedOutHWSet2(projId)
    projName = getSessionProjectName()
    return render_template('inproject.html', name=projName, id=projId, validity2=validity2, hwset1=hw_set1, hwset2=hw_set2, checkedSet1=checked_set1, checkedSet2=checked_set2)   


if __name__ == '__main__':
    app.run() 
    