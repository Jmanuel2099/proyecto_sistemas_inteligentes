from pydantic import BaseModel

class UploadFileResponse(BaseModel):
    local_file_path : str
    docs_inserted_mongo : int