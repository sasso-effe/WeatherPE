from typing import List
import matplotlib.pyplot as plt
from weape.data import Data
from weape.series import Series


class Correlation:
    def __init__(self, x: Series, y: Series):
        self.x = x
        self.y = y

    def draw(self):
        plt.scatter(self.x.values, self.y.values)
        plt.xlabel(self.x.label)
        plt.ylabel(self.y.label)
        plt.title("Correlation")
        plt.show()


def correlation_main():
    data = Data()
    correlation = Correlation(data.weather, data.hospitalizations)
    correlation.draw()


correlation_main()
