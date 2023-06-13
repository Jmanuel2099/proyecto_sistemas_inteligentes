import os
import numpy as np
import pandas as pd
from datetime import datetime
from .model_type_enum import ModelTypeOptions
from preprocessing_service.domain.file import FileSingleton
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, cross_val_predict, cross_validate, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import pickle


class MLModel:

    FOLDER_STORE_TRAINED_MODELS ='trained_models'

    def __init__(self, model_type, 
                normalization_type, 
                overfitting_underfitting, 
                target, 
                all_features, 
                features=None, 
                percent_tests=None, 
                number_folds=None, 
                neighbors=None, 
                kernel=None, 
                depth=None, 
                accuracy=0, 
                precision=0, 
                recall=0, 
                f1=0, 
                trained_model_path="",
                dataset_file = "") -> None:
        self.model_type = model_type
        self.normalization_type = normalization_type
        self.overfitting_underfitting = overfitting_underfitting
        self.target = target
        self.all_features = all_features
        self.features = features
        self.percent_tests = percent_tests
        self.number_folds = number_folds
        self.neighbors = neighbors
        self.kernel = kernel
        self.depth = depth
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall 
        self.f1 = f1
        self.trained_model_path = trained_model_path
        self.dataset_file = dataset_file
        self.dataframe = self.get_dataframe()

    def to_dict(self):
        return{
            "model_type": self.model_type,
            "normalization_type": self.normalization_type,
            "overfitting_underfitting": self.overfitting_underfitting,
            "target": self.target,
            "all_features": self.all_features,
            "features": self.features,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "trained_model_path": self.trained_model_path,
            "dataset_file": self.dataset_file
        }
    
    def get_dataframe(self):
        file = FileSingleton()
        self.dataset_file = file.get_dataset_file()
        return file.get_df_not_missing_data()

    def get_model_type(self):
        if self.model_type == ModelTypeOptions.logistic_regression.value:
            return LogisticRegression()
        elif self.model_type == ModelTypeOptions.knn.value:
            return KNeighborsClassifier(n_neighbors=self.neighbors)
        elif self.model_type == ModelTypeOptions.linear_regression.value:
            return LinearRegression()
        elif self.model_type == ModelTypeOptions.naive_bayes.value:
            return GaussianNB()
        elif self.model_type == ModelTypeOptions.decision_trees.value:
            return DecisionTreeClassifier(max_depth=self.depth)
        elif self.model_type == ModelTypeOptions.svm.value:
            return SVC(kernel=self.kernel)
        else:
            return None

    def get_features_and_target(self):
        try:
            if self.dataframe is None:
                return None

            if self.all_features:
                X = self.dataframe.drop([self.target], axis=1)
                self.features = list(X.columns)
            else:
                if not self._existsColumnsInDataframe():
                    return None

                X = self.dataframe.loc[:, self.features]
            y = self.dataframe[self.target]

            return X, y
        except Exception as error:
            raise error

    def encoder_target(self, target):
        try:
            if not pd.api.types.is_numeric_dtype(target):
                encoder = LabelEncoder()
                return encoder.fit_transform(target)
            
            return target
        except Exception as error:
            raise error

    def encoder_categorical_columns(self, dataframe):
        try:
            encoder = LabelEncoder()
            categorical_columns = dataframe.select_dtypes(include=['object']).columns
            for column in categorical_columns:
                dataframe[column] = encoder.fit_transform(dataframe[column].astype(str))

            return dataframe
        except Exception as error:
            raise error

    def normalization_by_minmax(self, dataframe):
        try:
            scalar = MinMaxScaler()
            numerical_columns = dataframe.select_dtypes(include=np.number).columns
            dataframe[numerical_columns] = scalar.fit_transform(dataframe[numerical_columns])

            return dataframe
        except Exception as error:
            raise error

    def normalization_by_standar_scaler(self, dataframe):
        try:
            scalar = StandardScaler()
            numerical_columns = dataframe.select_dtypes(include=np.number).columns
            dataframe[numerical_columns] = scalar.fit_transform(dataframe[numerical_columns])

            return dataframe
        except Exception as error:
            raise error

    def hold_out(self, X, y):
        # try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(self.percent_tests / 100), random_state=6)

        return X_train, X_test, y_train, y_test
        # except Exception as error:
        #     raise error

    def fit_hold_out(self, model, x_train, x_test, y_train, y_test):
        # try:
        model.fit(x_train, y_train)
        self._save_model_in_local(model)
        y_predict= model.predict(x_test)
        self._metrics(y_test=y_test, y_predict= y_predict)

        return self.to_dict()
        # except Exception as error:
        #     raise error

    def cross_validation(self, model, X, y):
        # try:
        kf = KFold(n_splits=self.number_folds, shuffle=True)
        cv_results = cross_validate(model, X=X, y=y,scoring=['accuracy', 'precision', 'recall', 'f1'], cv=kf)
        self.accuracy = cv_results['test_accuracy'].mean()
        self.precision = cv_results['test_precision'].mean()
        self.recall = cv_results['test_recall'].mean()
        self.f1 = cv_results['test_f1'].mean()

        model.fit(X, y)
        self._save_model_in_local(model)
        return self.to_dict()
        # except Exception as error:
        #     raise error

    def _save_model_in_local(self, model):
        try:
            folder_path = os.path.join(self.FOLDER_STORE_TRAINED_MODELS, self.model_type)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            path_model_file = os.path.join(folder_path, f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pkl' )
            # joblib.dump(model, path_model_file)
            with open(path_model_file, 'wb') as f:
                pickle.dump(model, f)
            self.trained_model_path = path_model_file
        except Exception as error:
            raise error

    def _metrics(self, y_test, y_predict):
        try:
            self.accuracy = accuracy_score(y_test, y_predict)
            print("acc: ", self.accuracy)
            self.precision = precision_score(y_test, y_predict)
            print("precc: ", self.precision)
            self.recall = recall_score(y_test, y_predict)
            print("rec: ", self.recall)
            self.f1 = f1_score(y_test, y_predict)
            print("f1:", self.f1)

        except Exception as error:
            raise error

    def _existsColumnsInDataframe(self):
        columns_df = self.dataframe.columns.tolist()
        if all(columna in columns_df for columna in self.features):
            return True
        return False
