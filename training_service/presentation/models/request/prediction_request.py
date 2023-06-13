from pydantic import BaseModel
from typing import Dict, Any


class PredictionRequest(BaseModel):
    model_identifier: str
    data: Dict[str, Any]