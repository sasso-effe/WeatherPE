from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt
from weape.data import Data
from weape.series import Series


class AutoCorrelation:

    def __init__(self, series: Series):
        self.series = series

    def draw(self):
        plt.acorr(self.series.values)
        plt.title("Correlogram of " + self.series.label)
        plt.show()


def auto_correlation_main():
    data = Data()
    ac = AutoCorrelation(data.weather)
    ac.draw()


auto_correlation_main()
