from training_service.domain.ml_model.ml_model_repository import MlModelRepository


class VisualizeMetricsUseCase:
    def __init__(self, repository:MlModelRepository) -> None:
        self.repositoty = repository

    def get_all_models_whit_metrics(self):
        # try:
        models = []
        for model in self.repositoty.get_all_ml_models():
            models.append(model.to_dict())
        
        return models
        # except Exception as error:
        #     raise error
        