from .service.anomaly_model_service import CombinedModelService

class CombinedModelPredictMultipleUsecase:
    __combined_model_service: CombinedModelService

    def __init__(self, combined_model_service: CombinedModelService) -> None:
        self.__combined_model_service = combined_model_service

    def execute(self, requests: list[dict] | None) -> list[dict]:
        if not requests:
            raise Exception('empty requests')

        return self.__combined_model_service.predict_multiple(requests)
