import pymongo
from typing import Any, List
from .conecction import db
from training_service.domain.ml_model.ml_model_repository import MlModelRepository
from training_service.domain.ml_model.ml_model import  MLModel

class MongoImplementation(MlModelRepository):

    COLLECTION_NAME = "models"
    def __init__(self) -> None:
        pass 

    def insert_ml_model(self, model_to_insert: MLModel) -> Any:
        try:
            db_collection = db.get_collection(self.COLLECTION_NAME)
            doc_inserted = db_collection.insert_one(model_to_insert.to_dict())

            return doc_inserted.inserted_id
        except pymongo.errors.WriteError as error:
            print("Error de escritura en mongo")
            raise error
        except Exception as error:
            raise error
        
    def get_ml_models(self, limit:int) ->List[MLModel]:
        db_collection = db.get_collection(self.COLLECTION_NAME)
        if limit == 0:
            records = db_collection.find().sort("accuracy", pymongo.DESCENDING)
        else:
            records = db_collection.find().sort("accuracy", pymongo.DESCENDING).limit(limit)
        
        ml_models = []
