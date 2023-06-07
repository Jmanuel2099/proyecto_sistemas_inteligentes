from pydantic import BaseModel
from typing import List, Union

class GetMlModelRequest(BaseModel):
    limit: int
    all_features: bool | None = False
    features: List[str] | None = None