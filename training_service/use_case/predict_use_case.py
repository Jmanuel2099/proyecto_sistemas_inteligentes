import joblib


class PredictUseCase:

    def __init__(self) -> None:
        pass

    def predict(self, ml_model_path, features):
        # try:
        loaded_ml_model = joblib.load(ml_model_path)
        prediction = loaded_ml_model.predict(features)
        
        return prediction
        # except Exception as error:
        #     raise error
