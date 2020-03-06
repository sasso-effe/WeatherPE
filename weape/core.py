import xlrd
import sys
import numpy
import matplotlib.pyplot as plt
from typing import Tuple, List
from peak_maker import PeakMaker
INDEX_DATES: int = 1
INDEX_WEATHER_DEFAULT: int = 11
INDEX_HOSPITALIZATIONS: int = 13
STD_MULT_FACTOR: float = 1.0
LEN_MOVING_WINDOW: int = 7


def main():
    input = get_input()
    dates: List[str] = input[0]
    weather_values: List[float] = input[1]
    hospitalizations: List[int] = input[2]
    dataset = PeakMaker(dates, weather_values, hospitalizations)
    draw_graph(dataset.hospitalizations, dataset.get_peaks())


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


def draw_graph(hospitalizations, peaks):
    plt.plot(hospitalizations)
    plt.plot(peaks)

    plt.title("Title")
    plt.legend()
    plt.show()


main()
