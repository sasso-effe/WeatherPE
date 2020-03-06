import unittest
from weape.peak_maker import PeakMaker


class TestPeakMaker(unittest.TestCase):
    def test_get_peaks(self):
        p_maker = PeakMaker(dates=[], weather_values=[0, 0, 0, 50, 0, 0], hospitalizations=[], len_moving_window=3,
                            std_mult_factor=1.0)
        self.assertEqual([0, 0, 0, 1, 0, 0], p_maker.get_peaks())

        p_maker.weather_values = [0, 0, 5, -5, 0, 5, 0]
        self.assertEqual([0, 0, 1, -1, 0, 1, 0], p_maker.get_peaks())


if __name__ == '__main__':
    unittest.main()
