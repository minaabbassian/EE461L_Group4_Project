#Python Code for accessing project information from MongoDB

#Cluster: FinalProjectGroup8
#Databases: HWinfo, logininfo, projectinfo

import pymongo
from pymongo import MongoClient 


#Connect to MongoDB
cluster = MongoClient("mongodb+srv://test:test@finalprojectgroup8.frm2z.mongodb.net/logininfo?retryWrites=true&w=majority")

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
		return "worked"
	else:
		return "taken"
		
#Function that gets info on an existing project by user entering an existing projectID: 
def getExistingProject(proj_id):
	# proj_id = input('ProjectID:')
	if (isProjectIDTaken(proj_id) == False):
		return "no"
	else:
		project_found = project_coll.find_one({"ID": proj_id})
		return project_found["Name"] + ' ' + project_found["Description"] + ' ' + project_found["ID"]
		
	
		
	
#addNewProjectToCollection(project_name, project_description, project_id)
getExistingProject()

#Close connection to the database
cluster.close()