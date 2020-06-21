from weape.argv import get_data_from_xlsx
from weape.peak_series import PeakSeries
from weape.correlation import Correlation


def main():
    pressure, hospitalizations = get_data_from_xlsx(11, 13)
    peaks = PeakSeries(pressure)
    for pattern in [(1, -1, 1), (1, 0, 1), (1, 0, -1)]:
        pattern_series = peaks.pattern_series(pattern)
        corr = Correlation(hospitalizations[:-2], pattern_series)
        corr.plot()
        print("{} {}".format(corr.pearson_coefficient(), corr.spearman_coefficient()))


main()
