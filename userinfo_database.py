#Python Code for connecting to MongoDB 

#Cluster: FinalProjectGroup8
#Databases: HWinfo, logininfo, projectinfo

import pymongo
from pymongo import MongoClient 


#Connect to MongoDB
cluster = MongoClient("mongodb+srv://test:test@finalprojectgroup8.frm2z.mongodb.net/logininfo?retryWrites=true&w=majority")

#CODE FOR LOGIN INFO 
#Database: logininfo
login_db = cluster["logininfo"]

#Collection: userinfo
user_coll = login_db["userinfo"]

#Ask for user to enter username and password 
person_username = input('username:')
person_password = input('password:')


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
	user = user_coll.find_one({"username": username})
	if(user["password"] == password):
		return True
	return False
		
		
#Function that adds new user to "user_coll" if username is not already taken 
def addNewUserToCollection(username, password):
	if (isUsernameTaken(username) == False):
		addNewUser(username, password)
	else:
		print("This username is already taken")
		
	
addNewUserToCollection(person_username, person_password)

#Close connection to the database
cluster.close()