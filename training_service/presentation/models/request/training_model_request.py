from pydantic import BaseModel, Field
from enum import Enum


class ModelNameOptions(str, Enum):
    logistic_regression = "logistic_regression"
    knn = "knn"
    svm = "svm"
    naive_bayes = "naive_bayes"
    decision_trees = "decision_trees"
    linear_regression = "linear_regression"

class NormalizationOptions(str, Enum):
    min_max = "min_max"
    standar_scaler = "standard_scaler"

class OverfittingUnderfittingOptions(str, Enum):
    cross_validation = "cross_validation"
    hold_out = "hold_out"

class KenerOptions(str, Enum):
    rbf = "rbf"
    poly = "poly"

class TrainingModelRequest(BaseModel):
    model_type: ModelNameOptions = Field(max_length=20)
    normalization_type: NormalizationOptions = Field(max_length=16)
    overfitting_underfitting: OverfittingUnderfittingOptions = Field(max_length=17)
    target: str = Field(max_length=50)
    all_features : bool | None = False
    features: list[str] | None = None
    percent_tests: int | None = None
    number_folds: int | None = None
    neighbors: int | None = None
    kernel: KenerOptions | None = Field(default=None, max_length=4)
    depth: int | None = None