import pymongo
from .conecction import db


class MongoImplementation:

    def __init__(self) -> None:
        pass

    def insert_collection(self, documents, collection_name):
        try: 
            db_collection = db.get_collection(collection_name)
            before_count = db_collection.count_documents({})
            db_collection.insert_many(documents)

            return db_collection.count_documents({}) - before_count
        
        except pymongo.errors.WriteError as error:
            print("Error de escritura en mongo")
            raise error
        except Exception as error:
            raise error