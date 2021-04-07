#Python Code for connecting to MongoDB 

#Database: logininfo
#Collection: usernames

import pymongo
from pymongo import MongoClient 


#Connect to MongoDB
cluster = MongoClient("mongodb+srv://test:test@finalprojectgroup8.frm2z.mongodb.net/logininfo?retryWrites=true&w=majority")

#Database Name
db = cluster["logininfo"]

#Collection Name
collection = db["usernames"]


#Read the collection people from the database logininfo
doc = collection.find()

#Print the contents of the collection
for x in doc:
	print(x)
	
#Close connection to the database
cluster.close()