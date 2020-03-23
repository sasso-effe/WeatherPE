import unittest
from weape.peak_maker import PeakMaker
from weape.series import Series


class TestPeakMaker(unittest.TestCase):
    def test_get_peaks(self):
        series = Series([0, 0, 0, 50, 0, 0], "test")
        peaks = PeakMaker(series, 3, 1.0).get_peaks()
        self.assertEqual(peaks.values, [0, 0, 0, 1, 0, 0])
        self.assertEqual(peaks.label, "Peaks of test (w=3 f=1.0)")

        series = Series([0, 0, 5, -5, 0, 5, 0], "test")
        peaks = PeakMaker(series, 3, 1.0).get_peaks()
        self.assertEqual(peaks.values, [0, 0, 1, -1, 0, 1, 0])


if __name__ == '__main__':
    unittest.main()
