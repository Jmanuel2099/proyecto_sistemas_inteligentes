import json
from proyecto_sistemas_inteligentes.mongodb import COLLECTION_AVERAGE_IMPUTATION, COLLECTION_DISCARDING, COLLECTION_TEST_NAME
from file_app.application.handling_file.file import File
from file_app.application.mongodb.insert_data import InsertData
from file_app.application.handling_file.statistical_analysis import StatisticalAnalysis


class FileController:
    AVERAGE_IMPUTATION_METHOD = 1
    DESCARD_METHOD = 2

    def __init__(self) -> None:
        self.file = File()
        self.respository = InsertData()
        self.statisticalAnalysis = StatisticalAnalysis(self.file)

    def load_file(self, file):
        try:
            self.file.save_file_in_local(file)
            self._load_data_in_respository(self.file.get_data_frame(), 
                                        COLLECTION_TEST_NAME)
        except Exception as error:
            raise error

    def describe_file(self):
        try:
            if self.file.get_data_frame is None:
                return None

            return self.file.describe_data()
        except Exception as error:
            raise error

    def process_missing_data(self, method):
        try:
            if self.file.get_data_frame is None:
                return None
            # statisticalAnalysis = StatisticalAnalysis(self.file)
            if method == self.DESCARD_METHOD:
                self.file.missing_data_by_discard()
                self._load_data_in_respository(self.file.get_df_not_missing_data(),
                                            COLLECTION_DISCARDING)
            if method == self.AVERAGE_IMPUTATION_METHOD:
                self.file.missing_data_by_imputation()
                self._load_data_in_respository(self.file.get_df_not_missing_data(),
                                            COLLECTION_AVERAGE_IMPUTATION)
        except Exception as error:
            raise error
    def graphical_analysis(self):
        try:
            histograms = self.statisticalAnalysis.histograms()
            correlation_matrix = self.statisticalAnalysis.correlation_matrix()

            if histograms is None or correlation_matrix is None:
                return None
            return histograms, correlation_matrix

        except Exception as error:
            raise error


    def _load_data_in_respository(self, data_frame, collection):
        try:
            data_to_insert = data_frame.to_json(orient='records')
            self.respository.insert_collection(json.loads(data_to_insert), collection)
        except Exception as error: 
            raise error
