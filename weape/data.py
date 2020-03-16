import xlrd

from weape.argv import XLSX_PATH
from weape.series import Series


class Data:

    def __init__(self, index_dates=1, index_weather=11, index_hospitalizations=13):
        data = self.__get_data_from_xlsx(index_dates, index_weather, index_hospitalizations)
        self.dates = Series(data[0])
        self.weather = Series(data[1])
        self.hospitalizations = Series(data[2])

    def __get_data_from_xlsx(self, index_dates, index_weather, index_hospitalizations):
        result: list = [[], [], []]
        sheet = self.__open_sheet(XLSX_PATH)
        for i in range(0, sheet.nrows):
            result[0].append(sheet.cell(i, index_dates).value)
            result[1].append(sheet.cell(i, index_weather).value)
            result[2].append(sheet.cell(i, index_hospitalizations).value)
        return result

    @staticmethod
    def __open_sheet(location: str) -> xlrd.sheet.Sheet:
        workbook = xlrd.open_workbook(location)
        return workbook.sheet_by_index(0)
