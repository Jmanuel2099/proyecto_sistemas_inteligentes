from training_service.domain.ml_model.ml_model_repository import MlModelRepository
from training_service.domain.ml_model.ml_model import MLModel
from typing import Any, List, Union


class MlModelsByFeaturesUseCase:
    def __init__(self, repository: MlModelRepository) -> None:
        self.repository = repository

    def get_ml_models_by_features(self, limit:int, featurs:Union[List[str], bool]) -> List[MLModel]:
        try:
            records = self.repository.get_ml_models_by_filter(limit, featurs)
            if not records:
                return None
            ml_models = []
            for record in records:
                ml_models.append(record.to_dict())
            
            return ml_models
        except Exception as error:
            raise error

