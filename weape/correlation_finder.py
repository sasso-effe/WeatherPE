#
# This is a script to find automatically the best correlation (according to Spearman and Pearson's coefficient)
# between daily hospitalizations and weather conditions, varying some parameters
#
from weape.correlation import Correlation
from weape.data import Data
from weape.argv import XLSX_PATH
import xlrd
from weape.peak_maker import PeakMaker

# Number of column in the xlsx file DO NOT MODIFY
COLUMNS = 14

# 2016 has 366 days
TESTING_SET_LENGTH = 366

# Max number of past days to consider during the calculus of variation series
MAX_VARIATION_LENGTH = 3

# Max delay of peaks' influence on hospitalizations to consider
MAX_PEAK_DELAY = 3

# List of indexes DO NOT MODIFY
(
    I_PLACE,  # 0
    I_DATES,  # 1
    I_TEMP_AVG,  # 2
    I_TEMP_MIN,  # 3
    I_TEMP_MAX,  # 4
    I_DEW_POINT,  # 5
    I_HUMIDITY,  # 6
    I_VISIBILITY,  # 7
    I_WIND_AVG,  # 8
    I_WIND_MAX,  # 9
    I_WIND_GUST,  # 10
    I_PRESSURE,  # 11
    I_PHENOMENONS,  # 12
    I_HOSPITALIZATIONS  # 13
) = range(0, COLUMNS)

# Values to consider
working_index = [I_TEMP_AVG, I_TEMP_MIN, I_TEMP_MAX, I_WIND_AVG, I_WIND_MAX, I_PRESSURE]


########################################################################################################################
# DO NOT MODIFY BELOW
########################################################################################################################


def __init_working_set() -> list:
    working_set = []
    for i in range(0, COLUMNS):
        working_set.append([])
    sheet = xlrd.open_workbook(XLSX_PATH).sheet_by_index(0)
    for j in working_index + [I_DATES, I_HOSPITALIZATIONS]:
        for i in range(0, min(sheet.nrows, TESTING_SET_LENGTH)):
            working_set[j].append(sheet.cell(i, j).value)
    return working_set


def __update_max(correlation: Correlation, spearman_max: list, pearson_max: list):
    if abs(correlation.spearman_coefficient()) > spearman_max[0]:
        spearman_max[0] = abs(correlation.spearman_coefficient())
        spearman_max[1] = correlation
    if abs(correlation.pearson_coefficient()) > pearson_max[0]:
        pearson_max[0] = abs(correlation.pearson_coefficient())
        pearson_max[1] = correlation


def __check_variation_series(data: Data, spearman_max: list, pearson_max: list):
    # correlate the variation of the value of the weather conditions in the last i+1 days with hospitalizations
    for i in range(1, MAX_VARIATION_LENGTH + 1):
        for b in [True, False]:
            __update_max(Correlation(data.weather.variation_series(i, b),
                                     # remove the first i values to have lists with the same dimension
                                     data.hospitalizations[i:]),
                         spearman_max,
                         pearson_max)


def __check_peak_series(data: Data, spearman_max: list, pearson_max: list):
    peaks = PeakMaker(data.weather).get_peaks()
    corr = Correlation(peaks, data.hospitalizations)
    for i in range(0, MAX_PEAK_DELAY + 1):
        __update_max(corr.shift(i), spearman_max, pearson_max)


def __print_results(spearman_max, pearson_max):
    print(
        """
Correlation with max Pearson: {}
    Pearson: {} Spearman: {}
Correlation with max Spearman: {}
    Pearson: {} Spearman: {}
        """.format(pearson_max[1].x.label, pearson_max[1].pearson_coefficient(), pearson_max[1].spearman_coefficient(),
                   spearman_max[1].x.label, spearman_max[1].pearson_coefficient(),
                   spearman_max[1].spearman_coefficient())
    )
    pearson_max[1].draw()
    spearman_max[1].draw()


def main():
    working_set = __init_working_set()
    spearman_max = [0.0, None]
    pearson_max = [0.0, None]
    for i in working_index:
        # create a dataset with dates, current weather condition and hospitalizations
        # and work only on the training subset (first year)
        data = Data(working_set[I_DATES], working_set[i], working_set[I_HOSPITALIZATIONS]).split_training_test(366)[0]
        # correlate raw data and, in case, update max
        __update_max(data.correlation(), spearman_max, pearson_max)
        __check_variation_series(data, spearman_max, pearson_max)
        __check_peak_series(data, spearman_max, pearson_max)
    __print_results(spearman_max, pearson_max)


main()
