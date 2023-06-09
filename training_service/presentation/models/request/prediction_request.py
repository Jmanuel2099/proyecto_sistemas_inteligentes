from pydantic import BaseModel
from typing import List, Any


class PredictionRequest(BaseModel):
    model_identifier: str
    data: List[Any]