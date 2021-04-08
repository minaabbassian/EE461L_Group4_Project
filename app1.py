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

#############################################

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
		return project_found["Name"] + ' ' + project_found["Description"] + ' ' + project_found["ID"]


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("login.html")

# login method prompting usernam and password
@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']

    if not name1:
        return render_template('login.html', info='Please Enter a Username')
    if not pwd:
        return render_template('login.html', info='Please Enter a password')

    valid = isUserInfoCorrect(name1, pwd)
    if(valid== 'Found'):
        return render_template('home.html', name= name1)

    elif(valid== 'Password'):
        return render_template('login.html', info='Invalid Password')
    else: 
        return render_template('login.html', info='Invalid Username')
    #DISPLAY ERROR MESSAGE

#registering a new user
@app.route('/form_signup',methods=['POST','GET'])
def signup():
    name1=request.form['username']
    pwd=request.form['password']

    if not name1:
        return render_template('login.html', info='Please Enter a Username')
    if not pwd:
        return render_template('login.html', info='Please Enter a password')


    if (isUsernameTaken(name1)):
        return render_template('login.html', info='Username Taken')
    else:
        addNewUserToCollection(name1, pwd)
        return render_template('home.html', name=name1)
    #ADD ERROR MESSAGE

#creating a new project
@app.route('/form_createproject', methods=['POST', 'GET'])
def create():
    projName = request.form['projectName']
    projId = request.form['projectID']
    desc = request.form['description']

    if not projName:
        return render_template('home.html', info='Please Enter a project Name')
    if not projId:
        return render_template('home.html', info='Please Enter a project Id')
    if not desc:
        return render_template('home.html', info='Please Enter a description')


    check = addNewProjectToCollection(projName, desc, projId)
    if(check== "taken"):
        return render_template('home.html', info="ProjectId taken")
    else:
       return render_template('inproject.html') 
       #Display Error Code


#signing into existing project
@app.route('/form_signintoproject', methods=['POST', 'GET'])
def signIn():
    projId = request.form['projectID']

    if not projId:
        return render_template('home.html', info='Please enter a Project Id')
    
    validate = getExistingProject(projId)
    if(validate== "no"):
        return render_template('home.html', info='ProjectId not found')
    else:
        return render_template('inproject.html', info=validate)
        #Display Error


if __name__ == '__main__':
    app.run() 
    
