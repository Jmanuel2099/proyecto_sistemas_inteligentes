from django.conf import settings
import os
from datetime import datetime
import numpy as np
import pandas as pd


class StatisticalAnalysis:

    DATAFRAME_FOLDER_WITH_DESCARD = 'dataframa_with_descard'
    DATAFRAME_FOLDER_WITH_AVERAGE_IMPUTATION = 'dataframa_with_average_imputation'


    def __init__(self, file) -> None:
        self.file = file

    def discard(self):
        try:
            data_frame = self.file.get_data_frame()
            data_without_NaN = data_frame.dropna()

            self.file.set_df_not_missing_data(data_without_NaN)
            self.file.save_df_not_missing_data_in_local(self.DATAFRAME_FOLDER_WITH_DESCARD)
        except Exception as error:
            raise error

    def imputation(self):
        try:
            data_frame = self.file.get_data_frame()
            num_columns = data_frame.select_dtypes(np.number).columns
            obj_columns = data_frame.select_dtypes(object).columns

            data_frame = self._average_imputation(data_frame, num_columns)
            data_frame = self._mode_imputation(data_frame, obj_columns)

            self.file.set_df_not_missing_data(data_frame)
            self.file.save_df_not_missing_data_in_local(self.DATAFRAME_FOLDER_WITH_AVERAGE_IMPUTATION)
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
