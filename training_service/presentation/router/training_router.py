from typing import Any, Union, List
from fastapi import APIRouter, Response, status
# Models
from training_service.presentation.models.request.training_model_request import TrainingModelRequest, ModelNameOptions, OverfittingUnderfittingOptions
from training_service.presentation.models.request.get_model_request import GetMlModelRequest
from training_service.presentation.models.request.prediction_request import PredictionRequest
from training_service.presentation.models.response import error_response, ml_model_trained_response, predict_response
# mapper
from training_service.presentation.mapper.training_request_to_ml_mdel import TrainingRequestToMLModel
#config dependencies
from training_service.core.dependencies import config_training_use_case, config_all_ml_models_metrics_use_case, config_ml_models_by_features_use_case, config_predict_use_case


router = APIRouter(
    prefix="/training",
    tags=["training"]
)

@router.post("/training_model",
            status_code= status.HTTP_200_OK, 
            response_model= Union[ml_model_trained_response.MlModelTrainedResponse, error_response.ErrorResponse])
def training_model(request: TrainingModelRequest, response: Response) -> Any:
    # try:
    error_resp = _check_possible_request_error(request, response)
    if error_resp is not None:
        return error_resp

    mapper = TrainingRequestToMLModel()
    use_case = config_training_use_case(mapper.mapper_request_to_mlmodel(fastapi_model=request))
    resp = use_case.training()
    if resp is None:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return error_response.ErrorResponse(error= status.HTTP_408_REQUEST_TIMEOUT,
                                            message="You have to verify that you have loaded the dataset or that the columns and target are correct.")

    return ml_model_trained_response.MlModelTrainedResponse(**resp)
    # except Exception as error:
    #     print(error)
    #     response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.post("/models_features",
        status_code= status.HTTP_200_OK,
        response_model=Union[List[ml_model_trained_response.MlModelTrainedResponse], error_response.ErrorResponse])
def get_ml_models_by_features(request: GetMlModelRequest, response: Response) -> Any:
    try:
        use_case = config_ml_models_by_features_use_case()
        if request.all_features:
            ml_models = use_case.get_ml_models_by_features(request.limit, request.all_features)
        if request.features:
            ml_models = use_case.get_ml_models_by_features(request.limit, request.features)

        if not ml_models:
            response.status_code = status.HTTP_408_REQUEST_TIMEOUT
            return error_response.ErrorResponse(error= status.HTTP_408_REQUEST_TIMEOUT,
                                                message="No records found in the database.")
        resp = []
        for data_ml_model in ml_models:
            resp.append(ml_model_trained_response.MlModelTrainedResponse(**data_ml_model))

        return resp
    except Exception as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.get("/list_models",
        status_code= status.HTTP_200_OK,
        response_model=Union[List[ml_model_trained_response.MlModelTrainedResponse], error_response.ErrorResponse])
def visualize_model_metrics(response: Response) -> Any:
    try:
        use_case = config_all_ml_models_metrics_use_case()
        ml_models = use_case.get_all_models_whit_metrics()
        if not ml_models:
            response.status_code = status.HTTP_408_REQUEST_TIMEOUT
            return error_response.ErrorResponse(error= status.HTTP_408_REQUEST_TIMEOUT,
                                                message="No records found in the database.")
        resp = []
        for data_ml_model in ml_models:
            resp.append(ml_model_trained_response.MlModelTrainedResponse(**data_ml_model))

        return resp
    except Exception as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.post("/predict",
             status_code= status.HTTP_200_OK,
             response_model=Union[predict_response.PredictResponse, error_response.ErrorResponse])
def make_prediction(request: PredictionRequest, response: Response):
    # try:
    use_case = config_predict_use_case()
    resp = use_case.predict(ml_model_path= request.model_identifier, features=request.data)
    prediction_response = predict_response.PredictResponse(prediction=resp[0])
    return prediction_response
    # except Exception as error:
    #     print(error)
    #     response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

def _check_possible_request_error(request, response):
    if (request.model_type == ModelNameOptions.knn 
        and request.neighbors is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for the knn machine learning model the neighbors are needed.")

    if (request.model_type == ModelNameOptions.svm 
        and request.kernel is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for the svm machine learning model the kernel is needed.")
    
    if (request.model_type == ModelNameOptions.decision_trees 
        and request.depth is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for the decision tree machine learning model the depth is needed.")
    
    if (request.overfitting_underfitting == OverfittingUnderfittingOptions.cross_validation 
        and request.number_folds is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for cross validation we need the number folds.")
    if (request.overfitting_underfitting == OverfittingUnderfittingOptions.hold_out 
        and request.percent_tests is None) :
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for hold out we need the percentage test.")
    
    return None
