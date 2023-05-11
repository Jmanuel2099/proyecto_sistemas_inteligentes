from django.core.files.storage import default_storage
from django.conf import settings
import os
import pandas as pd
from datetime import datetime
import json
from file_app.services.mongodb.insert_data import InsertData


class File:
    def __init__(self) -> None:
        self.data_frame = None

    def get_data_frame(self):
        return self.data_frame
    
    def set_data_frame(self, new_data_frame):
        self.data_frame = new_data_frame

    def describe_data(self):
        first_record_dict = self.data_frame.iloc[0].to_dict()
        return {key: type(value).__name__ for key, value in first_record_dict.items()}
    
    def load_file(self, file):
        file_name = self._save_file(file)

        file_path = os.path.join(settings.BASE_DIR, 'archivos\\' + file_name)
        self._create_data_famre(file_path)

        self._insert_data_in_repository()
        
    def _save_file(self, file):
        file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + file.name
        return default_storage.save(file_name, file)

    def _create_data_famre(self, file_path):
        self.set_data_frame(pd.read_excel(file_path))

    def _insert_data_in_repository(self):
        mongo_service = InsertData()
        data_json = self.data_frame.to_json(orient='records')
        mongo_service.insert_collection(json.loads(data_json))    