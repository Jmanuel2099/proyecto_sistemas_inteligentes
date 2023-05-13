import json
from proyecto_sistemas_inteligentes.mongodb import COLLECTION_AVERAGE_IMPUTATION, COLLECTION_DISCARDING, COLLECTION_TEST_NAME
from file_app.services.handling_file.file import File
from file_app.services.mongodb.insert_data import InsertData
from file_app.services.handling_file.statistical_analysis import StatisticalAnalysis


class FileController:

    def __init__(self) -> None:
        self.file = File()
        self.respository = InsertData()

    def load_file(self, file):
        self.file.save_file_in_local(file)
        self._load_data_in_respository(self.file.get_data_frame(), 
                                    COLLECTION_TEST_NAME )        

    def describe_file(self):
        self.file.describe_data()

    def process_missing_data(self, method):
        statisticalAnalysis = StatisticalAnalysis(self.file)
        if method == statisticalAnalysis.DESCARD_METHOD:
            statisticalAnalysis.discard()
            self._load_data_in_respository(self.file.get_df_not_missing_data(),
                                        COLLECTION_DISCARDING)
        if method == statisticalAnalysis.AVERAGE_IMPUTATION_METHOD:
            statisticalAnalysis.imputation()
            self._load_data_in_respository(self.file.get_df_not_missing_data(),
                                        COLLECTION_AVERAGE_IMPUTATION)

    def _load_data_in_respository(self, data_frame, collection):
        data_to_insert = data_frame.to_json(orient='records')
        self.respository.insert_collection(json.loads(data_to_insert), collection)
