from pymongo import MongoClient
from .mongo_credentials import PASSWORD, USER

PROJECT_NAME='proyectofinal'
DATABASE_NAME = 'micro-servicios'

client = MongoClient(f'mongodb+srv://{USER}:{PASSWORD}@{PROJECT_NAME}.afvv5vl.mongodb.net/')
db = client.get_database(DATABASE_NAME)