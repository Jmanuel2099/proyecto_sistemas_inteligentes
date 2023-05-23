from typing import Any, Union
from fastapi import APIRouter, Response, status
# Models
from training_service.models.request.training_request import TrainingRequest
from training_service.models.response.error_response import ErrorResposne


router = APIRouter(
    prefix="/training",
    tags=["training"]
)

@router.post("/training_model",
            status_code= status.HTTP_200_OK, 
            response_model= ErrorResposne)
def training_model(training_request: TrainingRequest, response: Response) -> Any:
    training_request.hola