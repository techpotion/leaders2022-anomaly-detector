from typing import Any

from config.config import Config
from framework.api.server import Server
from infra.models import get_combined_model
from usecase.combined_model_predict_multiple_usecase import (
    CombinedModelPredictMultipleUsecase,
)
from usecase.combined_model_predict_single_usecase import (
    CombinedModelPredictSingleUsecase,
)
from usecase.plot_efficiency_usecase import PlotEfficiencyUsecase
from usecase.service.anomaly_model_service import CombinedModelService
from usecase.service.plot_service import PlotService

class DI:
    config: Config
    combined_model: Any
    server: Server

    combined_model_service: CombinedModelService
    plot_service: PlotService

    combined_model_predict_multiple_usecase: CombinedModelPredictMultipleUsecase
    combined_model_predict_single_usecase: CombinedModelPredictSingleUsecase

    def __init__(self):
        self.config = Config()
        self.combined_model = get_combined_model(self.config)

        self.combined_model_service = CombinedModelService(self.combined_model)
        self.plot_service = PlotService()

        self.combined_model_predict_single_usecase = CombinedModelPredictSingleUsecase(self.combined_model_service)
        self.combined_model_predict_multiple_usecase = CombinedModelPredictMultipleUsecase(self.combined_model_service)
        self.plot_efficiency_usecase = PlotEfficiencyUsecase(self.plot_service)

        self.server = Server(
            self.config.host,
            self.config.port,
            self.combined_model_predict_multiple_usecase,
            self.combined_model_predict_single_usecase,
            self.plot_efficiency_usecase,
        )

    def start(self):
        self.server.start()
