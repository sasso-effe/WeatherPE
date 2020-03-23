import unittest
from weape.series import Series


class TestSeries(unittest.TestCase):
    def test_normalize(self):
        """
        In this method we are testing that normalise() create a new Series object, without modify the existing object
        """
        series = Series(["Test label", 1, 2, 3, 4, 5])
        normalized = series.normalize()
        self.assertEqual([1, 2, 3, 4, 5], series.values)
        self.assertEqual([0, 0.25, 0.5, 0.75, 1], normalized.values)
        self.assertEqual(series.label, normalized.label)

        normalized.label += " new"
        self.assertEqual("Test label", series.label)
        self.assertEqual("Test label new", normalized.label)

    def test_normalise_feature_range(self):
        series = Series(["Test label", 1, 2, 3, 4, 5])
        series = series.normalize((10, 50))
        self.assertEqual([10, 20, 30, 40, 50], series.values)

    def test_slice(self):
        series = Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "test")
        self.assertEqual(series[:].values, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(series[5:].values, [5, 6, 7, 8, 9])
        self.assertEqual(series[:3].values, [0, 1, 2])
        self.assertEqual(series[1:4].values, [1, 2, 3])
        self.assertEqual(series[2:8:2].values, [2, 4, 6])
        self.assertEqual(series[1:5].label, "test")

    def test_get_item(self):
        series = Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "test")
        self.assertEqual(series[3], 3)
        self.assertEqual(series[0], 0)
        self.assertEqual(series[-1], 9)
        self.assertEqual(series[-4], 6)

    def test_pop(self):
        series = Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "test")
        self.assertEqual(9, series.pop())
        self.assertEqual(series.values, [0, 1, 2, 3, 4, 5, 6, 7, 8])

    def test_variation_series(self):
        series = Series([0, 4, 2, 8, 3, 6, 7, 7], "test")
        self.assertEqual(series.variation_series(1).values, [4, -2, 6, -5, 3, 1, 0])
        self.assertEqual(series.variation_series(1, True).values, [4, 2, 6, 5, 3, 1, 0])
        self.assertEqual(series.variation_series(1).label, "Variation of test in 1 days")
        self.assertEqual(series.variation_series(2, False).values, [2, 4, 1, -2, 4, 1])
        self.assertEqual(series.variation_series(3, True).values, [12, 13, 14, 9, 4])
        self.assertEqual(series.variation_series(3, True).label, "Variation of test in 3 days (unsigned)")



if __name__ == '__main__':
    unittest.main()
