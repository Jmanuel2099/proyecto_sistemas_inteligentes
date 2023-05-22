import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


class Statistics:
    HISTOGRAMS_FOLDER = 'histograms'
    CORRELATION_MATRIX_FOLDER=' correlation_matrix'

    def __init__(self, file) -> None:
        self.file = file

    def histograms(self):
        try:
            data_frame = self.file.get_df_not_missing_data()
            if data_frame is None:
                return None

            df_numeric = data_frame.select_dtypes(np.number)
            plt.rcParams['figure.figsize'] = (16, 9)
            plt.style.use('ggplot')
            df_numeric.hist()

            folder_path_to_save = self.file.create_folder_to_store_files(self.HISTOGRAMS_FOLDER)
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

            folder_path_to_save = self.file.create_folder_to_store_files(self.CORRELATION_MATRIX_FOLDER)
            file_path_to_save = os.path.join(folder_path_to_save, 
                                        f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
            plt.savefig(file_path_to_save)
            return file_path_to_save
        except Exception as error:
            raise error