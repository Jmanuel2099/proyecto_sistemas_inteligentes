from training_service.domain.ml_model.ml_model import MLModel
from training_service.presentation.models.request.training_model_request import TrainingModelRequest


class TrainingRequestToMLModel:

    def __init__(self) -> None:
        pass

    def mapper_request_to_mlmodel(self, fastapi_model: TrainingModelRequest):
        model_dict = fastapi_model.dict()
        print("model_dict: ", model_dict)
        return MLModel(**model_dict)
