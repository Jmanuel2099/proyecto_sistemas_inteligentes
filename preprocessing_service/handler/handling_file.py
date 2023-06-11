import json
from preprocessing_service.domain.file import FileSingleton
from preprocessing_service.data_base.mongo.mongo_implementation import MongoImplementation
from preprocessing_service.models.request.missing_data_options import MissingDataOptions

class HandlingFile:
    DESCARD_METHOD = 1
    AVERAGE_IMPUTATION_METHOD = 2
    COLLECTION_TEST_NAME = 'data'
    COLLECTION_DISCARDING = 'data_missing_by_discarding'
    COLLECTION_AVERAGE_IMPUTATION = 'data_missing_by_average_imputation'

    def __init__(self) -> None:
        self.file = FileSingleton()
        self.respository = MongoImplementation()

    def get_file(self):
        return self.file

    def save_file(self, file):
        try:
            self.file.save_file(file)
            num_inserted_documents = self._load_data_in_respository(
                self.file.get_data_frame(),self.COLLECTION_TEST_NAME)
            return self.file.get_path(), num_inserted_documents
        except Exception as error:
            raise error

    def describe_file(self):
        try:
            if self.file.get_data_frame() is None:
                return None

            return self.file.describe_data()
        except Exception as error:
            raise error

    def process_missing_data(self, method):
        try:
            if self.file.get_data_frame() is None:
                return None
            
            if method is MissingDataOptions.descard:
                self.file.missing_data_by_discard()
                num_inserted_documents = self._load_data_in_respository(self.file.get_df_not_missing_data(),
                                            self.COLLECTION_DISCARDING)
            if method is MissingDataOptions.avergae_imputation:
                self.file.missing_data_by_imputation()
                num_inserted_documents = self._load_data_in_respository(self.file.get_df_not_missing_data(),
                                            self.COLLECTION_AVERAGE_IMPUTATION)
            
            return self.file.get_path(), num_inserted_documents
        except Exception as error:
            raise error

    def _load_data_in_respository(self, data_frame, collection):
        try:
            data_to_insert = data_frame.to_json(orient='records')
            return self.respository.insert_collection(json.loads(data_to_insert), collection)
        except Exception as error: 
            raise error
