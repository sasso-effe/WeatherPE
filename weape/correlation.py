import matplotlib.pyplot as plt
from weape.series import Series
from scipy.stats import spearmanr, pearsonr
from numpy import cov, ndarray, mean


class Correlation:
    def __init__(self, x: Series, y: Series):
        self.x = x
        self.y = y

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Correlation(self.x[item.start:item.stop:item.step], self.y[item.start:item.stop:item.step])
        else:
            return self.x[item], self.y[item]

    def scatter(self):
        plt.scatter(self.x.values, self.y.values)
        plt.xlabel(self.x.label)
        plt.ylabel(self.y.label)
        plt.title("Correlation")
        plt.show()

    def plot(self):
        plt.plot(self.x.values, label=self.x.label)
        plt.plot(self.y.values, label=self.y.label)
        plt.xlabel("Time (days)")
        plt.legend()
        plt.show()

    def draw_means(self, _max: int = None, xlabel: str = None, ylabel: str = None, hlabel: str = None):
        if _max is None:
            _max = int(max(self.x))
            max_label = str(_max)
        else:
            max_label = str(_max) + "+"
        sum_length = [[0, 0]]
        for i in range(_max):
            sum_length.append([0, 0])
        for i in range(len(self.x)):
            _x = int(self.x[i])
            _x = _max if _x >= _max else _x
            _y = self.y[i]
            sum_length[_x][0] += _y
            sum_length[_x][1] += 1
        means = []
        for s, l in sum_length:
            means.append(s / l)
        for i in range(len(means)):
            plt.plot(i, means[i], 'bo', markersize=int(sum_length[i][1] / len(self.x) * 100))
        plt.plot(means, 'b')
        xlabel = self.x.label if xlabel is None else xlabel
        ylabel = self.y.label if ylabel is None else ylabel
        hlabel = "Mean of {}".format(ylabel) if hlabel is None else hlabel
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        xticks = []
        for i in range(_max):
            xticks.append(str(i))
        xticks.append(max_label)
        plt.xticks(range(_max + 1), xticks)
        _mean = float(mean(self.y.values))
        ymax = means[_max]
        plt.hlines(_mean, 0, _max, linestyles="dashed",
                   label=hlabel)
        plt.annotate(str(round(_mean, 3)), xy=(_max - 0.5, _mean * 1.0005), xycoords='data')
        plt.vlines(_max, _mean, ymax, linestyles="dashed", colors="r",
                   label="Distance = {} (+{}%)".format(str(round(ymax - _mean, 3)),
                                                       str(round((ymax - _mean) / _mean * 100, 2))))
        plt.legend()
        plt.show()

    def spearman_coefficient(self) -> tuple:
        return spearmanr(self.x.values, self.y.values)

    def cov(self) -> ndarray:
        return cov(self.x.values, self.y.values)

    def pearson_coefficient(self) -> tuple:
        return pearsonr(self.x.values, self.y.values)

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

    def normalize(self, feature_range=(0, 1)):
        self.x = self.x.normalize(feature_range)
        self.y = self.y.normalize(feature_range)
        return self

