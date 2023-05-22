from pydantic import BaseModel

class GraphicalAnalysisResponse(BaseModel):
    histograms_path : str
    correlation_matrix_path : str
