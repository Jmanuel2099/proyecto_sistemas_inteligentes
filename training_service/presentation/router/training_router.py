from typing import Any, Union, List
from fastapi import APIRouter, Response, status
# Models
from training_service.presentation.models.request.training_model_request import TrainingModelRequest, ModelNameOptions, OverfittingUnderfittingOptions
from training_service.presentation.models.response import error_response, training_response, ml_model_metrics_response
# mapper
from training_service.presentation.mapper.training_request_to_ml_mdel import TrainingRequestToMLModel
#config dependencies
from training_service.core.dependencies import config_training_use_case, config_visualize_metrics_use_case


router = APIRouter(
    prefix="/training",
    tags=["training"]
)

@router.post("/training_model",
            status_code= status.HTTP_200_OK, 
            response_model= Union[training_response.TrainingResponse, error_response.ErrorResponse])
def training_model(request: TrainingModelRequest, response: Response) -> Any:
    # try:
    error_response = _check_possible_request_error(request, response)
    if error_response is not None:
        return error_response

    mapper = TrainingRequestToMLModel()
    use_case = config_training_use_case(mapper.mapper_request_to_mlmodel(fastapi_model=request))

    resp = use_case.training()
    return training_response.TrainingResponse(accuracy=resp[0], 
                                            precision=resp[1], 
                                            recall= resp[2], 
                                            f1=resp[3])
    # except Exception as error:
    #     print(error)
    #     response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.get("/model_metrics",
            status_code= status.HTTP_200_OK,
            response_model=Union[List[ml_model_metrics_response.MlModelMetricResponse], error_response.ErrorResponse])
def visualize_model_metrics(response: Response):
    # try:
    resp = []
    use_case = config_visualize_metrics_use_case()
    ml_models = use_case.get_all_models_whit_metrics()
    print("ml_models: ", ml_models)
    for data_model in ml_models:
        resp.append(ml_model_metrics_response.MlModelMetricResponse(**data_model))

    return resp
    # except Exception as error:
    #     print(error)
    #     response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

def _check_possible_request_error(request, response):
    if (request.model_type is ModelNameOptions.knn 
        and request.neighbors is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for the knn machine learning model the neighbors are needed.")

    if (request.model_type is ModelNameOptions.svm 
        and request.kernel is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for the svm machine learning model the kernel is needed.")
    
    if (request.model_type is ModelNameOptions.decision_trees 
        and request.depth is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for the decision tree machine learning model the depth is needed.")
    
    if (request.overfitting_underfitting is OverfittingUnderfittingOptions.cross_validation 
        and request.number_folds is None):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for cross validation we need the number folds.")
    if (request.overfitting_underfitting is OverfittingUnderfittingOptions.hold_out 
        and request.percent_tests is None) :
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response.ErrorResponse(error= status.HTTP_400_BAD_REQUEST, 
                                    message="for hold out we need the percentage test.")
    
    return None
