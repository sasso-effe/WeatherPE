import xlrd

from weape.argv import XLSX_PATH
from weape.series import Series


def _get_data_from_xlsx(index_dates, index_weather, index_hospitalizations):
    result: list = [[], [], []]
    sheet = _open_sheet(XLSX_PATH)
    for i in range(0, sheet.nrows):
        result[0].append(sheet.cell(i, index_dates).value)
        result[1].append(sheet.cell(i, index_weather).value)
        result[2].append(sheet.cell(i, index_hospitalizations).value)
    return Data(result[0], result[1], result[2])


def _open_sheet(location: str) -> xlrd.sheet.Sheet:
    workbook = xlrd.open_workbook(location)
    return workbook.sheet_by_index(0)


class Data:
    def __init__(self, dates: list, weather: list, hospitalizations: list):
        self.dates = Series(dates)
        self.weather = Series(weather)
        self.hospitalizations = Series(hospitalizations)

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


TRAINING_SET, TEST_SET = _get_data_from_xlsx(1, 11, 13).split_training_test(366)
pass
