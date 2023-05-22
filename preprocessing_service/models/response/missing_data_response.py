from pydantic import BaseModel


class MissingDataResponse(BaseModel):
    local_file_path : str
    docs_inserted_mongo : int