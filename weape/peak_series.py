from weape.peak_maker import PeakMaker
from weape.series import Series


class PeakSeries(Series):
    def __init__(self, series, len_moving_window=7, std_mult_factor=1.0):
        p_maker = PeakMaker(series, len_moving_window, std_mult_factor)
        peak_series = p_maker.get_peaks()
        super().__init__(peak_series.values, peak_series.label)

    def pattern_series(self, pattern: tuple):
        window = len(pattern)
        pattern_label = "{} - Pattern {}".format(self.label, pattern)
        pattern_values = []
        for i in range(len(self) - window + 1):
            sub_list = tuple(self.values[i:i+window])
            v = 1 if sub_list == pattern else 0
            pattern_values.append(v)
        return Series(pattern_values, pattern_label)

