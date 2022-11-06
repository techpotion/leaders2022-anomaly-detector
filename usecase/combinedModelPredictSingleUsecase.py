from .service.anomaly_model_service import CombinedModelService

class CombinedModelPredictSingleUsecase:
    __combined_model_service: CombinedModelService

    def __init__(self, combined_model_service: CombinedModelService) -> None:
        self.__combined_model_service = combined_model_service

    def execute(self, request: dict | None) -> dict:
        if not request:
            raise Exception('empty request')

        return self.__combined_model_service.predict_single(request)
