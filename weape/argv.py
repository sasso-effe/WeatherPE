import sys
import xlrd
import os.path

from weape.series import Series


def __get_argv() -> tuple:
    if len(sys.argv) not in [1, 3]:
        print("Invalid number of arguments")
        sys.exit()
    elif len(sys.argv) == 1:
        xlsx_path = os.path.abspath('./res/data.xlsx')
        txt_path = os.path.abspath('./res/lamma.txt')
        return xlsx_path, txt_path
    else:
        xlsx_path = sys.argv[1]
        txt_path = sys.argv[1]
        return xlsx_path, txt_path


def get_data_from_xlsx(*indexes) -> tuple:
    values = [[] for i in range(len(indexes))]
    sheet = __open_sheet(XLSX_PATH)
    for row in range(0, sheet.nrows):
        for i, column in enumerate(indexes):
            values[i].append(sheet.cell(row, column).value)
    result = map(lambda x: Series(x), values)
    return tuple(result)


def __open_sheet(location: str) -> xlrd.sheet.Sheet:
    workbook = xlrd.open_workbook(location)
    return workbook.sheet_by_index(0)


def get_data_from_txt(*indexes) -> tuple:
    txt = open(TXT_PATH, 'r')
    values = [[] for i in range(len(indexes))]
    for line in txt:
        splitted_line = line.split('\t')
        for i, j in enumerate(indexes):
            try:
                v = float(splitted_line[j])
                # n\a value in the file are represented with value -999.
                # Replace it with 1000 that's a less anomalous value
                if abs(v + 999) < 0.1:
                    v = 1000
            except ValueError:
                v = splitted_line[j]
            values[i].append(v)
    result = map(lambda x: Series(x), values)
    return tuple(result)


XLSX_PATH, TXT_PATH = __get_argv()
