from pydantic import BaseModel


class ErrorResposne(BaseModel):
    error : str
    message : str