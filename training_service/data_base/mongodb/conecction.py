from pymongo import MongoClient
from credentials import USER, PASSWORD

PROJECT_NAME='proyectofinal'
DATABASE_NAME = 'trained-models'

client = MongoClient(f'mongodb+srv://{USER}:{PASSWORD}@{PROJECT_NAME}.afvv5vl.mongodb.net/')
db = client.get_database(DATABASE_NAME)