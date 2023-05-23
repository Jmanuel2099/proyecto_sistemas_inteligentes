import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score, train_test_split, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import KFold


class Training:

    def __init__(self) -> None:
        pass
    
    def logistic_regression(self):
        logistic_regression_model = LogisticRegression()

    def K_nearest_neighbors(self, neighbors):
        knn_model = KNeighborsClassifier(n_neighbors=neighbors)

    def linear_regression(self):
        linear_regression_model = LinearRegression()

    def naive_bayes(self):
        naive_bayes_model = GaussianNB()

    def decision_trees(self, depth):
        decision_trees_model = DecisionTreeClassifier(max_depth=depth)

    def support_vector_machines(self, kernel):
        svc_model = SVC(kernel= kernel)

    def encoder_categorical_columns(self, dataframe):
        try:
            encoder = LabelEncoder()
            categorical_columns = dataframe.select_dtypes(object).columns
            for column in categorical_columns:
                dataframe[column] = encoder.fit_transform(dataframe[column].astype(str))
            return dataframe
        except Exception as error:
            raise error

    def normalization_by_minmax(self, dataframe):
        try:
            scalar = MinMaxScaler()
            numerical_columns = dataframe.select_dtypes(np.number).columns
            for column in numerical_columns:
                dataframe[column] = scalar.fit_transform(dataframe[column])

            return dataframe
        except Exception as error:
            raise error

    def normalization_by_standar_scaler(self, dataframe):
        try:
            scalar = StandardScaler()
            numerical_columns = dataframe.select_dtypes(np.number).columns
            for column in numerical_columns:
                dataframe[column] = scalar.fit_transform(dataframe[column])

            return dataframe
        except Exception as error:
            raise error

    def hold_out(self, model, x, y, percent_tests):
        try:
            X_train, X_test, y_train, y_test=train_test_split(x, y, test_size=percent_tests, random_state=6)
            model.fit(X_train, y_train)
            y_predict= model.predict(X_test)
            accuracy = accuracy_score(y_test, y_predict)
            precision = precision_score(y_test, y_predict)
            recall = recall_score(y_test, y_predict)
            f1 = f1_score(y_test, y_predict)
            
        except Exception as error:
            raise error

    def cross_validation(self, model, x, y, number_folds):
        try:
            kf = KFold(n_splits=number_folds)
            y_predict = cross_val_predict(model, X=x, y=y, cv=kf)
            accuracy = accuracy_score(y, y_predict)
            precision = precision_score(y, y_predict)
            recall = recall_score(y, y_predict)
            f1 = f1_score(y, y_predict)

        except Exception as error:
            raise error
