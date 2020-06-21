import xlrd
import sys
import numpy
import matplotlib.pyplot as plt
from typing import Tuple, List
from weape.series import Series


class PeakMaker:
    def __init__(self, series, len_moving_window=7, std_mult_factor=1.0):
        self.series = series
        self.len_moving_window = len_moving_window
        self.std_mult_factor = std_mult_factor

    def get_peaks(self) -> Series:
        values: list = self.series.values
        result: list = [0] * (self.len_moving_window - 1)  # Initial shift equal to window length
        label = "Peaks of {} (w={} f={})".format(self.series.label, self.len_moving_window,
                                                 self.std_mult_factor)
        means, stds = self._get_mobile_mean_and_std(values)
        for i in range(len(means)):
            j = i + self.len_moving_window - 1
            if values[j] < means[i] - self.std_mult_factor * stds[i]:
                result.append(-1)  # Negative peak
            elif values[j] > means[i] + self.std_mult_factor * stds[i]:
                result.append(1)  # Positive peak
            else:
                result.append(0)  # No peak
        return Series(result, label)

    def _get_mobile_mean_and_std(self, data: list):
        mobile_mean: list = []
        mobile_std: list = []
        for i in range(len(data) - self.len_moving_window + 1):
            mobile_mean.append(numpy.mean(data[i: i + self.len_moving_window]))
            mobile_std.append(abs(numpy.std(data[i: i + self.len_moving_window])))
        return mobile_mean, mobile_std
