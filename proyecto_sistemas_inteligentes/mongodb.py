from pymongo import MongoClient


COLLECTION_TEST_NAME = 'test'
DATABASE_NAME = 'micro-servicios'

client = MongoClient('mongodb+srv://Jose:Jose0920@proyectofinal.afvv5vl.mongodb.net/')
db = client.get_database(DATABASE_NAME)
db_collection_test = db.get_collection(COLLECTION_TEST_NAME)