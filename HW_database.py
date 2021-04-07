#Python Code for accessing HWSet information from MongoDB

#Cluster: FinalProjectGroup8
#Databases: HWinfo, logininfo, projectinfo

import pymongo
from pymongo import MongoClient 


#Connect to MongoDB
cluster = MongoClient("mongodb+srv://test:test@finalprojectgroup8.frm2z.mongodb.net/logininfo?retryWrites=true&w=majority")

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
def checkoutHWSet1():
	name = "HWSet1"
	number = int(input('Number to HWSet1 to check out:'))
	checkoutHWSet(number, name)
	
#Function that asks user to enter how many of HWSet2 they want to check out
def checkoutHWSet2():
	name = "HWSet2"
	number = int(input('Number to check out:'))
	checkoutHWSet(number, name)
		

checkoutHWSet2()


#Close connection to the database
cluster.close()