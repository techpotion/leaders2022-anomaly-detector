import io
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class PlotException(Exception):
    pass

class PlotExceptionUniqueDates(PlotException):
    pass

class PlotService:
    def __init__(self) -> None:
        matplotlib.use('Agg')

        self.font_path = Path("fonts/Inter-Regular.ttf")
        self.red = "red"
        self.green = "#19563A"
        self.axis_color = "#CCCCCC"
        self.red_scatter = "#F0695E"
        self.green_scatter = "#497963"
        self.grades_to_numbers = {"Отлично": 5, "Хорошо": 4, "Удовлетворительно": 3, "Плохо": 2, "Неудовлетворительно": 1}
        self.save_folder = "data/"

    def __plot_ascending_doubles(self, x, y):
        '''
        returns: list of doubles of points [[(x1, y1), (x2, y2)], [...]] for plotting 'green' line

        x is always ascending
        '''
        plotted = 0
        for i in range(1, len(y)):
            if y[i] > y[i - 1]:
                if plotted == 0:
                    plt.plot([x[i - 1], x[i]], [y[i - 1], y[i]], color=self.green, label="Положительная динамика результативности")
                    plotted += 1
                else:
                    plt.plot([x[i - 1], x[i]], [y[i - 1], y[i]], color=self.green)

    def __colour_dots(self, x, y):
        '''
        x - from 0 to 100
        '''
        plotted = 0
        for i in range(len(x)):
            if y[i] <= 60:
                if plotted == 0:
                    plt.scatter(x[i], y[i], color=self.red_scatter, marker="x", s=150, label="Дни с низкой оценкой", linewidths=2)
                    plotted += 1
                else:
                    plt.scatter(x[i], y[i], color=self.red_scatter, marker="x", s=150, linewidths=2)

    def get_plot(self, list_of_dicts, figsize_scale=1.5):
        '''
        input: list_of_dicts;
        output: svg string (or json with two svg strings - for each graph)
        '''
        figsize = (16 * figsize_scale, 9 * figsize_scale)

        df = pd.DataFrame(list_of_dicts).astype({"closure_date": "datetime64[D]"}).sort_values(by="closure_date").drop(columns=["dispetchers_number", "root_id"])
        df["closure_date"] = df["closure_date"].to_numpy(dtype="datetime64[D]")

        df_grades = df.loc[df["grade_for_service"].notna()]
        df_grades.index = [i for i in range(len(df_grades))]
        df_grades["grade_for_service"] = df_grades["grade_for_service"].replace(self.grades_to_numbers)
        dates_for_grades = df_grades["closure_date"].unique()

        if len(dates_for_grades) < 3:
            raise PlotExceptionUniqueDates("Amount of unique dates is below 3")

        mean_grades = []
        for date in dates_for_grades:
            mean_grades.append(df_grades.loc[df_grades["closure_date"] == date]["grade_for_service"].mean())


        xticks_step = 1 + len(dates_for_grades) // 50

        # plotting:
        plt.figure(figsize=figsize)
        mean_grades = np.array(mean_grades) * 20

        plt.scatter(dates_for_grades, mean_grades, color=self.green_scatter, marker="x", s=100, label="Дни с высокой оценкой", linewidths=2)
        self.__colour_dots(dates_for_grades, mean_grades)

        df_efficiency = df.loc[df["efficiency"].notna()]
        df_efficiency.index = [i for i in range(len(df_efficiency))]
        done_percent = []
        for date in dates_for_grades:
            done_percent.append(
            round(100 * len(df_efficiency.loc[(df_efficiency["closure_date"] == date) & (df_efficiency["efficiency"] == "Выполнено")]) / len(df_efficiency.loc[(df_efficiency["closure_date"] == date)]))
            )
        plt.plot(dates_for_grades, done_percent, color=self.red, label="Отрицательная динамика результативности")
        self.__plot_ascending_doubles(x=dates_for_grades, y=done_percent)

        xticks = (dates_for_grades)[::xticks_step]
        plt.xticks(xticks, rotation=75, fontsize=14)
        plt.yticks(
            list(map(lambda x: x * 20, list(self.grades_to_numbers.values()))), list(self.grades_to_numbers.keys())
            )
        plt.ylabel("Оценка", fontsize=20, color=self.axis_color, font=self.font_path)

        plt.legend(loc="best", fontsize=14)
        plt.grid(alpha=0.3)
        ax = plt.gca()
        ax2 = ax.twinx()
        ax2.spines['bottom'].set_color('white')
        ax2.spines['top'].set_color('white')
        ax2.spines['right'].set_color('white')
        ax2.spines['left'].set_color('white')
        plt.ylabel("Результативность, %", fontsize=20, color=self.axis_color, font=self.font_path)
        plt.yticks([i for i in range(0, 110, 10)])

        plt.grid(alpha=0.3)

        f = io.StringIO()
        plt.savefig(f, format = "svg")

        return f.getvalue()
