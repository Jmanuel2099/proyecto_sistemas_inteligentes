from pydantic import BaseModel


class PredictResponse(BaseModel):
    prediction: float | int | str 