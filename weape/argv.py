import sys
from weape.data import Data
import xlrd
import os.path


def __get_argv() -> str:
    if len(sys.argv) > 3:
        print("Invalid number of arguments")
        sys.exit()
    elif len(sys.argv) == 1:
        full_path = os.path.abspath('./res/data.xlsx')
        return full_path
    else:
        return str(sys.argv[1])


def get_data_from_xlsx(index_dates, index_weather, index_hospitalizations) -> Data:
    result: list = [[], [], []]
    sheet = __open_sheet(XLSX_PATH)
    for i in range(0, sheet.nrows):
        result[0].append(sheet.cell(i, index_dates).value)
        result[1].append(sheet.cell(i, index_weather).value)
        result[2].append(sheet.cell(i, index_hospitalizations).value)
    return Data(result[0], result[1], result[2])


def __open_sheet(location: str) -> xlrd.sheet.Sheet:
    workbook = xlrd.open_workbook(location)
    return workbook.sheet_by_index(0)


XLSX_PATH: str = __get_argv()
