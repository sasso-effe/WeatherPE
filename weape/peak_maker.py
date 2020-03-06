import xlrd
import sys
import numpy
import matplotlib.pyplot as plt
from typing import Tuple, List


class PeakMaker:
    def __init__(self, dates: List[str], weather_values: List[float], hospitalizations: List[int],
                 len_moving_window: int = 7, std_mult_factor: float = 1.0):
        self.dates = dates
        self.weather_values = weather_values
        self.hospitalizations = hospitalizations
        self.len_moving_window = len_moving_window
        self.std_mult_factor = std_mult_factor

    def get_peaks(self) -> list:
        result: list = [0] * (self.len_moving_window - 1)  # Initial shift equal to window length
        means, stds = self._get_mobile_mean_and_std(self.weather_values)
        for i in range(len(means)):
            j = i + self.len_moving_window - 1
            if self.weather_values[j] < means[i] - self.std_mult_factor * stds[i]:
                result.append(-1)  # Negative peak
            elif self.weather_values[j] > means[i] + self.std_mult_factor * stds[i]:
                result.append(1)  # Positive peak
            else:
                result.append(0)  # No peak
        return result

    def _get_mobile_mean_and_std(self, data: list) -> Tuple[List, List]:
        mobile_mean: list = []
        mobile_std: list = []
        for i in range(len(data) - self.len_moving_window + 1):
            mobile_mean.append(numpy.mean(data[i: i + self.len_moving_window]))
            mobile_std.append(abs(numpy.std(data[i: i + self.len_moving_window])))
        return mobile_mean, mobile_std
