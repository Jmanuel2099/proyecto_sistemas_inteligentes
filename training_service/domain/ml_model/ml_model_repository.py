from abc import ABC, abstractmethod
from typing import Any, List, Union
from .ml_model import MLModel


class MlModelRepository(ABC):

    @abstractmethod
    def insert_ml_model(self, model_to_insert:MLModel) -> Any:
        pass

    @abstractmethod
    def get_all_ml_models(self) -> List[MLModel]:
        pass

    @abstractmethod
    def get_ml_models_by_filter(self, limit:int, featurs:Union[List[str], bool]) -> List[MLModel]:
        pass