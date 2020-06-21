import unittest

from weape.peak_series import PeakSeries
from weape.series import Series


class TestPeakSeries(unittest.TestCase):
    def test_init(self):
        series = Series([0, 0, 0, 50, 0, 0], "test")
        p_series = PeakSeries(series, 3, 1.0)
        self.assertEqual(p_series.label, "Peaks of test (w=3 f=1.0)")
        self.assertEqual(p_series.values, [0, 0, 0, 1, 0, 0])

    def test_pattern_series(self):
        series = Series([0, 0, 0, 50, 0, 0], "test")
        pattern_00 = PeakSeries(series, 3, 1.0).pattern_series((0, 0))
        pattern_000 = PeakSeries(series, 3, 1.0).pattern_series((0, 0, 0))
        pattern_01 = PeakSeries(series, 3, 1.0).pattern_series((0, 1))
        self.assertEqual(pattern_00.values, [1, 1, 0, 0, 1])
        self.assertEqual(pattern_000.values, [1, 0, 0, 0])
        self.assertEqual(pattern_01.values, [0, 0, 1, 0, 0])


if __name__ == '__main__':
    unittest.main()
