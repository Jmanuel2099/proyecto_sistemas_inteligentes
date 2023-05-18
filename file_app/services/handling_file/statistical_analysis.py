from django.conf import settings
import os
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


class StatisticalAnalysis:

    HISTOGRAMS_FOLDER = 'histograms'
    CORRELATION_MATRIX_FOLDER=' correlation_matrix'
    
    def __init__(self, file) -> None:
        self.file = file

    # def discard(self):
    #     try:
    #         data_frame = self.file.get_data_frame()
    #         data_without_NaN = data_frame.dropna()

    #         self.file.set_df_not_missing_data(data_without_NaN)
    #         self.file.save_df_not_missing_data_in_local(self.DATAFRAME_FOLDER_WITH_DESCARD)
    #     except Exception as error:
    #         raise error

    # def imputation(self):
    #     try:
    #         data_frame = self.file.get_data_frame()
    #         num_columns = data_frame.select_dtypes(np.number).columns
    #         obj_columns = data_frame.select_dtypes(object).columns

    #         data_frame = self._average_imputation(data_frame, num_columns)
    #         data_frame = self._mode_imputation(data_frame, obj_columns)

    #         self.file.set_df_not_missing_data(data_frame)
    #         self.file.save_df_not_missing_data_in_local(self.DATAFRAME_FOLDER_WITH_AVERAGE_IMPUTATION)
    #     except Exception as error:
    #         raise error

    # def _average_imputation(self, data_frame, numeric_columns):
    #     for column in numeric_columns:
    #         media = data_frame[column].mean()
    #         data_frame[column].fillna(media, inplace=True)
    #     return data_frame

    # def _mode_imputation(self, data_frame, not_numeric_columns):
    #     for column in not_numeric_columns:
    #         mode = data_frame[column].mode()[0]
    #         data_frame[column].fillna(mode, inplace=True)
    #     return data_frame

    def histograms(self):
        try:
            data_frame = self.file.get_df_not_missing_data()
            if data_frame is None:
                return None

            df_numeric = data_frame.select_dtypes(np.number)
            plt.rcParams['figure.figsize'] = (16, 9)
            plt.style.use('ggplot')
            df_numeric.hist()

            folder_path_to_save = os.path.join(settings.MEDIA_ROOT, self.HISTOGRAMS_FOLDER)
            if not os.path.exists(folder_path_to_save):
                os.makedirs(folder_path_to_save)
            file_path_to_save = os.path.join(folder_path_to_save, 
                                    f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
            plt.savefig(file_path_to_save)
            return file_path_to_save
        except Exception as error:
            raise error
        
    def correlation_matrix(self):
        try:
            data_frame = self.file.get_df_not_missing_data()
            if data_frame is None:
                return None
            df_numeric = data_frame.select_dtypes(np.number)
            correlation_matrix = df_numeric.astype(float).corr()
            colormap = plt.cm.coolwarm
            plt.figure(figsize=(12,12))
            plt.title('Correlation of Features', y=1.05, size=15)
            sb.heatmap(correlation_matrix,linewidths=0.1,vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)

            folder_path_to_save = os.path.join(settings.MEDIA_ROOT, self.CORRELATION_MATRIX_FOLDER)
            if not os.path.exists(folder_path_to_save):
                    os.makedirs(folder_path_to_save)
            file_path_to_save = os.path.join(folder_path_to_save, 
                                        f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
            plt.savefig(file_path_to_save)
            return file_path_to_save
        except Exception as error:
            raise error
