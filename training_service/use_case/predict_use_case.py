import joblib
import numpy as np


class PredictUseCase:

    def __init__(self) -> None:
        pass

    def predict(self, ml_model_path, features):
        # try:
        new_query = np.array([features])
        loaded_ml_model = joblib.load(ml_model_path)
        prediction = loaded_ml_model.predict(new_query)
        
        return prediction
        # except Exception as error:
        #     raise error
