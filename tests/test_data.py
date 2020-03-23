import unittest
from weape.data import Data


class TestData(unittest.TestCase):
    @staticmethod
    def __sample_data():
        dates = ["Dates", "03/21/2020", "03/22/2020", "03/23/2020", "03/24/2020", "03/25/2020"]
        pressure = ["Pressure", 1000, 1002, 999, 1000, 1005]
        hospitalizations = ["Hospitalizations", 0, 1, 2, 0, 3]
        data = Data(dates, pressure, hospitalizations)
        return data

    def test_pop(self):
        data = self.__sample_data()
        self.assertEqual(data.pop(), ("03/25/2020", 1005, 3))
        self.assertEqual(data.dates.values, ["03/21/2020", "03/22/2020", "03/23/2020", "03/24/2020"])
        self.assertEqual(data.weather.values, [1000, 1002, 999, 1000])
        self.assertEqual(data.hospitalizations.values, [0, 1, 2, 0])

    def test_split_training_series(self):
        data = self.__sample_data()
        self.assertEqual(data.split_training_test(2)[1].hospitalizations.values, [2, 0, 3])
        self.assertEqual(data.hospitalizations.values, [0, 1])


if __name__ == '__main__':
    unittest.main()
