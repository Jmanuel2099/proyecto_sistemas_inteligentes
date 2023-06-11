# from training_service.presentation.models.request.training_model_request import TrainingModelRequest
# from training_service.presentation.mapper.training_request_to_ml_mdel import TrainingRequestToMLModel
# # use case
# from training_service.use_case.training_use_case import TrainingUseCase

# class TrainingHandler:
#     def __init__(self) -> None:
#         self.mapper = TrainingRequestToMLModel()

#     def training(self, requestModel: TrainingModelRequest):
#         use_case = TrainingUseCase(self.mapper.mapper(requestModel))
#         metrics = use_case.training()
#         return metrics