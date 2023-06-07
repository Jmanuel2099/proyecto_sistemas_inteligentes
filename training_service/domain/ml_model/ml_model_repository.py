from abc import ABC, abstractmethod
from typing import Any, List
from .ml_model import MLModel


class MlModelRepository(ABC):

    @abstractmethod
    def insert_ml_model(self, model_to_insert:MLModel) -> Any:
        pass

    @abstractmethod
    def get_ml_models(self, limit:int) ->List[MLModel]:
        pass
