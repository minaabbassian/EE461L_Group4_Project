#Python Code for accessing HWSet information from MongoDB

#Cluster: FinalProjectGroup8
#Databases: HWinfo, logininfo, projectinfo

import pymongo
from pymongo import MongoClient 

#Connect to MongoDB
cluster = MongoClient("mongodb+srv://test:test@finalprojectgroup8.frm2z.mongodb.net/logininfo?retryWrites=true&w=majority")

########################################################

#CODE FOR PROJECT INFO 
#Database: projectinfo
project_db = cluster["projectinfo"]
#Collection: projectID
project_coll = project_db["projectID"]

#Ask for user to enter project name, project description, project ID 
def projectInput():
	project_name = input('Name:')
	project_description = input('Description:')
	project_id = input('ProjectID:')


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
	if (isProjectIDTaken(project_id) == False):
		addNewProject(project_name, project_description, project_id)
	else:
		print("This projectID has already been taken")
		
#Function that gets info on an existing project by user entering an existing projectID: 
def getExistingProject():
	proj_id = input('ProjectID:')
	if (isProjectIDTaken(proj_id) == False):
		print("This Project does not exist")
	else:
		project_found = project_coll.find_one({"ID": proj_id})
		print(project_found["Name"])
		print(project_found["Description"])
		print(project_found["ID"])#Ask for user to enter project name, project description, project ID 


#####################################################

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
		print("There are not enough remaining for you to check out")
	else:
		updated_num = num_remaining - number
		hw_coll.update_one({"Name": name}, {"$set": {"Available": updated_num}})
		print("You have successfully checked out", number, "of", name)
		
#Function that asks user to enter how many of HWSet1 they want to check out
def checkoutHWSet1(projectID):
	name = "HWSet1"
	number = int(input('Number of HWSet1 to check out:'))
	project_found = project_coll.find_one({"ID": projectID})
	num_checkedout = project_found["HWSet1"]
	updated_num = num_checkedout + number
	project_coll.update_one({"ID": projectID}, {"$set": {"HWSet1": updated_num}})
	checkoutHWSet(number, name)
	
#Function that asks user to enter how many of HWSet2 they want to check out
def checkoutHWSet2(projectID):
	name = "HWSet2"
	number = int(input('Number of HWSet2 to check out:'))
	project_found = project_coll.find_one({"ID": projectID})
	num_checkedout = project_found["HWSet2"]
	updated_num = num_checkedout + number
	project_coll.update_one({"ID": projectID}, {"$set": {"HWSet2": updated_num}})
	checkoutHWSet(number, name)
	
#Function that handles checking in a HWSet
#Updates availablility of the HWSet while checking in 
def checkinHWSet(number, name):
	hw_found = hw_coll.find_one({"Name": name})
	num_remaining = hw_found["Available"]
	updated_num = num_remaining + number
	hw_coll.update_one({"Name": name}, {"$set": {"Available": updated_num}})
	print("You have successfully checked in", number, "of", name)
		
#Function that asks user to enter how many of HWSet1 they want to check in
def checkinHWSet1(projectID):
	name = "HWSet1"
	project_found = project_coll.find_one({"ID": projectID})
	num_checkedout = project_found["HWSet1"]
	number = int(input('Number of HWSet1 to check in:'))
	if (number > num_checkedout):
		print("You cannot check out this many of HWSet1!")
	else:
		updated_num = num_checkedout - number 
		project_coll.update_one({"ID": projectID}, {"$set": {"HWSet1": updated_num}})
		checkinHWSet(number, name)
	
#Function that asks user to enter how many of HWSet2 they want to check in
def checkinHWSet2(projectID):
	name = "HWSet2"
	project_found = project_coll.find_one({"ID": projectID})
	num_checkedout = project_found["HWSet2"]
	number = int(input('Number of HWSet2 to check in:'))
	if (number > num_checkedout):
		print("You cannot check out this many of HWSet2!")
	else:
		updated_num = num_checkedout - number 
		project_coll.update_one({"ID": projectID}, {"$set": {"HWSet2": updated_num}})
		checkinHWSet(number, name)

checkoutHWSet2('123456')

#Close connection to the database
cluster.close()