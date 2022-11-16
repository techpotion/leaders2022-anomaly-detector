from usecase.service.plot_service import PlotExceptionUniqueDates, PlotService

class PlotEfficiencyUsecase:
    __plot_service: PlotService

    def __init__(self, plot_service):
        self.__plot_service = plot_service

    def execute(self, requests):
        return self.__plot_service.get_plot(requests)
