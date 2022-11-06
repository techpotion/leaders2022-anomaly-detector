from flask import Flask, request

from usecase.combinedModelPredictMultipleUsecase import (
    CombinedModelPredictMultipleUsecase,
)
from usecase.combinedModelPredictSingleUsecase import CombinedModelPredictSingleUsecase

class Server:
    __host: str
    __port: int
    __engine: Flask
    __combined_model_predict_multiple_usecase: CombinedModelPredictMultipleUsecase
    __combined_model_predict_single_usecase: CombinedModelPredictSingleUsecase

    def __init_flask_with_routes(self) -> None:
        engine = Flask(__name__)

        @engine.route("/health", methods=['GET'])
        def health_check_handler() -> dict[str, str]:
            return {"status": "ok"}

        @engine.route("/combined_model/predict_single", methods=['POST'])
        def combined_model_predict_single_handler() -> dict:
            content = request.json
            return self.__combined_model_predict_single_usecase.execute(content)

        @engine.route("/combined_model/predict_multiple", methods=['POST'])
        def combined_model_predict_multiple_handler() -> list[dict]:
            content = request.json
            return self.__combined_model_predict_multiple_usecase.execute(content)


        self.__engine = engine


    def __init__(
        self,
            host: str,
            port: int,
            combined_model_predict_multiple_usecase: CombinedModelPredictMultipleUsecase,
            combined_model_predict_single_usecase: CombinedModelPredictSingleUsecase,
        ) -> None:
        self.__host = host
        self.__port = port

        self.__combined_model_predict_multiple_usecase = combined_model_predict_multiple_usecase
        self.__combined_model_predict_single_usecase = combined_model_predict_single_usecase

        self.__init_flask_with_routes()


    def start(self) -> None:
        self.__engine.run(host=self.__host, port=self.__port)

