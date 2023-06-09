from pydantic import BaseModel


class MlModelTrainedResponse(BaseModel):
    model_type: str
    normalization_type: str
    overfitting_underfitting: str
    target: str
    all_features : bool | None = None
    features: list[str] | None = None 
    accuracy: float | int
    precision: float | int
    recall: float | int
    f1: float | int
    trained_model_path: str
    dataset_file: str