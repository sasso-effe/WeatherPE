#
# This is a script to find automatically the best correlation (according to Spearman and Pearson's coefficient)
# between daily hospitalizations and weather conditions, varying some parameters
#
from weape.correlation import Correlation
from weape.argv import XLSX_PATH
import xlrd
from weape.peak_series import PeakSeries
from weape.series import Series

# Number of column in the xlsx file DO NOT MODIFY
COLUMNS = 14

# 2016 has 366 days

# Max number of past days to consider during the calculus of variation series
MAX_VARIATION_LENGTH = 6

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

# Patterns to find
PATTERNS = [(1, -1, 1), (1, 0, 1), (1, 0, -1)]


########################################################################################################################
# DO NOT MODIFY BELOW
########################################################################################################################


def __init_working_set() -> list:
    """
    Initialize the working set, taking data from xlsx file.
    :return: A list of lists. Each one represents a historical series.
    """
    working_set = []
    # Initialise an empty list for each series
    for i in range(0, COLUMNS):
        working_set.append([])
    # open the xlsx file
    sheet = xlrd.open_workbook(XLSX_PATH).sheet_by_index(0)
    # Load dates, hospitalization series and all weather values to consider
    for j in working_index + [I_DATES, I_HOSPITALIZATIONS]:
        for i in range(0, sheet.nrows):
            working_set[j].append(sheet.cell(i, j).value)
    return working_set


def __update_max(correlation: Correlation, spearman_max: list, pearson_max: list):
    """
    Update current max coefficients in terms of absolute values.
    :param correlation: The Correlation object for which to calculate the indexes
    :param spearman_max: [abs(current Spearman max value), current Spearman max correlation index]
    :param pearson_max: [abs(current Pearson max value), current Pearson max correlation index]
    """
    if abs(correlation.spearman_coefficient()[0]) > spearman_max[0]:
        spearman_max[0] = abs(correlation.spearman_coefficient()[0])
        spearman_max[1] = correlation
    if abs(correlation.pearson_coefficient()[0]) > pearson_max[0]:
        pearson_max[0] = abs(correlation.pearson_coefficient()[0])
        pearson_max[1] = correlation


def __check_variation_series(series: Series, hosp: Series, spearman_max: list, pearson_max: list):
    """
    Correlate the variation of the value of the weather conditions in the last i + 1 days with hospitalizations,
    calculate correlation indexes and update max values.
    :param series: a Series object representing the weather historical series
    :param hosp: a Series object representing the hospitalizations historical series
    :param spearman_max: [abs(current Spearman max value), current Spearman max correlation index]
    :param pearson_max: [abs(current Pearson max value), current Pearson max correlation index]
    """
    for i in range(1, MAX_VARIATION_LENGTH + 1):
        for b in [True, False]:
            cut_hosp = hosp[i:]  # remove the first i values to have lists with the same dimension
            __update_max(Correlation(series.variation_series(i, b), cut_hosp),
                         spearman_max, pearson_max)


def __check_peak_series(series: Series, hosp: Series, spearman_max: list, pearson_max: list):
    """
    Obtain the peak series and correlate it with hospitalizations shifting it by all values between 0 and
    MAX_PEAK_DELAY, calculate correlation indexes and update max values. It also check pattern series.
    :param series: a Series object representing the weather historical series
    :param hosp: a Series object representing the hospitalizations historical series
    :param spearman_max: [abs(current Spearman max value), current Spearman max correlation index]
    :param pearson_max: [abs(current Pearson max value), current Pearson max correlation index]
    """
    peaks = PeakSeries(series)
    corr = Correlation(peaks, hosp)
    for i in range(0, MAX_PEAK_DELAY + 1):
        __update_max(corr.shift(i), spearman_max, pearson_max)
        __check_pattern_series(peaks, hosp, spearman_max, pearson_max, i)


def __check_pattern_series(peaks: PeakSeries, hosp: Series, spearman_max: list, pearson_max: list, shift: int):
    """
    Obtain the pattern series for all pattern in PATTERNS, shift it and correlate it with hospitalizations.
    Then calculate correlation indexes and update max values.
    :param peaks: a PeakSeries object
    :param hosp: a Series object representing the hospitalizations historical series
    :param spearman_max: [abs(current Spearman max value), current Spearman max correlation index]
    :param pearson_max: [abs(current Pearson max value), current Pearson max correlation index]
    :param shift: length of the shift
    """
    for pattern in PATTERNS:
        pattern_series = peaks.pattern_series(pattern)
        # do not consider pattern series with no occurrences
        if not all(v == 0 for v in pattern_series.values):
            corr = Correlation(hosp[:-2], pattern_series)
            __update_max(corr.shift(shift), spearman_max, pearson_max)


def __print_results(spearman_max, pearson_max):
    """
    Print results in a easy to read way and plot graphics.
    :param spearman_max: [abs(current Spearman max value), current Spearman max correlation index]
    :param pearson_max: [abs(current Pearson max value), current Pearson max correlation index]
    """
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
    pearson_max[1].scatter()
    pearson_max[1].plot()
    spearman_max[1].scatter()
    spearman_max[1].plot()


def main():
    working_set = __init_working_set()
    spearman_max = [0.0, None]
    pearson_max = [0.0, None]
    hosp = Series(working_set[I_HOSPITALIZATIONS])
    for i in working_index:
        # create a dataset with dates, current weather condition and hospitalizations
        series = Series(working_set[i])
        # correlate raw data and, in case, update max
        __update_max(Correlation(series, hosp), spearman_max, pearson_max)
        # correlate variation series and, in case, update max
        __check_variation_series(series, hosp, spearman_max, pearson_max)
        # correlate peak and pattern series and, in case, update max
        __check_peak_series(series, hosp, spearman_max, pearson_max)
    __print_results(spearman_max, pearson_max)


main()
