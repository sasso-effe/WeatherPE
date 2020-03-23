import unittest
from weape.correlation import Correlation
from weape.series import Series


class TestCorrelation(unittest.TestCase):
    @staticmethod
    def __linear_corr():
        x = Series([0, 1, 2, 3, 4], "x")
        y = Series([0, 2, 4, 6, 8], "y")
        corr = Correlation(x, y)
        return corr

    def __assert_equal_to_linear_corr(self, corr):
        linear_corr = self.__linear_corr()
        self.assertEqual(corr.x.values, linear_corr.x.values)
        self.assertEqual(corr.x.label, linear_corr.x.label)
        self.assertEqual(corr.y.values, linear_corr.y.values)
        self.assertEqual(corr.y.label, linear_corr.y.label)

    def test_get_item(self):
        corr = self.__linear_corr()
        self.assertEqual(corr[0], (0, 0))
        self.assertEqual(corr[-1], (4, 8))
        self.assertEqual(corr[1], (1, 2))

    def test_shift(self):
        corr = self.__linear_corr()
        shifted_by_0 = corr.shift(0)
        shifted_by_1 = corr.shift()
        shifted_by_2 = corr.shift(2)

        self.__assert_equal_to_linear_corr(corr)
        self.__assert_equal_to_linear_corr(shifted_by_0)

        self.assertEqual(shifted_by_1.x.values, [1, 2, 3, 4])
        self.assertEqual(shifted_by_1.x.label, "x")
        self.assertEqual(shifted_by_1.y.values, [0, 2, 4, 6])
        self.assertEqual(shifted_by_1.y.label, "y shifted by 1")

        self.assertEqual(shifted_by_2.x.values, [2, 3, 4])
        self.assertEqual(shifted_by_2.x.label, "x")
        self.assertEqual(shifted_by_2.y.values, [0, 2, 4])
        self.assertEqual(shifted_by_2.y.label, "y shifted by 2")





if __name__ == '__main__':
    unittest.main()
