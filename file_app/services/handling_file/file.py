from django.core.files.storage import default_storage
from django.conf import settings
import os
import pandas as pd
from datetime import datetime
from file_app.services.mongodb.insert_data import InsertData


class File:
    def __init__(self) -> None:
        self.data_frame = None
        self.data_frame_not_missing_data = None
        self.path = ''

    def get_data_frame(self):
        return self.data_frame
    
    def set_data_frame(self, new_data_frame):
        self.data_frame = new_data_frame

    def get_df_not_missing_data(self):
        return self.data_frame_not_missing_data

    def set_df_not_missing_data(self, new_df):
        self.data_frame_not_missing_data = new_df

    def get_path(self):
        return self.path

    def set_path(self, new_path):
        self.path = new_path

    def save_file_in_local(self, file):
        name_new_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + file.name
        name_new_file = default_storage.save(name_new_file, file)
        self.set_path(os.path.join(settings.MEDIA_ROOT, name_new_file))
        self._create_data_frame()

    def describe_data(self):
        first_record_dict = self.data_frame.iloc[0].to_dict()
        return {key: type(value).__name__ for key, value in first_record_dict.items()}

    def save_df_not_missing_data_in_local(self, folder_name):
        path_excel_file = os.path.join(settings.MEDIA_ROOT,
                                       folder_name,
                                       f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx')
        self.path = path_excel_file
        self.data_frame_not_missing_data.to_excel(self.path)

    def _create_data_frame(self):
        self.set_data_frame(pd.read_excel(self.path))
