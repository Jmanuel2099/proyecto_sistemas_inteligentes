from pydantic import BaseModel, Field
from enum import Enum


class ModelNameOptions(str, Enum):
    logistic_regression = "logistic_regression"
    knn = "knn"
    svm = "svm"
    naive_bayes = "naive_bayes"
    decision_trees = "decision_trees"
    linear_regression = "linear_regression"

class overfitting_underfittingOptions(str, Enum):
    cross_validation = "cross_validation"
    hold_out = "hold_out"

class NormalizationOptions(str, Enum):
    min_max = "min_max"
    standar_scaler = "standar_scaler"

class KenerOptions(str, Enum):
    rbf = "rbf"
    poly = "poly"

class TrainingRequest(BaseModel):
    model_name: ModelNameOptions = Field(max_length=20)
    normalization: NormalizationOptions = Field(max_length=16)
    overfitting_underfitting: overfitting_underfittingOptions = Field(max_length=17)
    percent_tests: int | None = None
    number_folds: int | None = None
    target: str = Field(max_length=50)
    featires: list[str]
    neighbors: int | None = None
    kernel: KenerOptions | None = Field(default=None, max_length=4)
    depth: int | None = None