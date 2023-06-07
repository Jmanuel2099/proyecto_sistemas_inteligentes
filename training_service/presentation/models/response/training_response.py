from pydantic import BaseModel


class TrainingResponse(BaseModel):
    accuracy : float
    precision : float
    recall : float
    f1 : float