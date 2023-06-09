# data base
from training_service.data_base.mongodb.implemetation import MongoImplementation
# use cases
from training_service.use_case.training_use_case import TrainingUseCase
from training_service.use_case.all_ml_models_metrics_use_case import AllMlModelsMetricsUseCase
from training_service.use_case.ml_models_by_features_use_case import MlModelsByFeaturesUseCase
from training_service.use_case.predict_use_case import PredictUseCase
# domain
from training_service.domain.ml_model.ml_model import MLModel
# from training_service.presentation.models.request.training_model_request import TrainingModelRequest

CURRENT_REPO = "mongo"

def config_predict_use_case():
    return PredictUseCase()

def config_training_use_case(model: MLModel):
    repository = _config_repositories()
    return TrainingUseCase(model= model, repository=repository)

def config_all_ml_models_metrics_use_case():
    repository = _config_repositories()
    return AllMlModelsMetricsUseCase(repository=repository)

def config_ml_models_by_features_use_case():
    repository = _config_repositories()
    return MlModelsByFeaturesUseCase(repository=repository)

def _config_repositories():
    if CURRENT_REPO == "mongo":
        return MongoImplementation()
    if CURRENT_REPO == "other":
        return None
