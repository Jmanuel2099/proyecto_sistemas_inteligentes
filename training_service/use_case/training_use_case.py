from training_service.domain.ml_model.ml_model import MLModel
from training_service.domain.ml_model.ml_model_repository import MlModelRepository

class TrainingUseCase:
    # overfitting and underfitting
    CROSS_VALIDATION = "cross_validation"
    HOLD_OUT= "hold_out"
    # normalization
    MIN_MAX_NORMALIZATION = "min_max"
    STANDARD_SCALER_NORMALIZATION= "standard_scaler"

    def __init__(self, model:MLModel, repository: MlModelRepository ) -> None:
        self.ml_model = model
        self.repository = repository

    def training(self):
        try:
            features = self.ml_model.get_features_and_target()
            if features is None:
                return None
            
            X, y = features
            X = self.ml_model.encoder_categorical_columns(X)
            y = self.ml_model.encoder_target(y)
            model = self.ml_model.get_model_type()
            ml_model_trained = self._train_without_overfitting_or_underfitting(model, X, y)
            self.repository.insert_ml_model(self.ml_model)

            return ml_model_trained
        except Exception as error:
            raise error

    def _train_without_overfitting_or_underfitting(self, model, X, y):
        try:
            if self.ml_model.overfitting_underfitting == self.CROSS_VALIDATION:
                return self.ml_model.cross_validation(model, self._normalization(X), y)
                
            if self.ml_model.overfitting_underfitting == self.HOLD_OUT:
                X_train, X_test, y_train, y_test = self.ml_model.hold_out(X=X, y=y)
                return self.ml_model.fit_hold_out(model=model, 
                                                x_train=self._normalization(X_train),
                                                x_test=self._normalization(X_test),
                                                y_test= y_test,
                                                y_train=y_train)

            return None
        except Exception as error:
            raise error

    def _normalization(self, dataframe):
        try:
            if self.ml_model.normalization_type == self.MIN_MAX_NORMALIZATION:
                return self.ml_model.normalization_by_minmax(dataframe)
            if self.ml_model.normalization_type == self.STANDARD_SCALER_NORMALIZATION:
                return self.ml_model.normalization_by_standar_scaler(dataframe)
        except Exception as error:
            raise error
        
    
