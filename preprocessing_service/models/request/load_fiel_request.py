from pydantic import BaseModel
from fastapi import UploadFile


class LoadFielRequest(BaseModel):
    file : UploadFile
