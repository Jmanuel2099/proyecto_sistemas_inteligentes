from preprocessing_service.domain.statistics import Statistics
from preprocessing_service.domain.file import FileSingleton


class HandlingStatistics:
    # def __init__(self, file) -> None:
    #     self.file = file
    #     self.statisticalAnalysis = Statistics(self.file)

    def __init__(self) -> None:
        self.statisticalAnalysis = Statistics()

    def graphical_analysis(self):
        histograms = self.statisticalAnalysis.histograms()
        correlation_matrix = self.statisticalAnalysis.correlation_matrix()

        if histograms is None or correlation_matrix is None:
            return None
        return histograms, correlation_matrix
