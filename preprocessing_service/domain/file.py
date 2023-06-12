import os
from typing import Any
import pandas as pd
import numpy as np
from datetime import datetime


class SingletonMeta(type):

    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class FileSingleton(metaclass=SingletonMeta):
    """
    This class implements the singleton pattern
    """
    BASE_DIR = "received_files"
    FOLDER_TO_SAVE_NEW_FILES = "new_files"
    DATAFRAME_FOLDER_WITH_DESCARD = 'dataframa_with_descard'
    DATAFRAME_FOLDER_WITH_AVERAGE_IMPUTATION = 'dataframa_with_average_imputation'

    def __init__(self) -> None:
        self.path = ''
        self.data_frame = None
        self.data_frame_not_missing_data = None

    def get_path(self):
        return self.path
    
    def get_data_frame(self):
        return self.data_frame

    def get_df_not_missing_data(self):
        return self.data_frame_not_missing_data

    def set_path(self, new_path):
        self.path = new_path

    def set_data_frame(self, new_data_frame):
        self.data_frame = new_data_frame

    def set_df_not_missing_data(self, new_df):
        self.data_frame_not_missing_data = new_df

    def save_file(self, file):
        try:
            folder_path = self.create_folder_to_store_files(self.FOLDER_TO_SAVE_NEW_FILES)
            name_new_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + file.filename
            path_new_file = os.path.join(folder_path, name_new_file)
            self._save_file_in_local(file ,path_new_file)
        except Exception as error:
            raise error

    def describe_data(self):
        try:
            first_record_dict = self.data_frame.iloc[0].to_dict()
            return {key: type(value).__name__ for key, value in first_record_dict.items()}
        except Exception as error:
            raise error

    def missing_data_by_discard(self):
        try:
            data_without_NaN = self.data_frame.dropna()
            self.set_df_not_missing_data(data_without_NaN)
            self._save_df_not_missing_data_in_local(self.DATAFRAME_FOLDER_WITH_DESCARD)
        except Exception as error:
            raise error

    def missing_data_by_imputation(self):
        try:
            num_columns = self.data_frame.select_dtypes(np.number).columns
            obj_columns = self.data_frame.select_dtypes(object).columns

            data_frame = self._average_imputation(self.data_frame, num_columns)
            data_frame = self._mode_imputation(data_frame, obj_columns)

            self.set_df_not_missing_data(data_frame)
            self._save_df_not_missing_data_in_local(self.DATAFRAME_FOLDER_WITH_AVERAGE_IMPUTATION)
        except Exception as error:
            raise error

    def create_folder_to_store_files(self, folder_name):
        folder_path = os.path.join(self.BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return folder_path

    def _save_file_in_local(self, file, path_file_to_save):
        with open(path_file_to_save, "wb") as buffer:
            buffer.write(file.file.read())
            
        self.set_path(path_file_to_save)
        if file.filename.split('.')[1] == 'xlsx' :
            self._create_data_frame_excel()
        if file.filename.split('.')[1] == 'csv':
            self._create_data_frame_csv()

    def _create_data_frame_excel(self):
        try:
            self.set_data_frame(pd.read_excel(self.path))
        except Exception as error: 
            raise error
    
    def _create_data_frame_csv(self):
        try:
            self.set_data_frame(pd.read_csv(self.path, delimiter=","))
        except Exception as error: 
            raise error

    def _average_imputation(self, data_frame, numeric_columns):
        for column in numeric_columns:
            media = data_frame[column].mean()
            data_frame[column].fillna(media, inplace=True)
        return data_frame

    def _mode_imputation(self, data_frame, not_numeric_columns):
        for column in not_numeric_columns:
            mode = data_frame[column].mode()[0]
            data_frame[column].fillna(mode, inplace=True)
        return data_frame

    def _save_df_not_missing_data_in_local(self, folder_name):
        try:
            path_folder = self.create_folder_to_store_files(folder_name)
            path_excel_file = os.path.join(path_folder,
                                        f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx')
            self.path = path_excel_file
            self.data_frame_not_missing_data.to_excel(self.path, index=False)
        except Exception as error:
            raise error
