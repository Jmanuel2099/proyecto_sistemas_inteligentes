# import joblib
import pickle
import numpy as np
import pandas as pd


class PredictUseCase:

    def __init__(self) -> None:
        pass

    def predict(self, ml_model_path, features):
        # try:

        df_to_predict = self.pre_processing_features(features)
        print("df to predict: ", df_to_predict)
        # loaded_ml_model = joblib.load(ml_model_path)
        with open(ml_model_path, 'rb') as f:
            loaded_ml_model = pickle.load(f)

        # print("x_model: ", loaded_ml_model.X)

        prediction = loaded_ml_model.predict(df_to_predict)
        print("prediction: ", prediction[0])
        return prediction
        # except Exception as error:
        #     raise error

    def pre_processing_features(self, features):
        new_features = {}
        for key, value in features.items():
            new_features[key] = [value]

        return pd.DataFrame(new_features)
