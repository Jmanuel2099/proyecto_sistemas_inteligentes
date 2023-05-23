from training_service.domain.training import Training
from training_service.models.request.training_request import TrainingRequest, ModelNameOptions

class HandlingTraining:

    def __init__(self) -> None:
        self.training = Training()

    def training_model(self, model_training: TrainingRequest):
        pass
    