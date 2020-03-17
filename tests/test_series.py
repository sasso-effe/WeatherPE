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


if __name__ == '__main__':
    unittest.main()
