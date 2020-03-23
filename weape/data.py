from typing import Tuple

from weape.series import Series
from weape.correlation import Correlation


class Data:
    def __init__(self, dates: list, weather: list, hospitalizations: list):
        self.dates: Series = Series(dates)
        self.weather: Series = Series(weather)
        self.hospitalizations: Series = Series(hospitalizations)

    def pop(self) -> Tuple[str, bool, int]:
        """
        pop from each series
        :return: (date, weather, hospitalizations)
        """
        return self.dates.pop(), self.weather.pop(), self.hospitalizations.pop()

    def split_training_test(self, training_len: int) -> tuple:
        """
        Method to separate the training test from the testing set

        :param training_len: number of element in the training test
        :return: Tuple(Data, Data) = (training, test)
        """
        test_dates = self.__split_series(self.dates, training_len)
        test_weather = self.__split_series(self.weather, training_len)
        test_hospitalizations = self.__split_series(self.hospitalizations, training_len)

        return self, Data(test_dates, test_weather, test_hospitalizations)

    @staticmethod
    def __split_series(series: Series, size: int) -> list:
        second_part: list = series.values[size:]
        # The series passed become the first part
        series.values = series.values[:size]
        second_part.insert(0, series.label)
        return second_part

    def correlation(self) -> Correlation:
        return Correlation(self.weather, self.hospitalizations)
