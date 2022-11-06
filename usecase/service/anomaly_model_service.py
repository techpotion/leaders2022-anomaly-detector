from typing import Any

class CombinedModelService:
    __model: Any

    def __init__(self, model: Any):
        self.__model = model

    def predict_single(self, d: dict) -> dict:
        return self.__model.predict_single(d)

    def predict_multiple(self, ds: list[dict]) -> list[dict]:
        return self.__model.predict_multiple(ds)

