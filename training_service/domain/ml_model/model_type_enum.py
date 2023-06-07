from enum import Enum


class ModelTypeOptions(Enum):
    logistic_regression = "logistic_regression"
    knn = "knn"
    svm = "svm"
    naive_bayes = "naive_bayes"
    decision_trees = "decision_trees"
    linear_regression = "linear_regression"