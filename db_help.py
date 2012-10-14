import pymongo

def initConnection(dbName):
#connect to a mongo database on the localhost
	from pymongo import Connection
	connection = Connection()
	db = connection[dbName]
	return db

def get_num_collection(db,collection_name = "posts",field = "name",key=None):
#get total count of collection for a given field and key
	if(key):
		return db[collection_name].find({field:key}).count()
	else:
		return db[collection_name].count()

				
