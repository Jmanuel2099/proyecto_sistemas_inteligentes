from typing import Any, Union
from fastapi import APIRouter, UploadFile, Response, status
# Models
from preprocessing_service.models.request.load_fiel_request import LoadFielRequest
from preprocessing_service.models.request.missing_data_options import MissingDataOptions
from preprocessing_service.models.response.error_resposne import ErrorResposne
from preprocessing_service.models.response.upload_file_response import UploadFileResponse
from preprocessing_service.models.response.missing_data_response import MissingDataResponse
from preprocessing_service.models.response.graphical_analysis_response import GraphicalAnalysisResponse
# Handlers
from preprocessing_service.handler.handling_file import HandlingFile
from preprocessing_service.handler.handling_statistics import HandlingStatistics


file_handler = HandlingFile()
# statistics_handler = HandlingStatistics(file_handler.get_file())
statistics_handler = HandlingStatistics()

router = APIRouter(
    prefix="/preprocessing",
    tags=["preprocessing"]
)

@router.post("/upload_file", 
             status_code=200, 
             response_model= Union[UploadFileResponse, ErrorResposne])
async def load_file(file: UploadFile, response: Response) -> Any:
    try:
        if file.filename.split('.')[1] != 'xlsx':
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ErrorResposne(error= status.HTTP_400_BAD_REQUEST, 
                                message= "expect a file with .xlsx extension.")
            
        resp = file_handler.save_file(file)
        return UploadFileResponse(local_file_path=resp[0], docs_inserted_mongo=resp[1])
    except Exception as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.get("/describe_file", 
            status_code=200, 
            response_model= Union[dict, ErrorResposne])
async def describe_file(response: Response):
    try:
        resp = file_handler.describe_file()
        if resp is None:
            response.status_code = status.HTTP_424_FAILED_DEPENDENCY
            return ErrorResposne(error= status.HTTP_424_FAILED_DEPENDENCY, 
                                message= "No document has been uploaded yet.")
        return resp
    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.get("/missing_data/{method_id}", 
            status_code=200,
            response_model= Union[MissingDataResponse, ErrorResposne])
async def missing_data(method_id: MissingDataOptions, response: Response):
    try:
        resp = file_handler.process_missing_data(method_id)
        if resp is None:
            response.status_code = status.HTTP_424_FAILED_DEPENDENCY
            return ErrorResposne(error= status.HTTP_424_FAILED_DEPENDENCY, 
                                message= "No document has been uploaded yet.")
        
        return MissingDataResponse(local_file_path= resp[0], docs_inserted_mongo= resp[1])
    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

@router.get("/graphicalanalysis",
            status_code=200,
            response_model= Union[GraphicalAnalysisResponse, ErrorResposne] )
async def graphical_statistical_analysis(response: Response):
    try:
        resp = statistics_handler.graphical_analysis()
        if resp is None:
            response.status_code = status.HTTP_424_FAILED_DEPENDENCY
            return ErrorResposne(error= status.HTTP_424_FAILED_DEPENDENCY, 
                                message= "It is recommended to do the missing data treatment first.")
        return GraphicalAnalysisResponse(histograms_path= resp[0],
                                        correlation_matrix_path= resp[1])
    except Exception as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
