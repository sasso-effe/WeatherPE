import xlrd
import sys
import numpy
from typing import Tuple, List


def main():
    input = get_input()
    dates = input[0]
    pressure = input[1]
    hospitalizations = input[2]
    peaks = get_peaks(pressure)


def get_input() -> list:
    result: list = [[], [], []]
    input_loc = get_input_loc()
    sheet = open_sheet(input_loc)
    for i in range(sheet.nrows):
        for j in range(len(result)):
            result[j].append(sheet.cell(i, j).value)
    return result


def get_input_loc() -> str:
    if len(sys.argv) != 2:
        print("Invalid number of arguements")
        sys.exit()
    else:
        return str(sys.argv[1])


def open_sheet(location: str) -> xlrd.sheet.Sheet:
    workbook = xlrd.open_workbook(location)
    return workbook.sheet_by_index(0)


def get_mobile_mean_and_std(data: list) -> Tuple[List, List]:
    WINDOW = 7
    mobile_mean: list = []
    mobile_std: list = []
    for i in range(len(data) - WINDOW):
        mobile_mean.append(numpy.mean(data[i: i + WINDOW]))
        mobile_std.append(abs(numpy.std(data[i: i + WINDOW])))
    return mobile_mean, mobile_std


def get_peaks(data: list) -> list:
    result: list = []
    means, stds = get_mobile_mean_and_std(data)
    for i in range(len(means)):
        if data[i] < means[i] - stds[i]:
            result.append(-1)   # Negative peak
        elif data[i] > means[i] + stds[i]:
            result.append(1)    # Positive peak
        else:
            result.append(0)    # No peak
    return result


main()
