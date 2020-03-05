import xlrd
import sys
import numpy
import matplotlib.pyplot as plt
from typing import Tuple, List
INDEX_DATES: int = 1
INDEX_WEATHER_DEFAULT: int = 11
INDEX_HOSPITALIZATIONS: int = 13
STD_MULT_FACTOR: float = 1.0
LEN_MOVING_WINDOW: int = 7


def main():
    input = get_input()
    dates = input[0]
    weather_values = input[1]
    hospitalizations = input[2]
    peaks = get_peaks(weather_values)
    draw_graph(hospitalizations, peaks)


def get_input() -> list:
    result: list = [[], [], []]
    input_loc, INDEX_WEATHER = get_argv()
    sheet = open_sheet(input_loc)
    for i in range(1, sheet.nrows):
        result[0].append(sheet.cell(i, INDEX_DATES).value)
        result[1].append(sheet.cell(i, INDEX_WEATHER).value)
        result[2].append(sheet.cell(i, INDEX_HOSPITALIZATIONS).value)
    return result


def get_argv() -> Tuple[str, int]:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Invalid number of arguements")
        sys.exit()
    else:
        weather_col_index = int(sys.argv[2]) if len(
            sys.argv) == 3 else INDEX_WEATHER_DEFAULT
        return str(sys.argv[1]), weather_col_index


def open_sheet(location: str) -> xlrd.sheet.Sheet:
    workbook = xlrd.open_workbook(location)
    return workbook.sheet_by_index(0)


def get_mobile_mean_and_std(data: list) -> Tuple[List, List]:
    mobile_mean: list = []
    mobile_std: list = []
    for i in range(len(data) - LEN_MOVING_WINDOW):
        mobile_mean.append(numpy.mean(data[i: i + LEN_MOVING_WINDOW]))
        mobile_std.append(abs(numpy.std(data[i: i + LEN_MOVING_WINDOW])))
    return mobile_mean, mobile_std


def get_peaks(data: list) -> list:
    result: list = [0] * 7      # Initial shift of 7 positions
    means, stds = get_mobile_mean_and_std(data)
    for i in range(len(means)):
        j = i + LEN_MOVING_WINDOW - 1
        if data[i] < means[i] - STD_MULT_FACTOR * stds[i]:
            result.append(-1)   # Negative peak
        elif data[i] > means[i] + STD_MULT_FACTOR * stds[i]:
            result.append(1)    # Positive peak
        else:
            result.append(0)    # No peak
    return result


def draw_graph(hospitalizations, peaks):
    plt.plot(hospitalizations)
    plt.plot(peaks)

    plt.title("Title")
    plt.legend()
    plt.show()


main()
