from django.conf import settings
import os
from datetime import datetime
import numpy as np
import pandas as pd

class StatisticalAnalysis:

    AVERAGE_IMPUTATION_METHOD = 1
    DESCARD_METHOD = 2
    DATAFRAME_FOLDER_WITH_DESCARD = 'dataframa_with_descard'
    DATAFRAME_FOLDER_WITH_AVERAGE_IMPUTATION = 'dataframa_with_average_imputation'


    def __init__(self, file) -> None:
        self.file = file

    def discard(self):
        data_frame = self.file.get_data_frame()
        data_without_NaN = data_frame.dropna()

        self.file.set_df_not_missing_data(data_without_NaN)
        path_excel_file = os.path.join(settings.MEDIA_ROOT,
                                       self.DATAFRAME_FOLDER_WITH_DESCARD,
                                       f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx')
        self.file.set_path(path_excel_file)
        data_without_NaN.to_excel(self.file.get_path())

    def imputation(self):
        data_frame = self.file.get_data_frame()
        num_columns = data_frame.select_dtypes(np.number).columns
        obj_columns = data_frame.select_dtypes(object).columns

        print('number', num_columns)
        print('obj', obj_columns)

        data_frame = self._average_imputation(data_frame, num_columns)
        data_frame = self._mode_imputation(data_frame, obj_columns)

        self.file.set_df_not_missing_data(data_frame)
        path_excel_file = os.path.join(settings.MEDIA_ROOT,
                                       self.DATAFRAME_FOLDER_WITH_AVERAGE_IMPUTATION,
                                       f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx')
        self.file.set_path(path_excel_file)
        data_frame.to_excel(self.file.get_path())

    def _average_imputation(self, data_frame, numeric_columns):
        for column in numeric_columns:
            print('col_num', column)
            media = data_frame[column].mean()
            data_frame[column].fillna(media, inplace=True)
        return data_frame

    def _mode_imputation(self, data_frame, not_numeric_columns):
        for column in not_numeric_columns:
            print('col_obj', column)
            mode = data_frame[column].mode()[0]
            data_frame[column].fillna(mode, inplace=True)
        return data_frame
