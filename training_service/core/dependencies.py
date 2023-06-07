# data base
from training_service.data_base.mongodb.implemetation import MongoImplementation
# use cases
from training_service.use_case.training_use_case import TrainingUseCase
from training_service.use_case.visualize_metrics_use_case import VisualizeMetricsUseCase
# domain
from training_service.domain.ml_model.ml_model import MLModel
# from training_service.presentation.models.request.training_model_request import TrainingModelRequest

CURRENT_REPO = "mongo"

def config_training_use_case(model: MLModel):
    repository = _config_repositories()
    return TrainingUseCase(model= model, repository=repository)

def config_visualize_metrics_use_case():
    repository = _config_repositories()
    return VisualizeMetricsUseCase(repository=repository)

def _config_repositories():
    if CURRENT_REPO == "mongo":
        return MongoImplementation()
    if CURRENT_REPO == "other":
        return None
