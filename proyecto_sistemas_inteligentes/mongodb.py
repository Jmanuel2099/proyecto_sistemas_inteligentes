from pymongo import MongoClient
from proyecto_sistemas_inteligentes.environment import PASSWORD, USER

PROJECT_NAME='proyectofinal'
DATABASE_NAME = 'micro-servicios'
COLLECTION_TEST_NAME = 'test'

client = MongoClient(f'mongodb+srv://{USER}:{PASSWORD}@{PROJECT_NAME}.afvv5vl.mongodb.net/')
db = client.get_database(DATABASE_NAME)
db_collection_test = db.get_collection(COLLECTION_TEST_NAME)