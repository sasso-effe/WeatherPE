import matplotlib.pyplot as plt
# from weape.data import TRAINING_SET
from weape.series import Series
from scipy.stats import spearmanr, pearsonr
from numpy import cov, ndarray


class Correlation:
    def __init__(self, x: Series, y: Series):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def draw(self):
        plt.scatter(self.x.values, self.y.values)
        plt.xlabel(self.x.label)
        plt.ylabel(self.y.label)
        plt.title("Correlation")
        plt.show()

    def spearman_coefficient(self) -> float:
        return spearmanr(self.x.values, self.y.values)[0]

    def cov(self) -> ndarray:
        return cov(self.x.values, self.y.values)

    def pearson_coefficient(self) -> float:
        return pearsonr(self.x.values, self.y.values)[0]

    def shift(self, length=1):
        """
        Shift y series
        :param length: shift's length
        :return: a Correlation with y series shifted by length from x series
        """
        new_x = self.x[length:]
        new_y = self.y[:-length] if length != 0 else self.y[:]
        if length != 0:
            new_y.label += " shifted by {}".format(length)
        return Correlation(new_x, new_y)


def correlation_main():
    data = TRAINING_SET
    delta_pressure = ["PRESSURE MSL VARIATION (mbar)"]
    for i in range(1, len(data.weather.values)):
        delta_pressure.append((data.weather.values[i] - data.weather.values[i - 1]))
    delta_pressure = Series(delta_pressure)
    del data.hospitalizations.values[0]
    correlation = Correlation(delta_pressure, data.hospitalizations)
    correlation.draw()
    print("Spearman's coefficient: " + str(correlation.spearman_coefficient()) + "\n"
          + "Pearson's coefficient: " + str(correlation.pearson_coefficient()) + "\n"
          + "Covariance: " + str(correlation.cov()) + "\n")

# correlation_main()
