from training_service.domain.ml_model.ml_model_repository import MlModelRepository


class AllMlModelsMetricsUseCase:
    def __init__(self, repository:MlModelRepository) -> None:
        self.repositoty = repository

    def get_all_models_whit_metrics(self):
        try:
            records = self.repositoty.get_all_ml_models()
            if not records:
                return None
            ml_models = []
            for model in records:
                ml_models.append(model.to_dict())
            
            return ml_models
        except Exception as error:
            raise error
        