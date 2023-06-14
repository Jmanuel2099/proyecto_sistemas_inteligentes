import pymongo
from typing import Any, List, Union
from .conecction import db
from training_service.domain.ml_model.ml_model_repository import MlModelRepository
from training_service.domain.ml_model.ml_model import  MLModel

class MongoImplementation(MlModelRepository):
    COLLECTION_NAME = "models"

    def __init__(self) -> None:
        pass 

    def insert_ml_model(self, model_to_insert: MLModel) -> Any:
        try:
            print("model dict: ", model_to_insert.to_dict())
            db_collection = db.get_collection(self.COLLECTION_NAME)
            doc_inserted = db_collection.insert_one(model_to_insert.to_dict())

            return doc_inserted.inserted_id
        except pymongo.errors.WriteError as error:
            print("Error de escritura en mongo")
            raise error
        except Exception as error:
            raise error
        
    def get_all_ml_models(self) -> List[MLModel]:
        db_collection = db.get_collection(self.COLLECTION_NAME)
        records = db_collection.find().sort("accuracy", pymongo.DESCENDING)
        if not records: 
            return None
        ml_models = []
        for record in records:
            ml_model = MLModel(model_type=record["model_type"],
                               normalization_type=record["normalization_type"],
                               overfitting_underfitting=record["overfitting_underfitting"],
                               target=record["target"],
                               all_features=record["all_features"],
                               features=record["features"],
                               accuracy=record["accuracy"],
                               recall=record["recall"],
                               precision=record["precision"],
                               f1=record["f1"],
                               trained_model_path= record["trained_model_path"],
                               dataset_file= record["dataset_file"])
            ml_models.append(ml_model)

        return ml_models
    
    def get_ml_models_by_filter(self, limit:int, features:Union[List[str], bool]) -> List[MLModel]:
        if isinstance(features, List):
            query = {'features': {'$in': features}, 'all_features': False}
        else:
            query = {'all_features': True}

        print("query: ", query)
        db_collection = db.get_collection(self.COLLECTION_NAME)
        records = db_collection.find(query).sort("accuracy", pymongo.DESCENDING).limit(limit)
        if not records: 
            return None
        ml_models = []
        for record in records:
            ml_model = MLModel(model_type=record["model_type"],
                               normalization_type=record["normalization_type"],
                               overfitting_underfitting=record["overfitting_underfitting"],
                               target=record["target"],
                               all_features=record["all_features"],
                               features=record["features"],
                               accuracy=record["accuracy"],
                               recall=record["recall"],
                               precision=record["precision"],
                               f1=record["f1"],
                               trained_model_path= record["trained_model_path"],
                               dataset_file= record["dataset_file"])
            ml_models.append(ml_model)

        return ml_models
