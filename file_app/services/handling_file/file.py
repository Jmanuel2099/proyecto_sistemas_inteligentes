from django.core.files.storage import default_storage
from django.conf import settings
import os
import pandas as pd
from datetime import datetime
import json
from file_app.services.mongodb.insert_data import InsertData


class File:
    def __init__(self) -> None:
        pass

    def load_file(self, file):
        file_name = self._save_file(file)

        file_path = os.path.join(settings.BASE_DIR, 'archivos\\' + file_name)
        data_json = self._to_json(file_path)
        
        mongo_service = InsertData()
        mongo_service.insert_collection(json.loads(data_json))
        
    def _save_file(self, file):
        file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + file.name
        return default_storage.save(file_name, file)

    def _to_json(self, file_path):
        data_frame = pd.read_excel(file_path)
        # orient='records' indica que el DataFrame debe ser convertido a 
        # una lista de diccionarios donde cada fila del DataFrame se representa como un diccionario.
        return data_frame.to_json(orient='records')