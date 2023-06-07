from pydantic import BaseModel


class MlModelMetricResponse(BaseModel):
    model_type: str
    normalization_type: str
    overfitting_underfitting: str
    target: str
    all_features : bool
    features: list[str]
    accuracy: int
    precision: int
    recall: int
    f1: int