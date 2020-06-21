import matplotlib.pyplot as plt
import numpy as np
import scipy.fft as sp


class Series:
    def __init__(self, values: list, label: str = None):
        self.values = list(values)
        self.label = self.values.pop(0) if label is None else label

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Series(self.values[item.start:item.stop:item.step], self.label)
        else:
            return self.values[item]

    def __len__(self):
        return len(self.values)

    def __str__(self):
        return ("member of Series\n" +
                "Label: " + self.label + "\n" +
                "Length: " + str(len(self)) + "\n" +
                "Values: " + str(self.values))

    def normalize(self, feature_range=(0, 1)):
        min_ = min(self.values)
        max_ = max(self.values)
        normalized = [self.label + " [NORMALIZED]"]
        for v in self.values:
            v = (v - min_) / (max_ - min_)
            v *= feature_range[1] - feature_range[0]
            v += feature_range[0]
            normalized.append(v)
        return Series(normalized)

    def draw_correlogram(self):
        plt.acorr(self.values)
        plt.xlim([-1, 11])
        plt.title("Correlogram of " + self.label)
        plt.show()

    def plot(self, x_label="Time (days)", y_label=""):
        if y_label == "":
            y_label = self.label
        plt.plot(self.values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    def pop(self):
        return self.values.pop()

    def variation_series(self, length: int, unsigned=False):
        label = "Variation of {} in {} days".format(self.label, length)
        if unsigned:
            label += " (unsigned)"
        values = list(self.values)
        for i in range(length, len(values)):
            if not unsigned:
                values[i] = self.values[i] - self.values[i - length]
            else:
                values[i] = 0
                for j in range(length):
                    values[i] += abs(self.values[i - j] - self.values[i - j - 1])
        values = values[length:]
        return Series(values, label)

    def mobile_mean(self, window: int, ws=None):
        if ws is None:
            new_label = "Mobile mean of: {}".format(self.label)
            ws = [1 / window] * window
        else:
            new_label = "Mobile mean (weights={}) of: {}".format(ws, self.label)
        assert len(ws) == window, \
            "in Series.mobile_mean(window, ws), len(ws) is {} and window is {}. They must be equal".format(
                str(len(ws), ), str(window))
        assert abs(sum(ws) - 1) < 0.01, \
            "in Series.mobile_mean(window,ws), sum(ws) is {}. it must be 1".format(sum(ws))
        mobile_mean: list = []
        for i in range(len(self.values) - window + 1):
            mean = j = 0
            for v in self.values[i: i + window]:
                mean += v * ws[j]
                j += 1
            mobile_mean.append(mean)
        return Series(mobile_mean, new_label)

    def eventuality(self):
        new_label = "{} - 1 if greater than 0".format(self.label)
        new_values = []
        for i in range(len(self.values)):
            v = 0 if self.values[i] == 0 else 1
            new_values.append(v)
        return Series(new_values, new_label)

    def dilute(self, r: int):
        new_values = []
        for i in range(len(self)):
            v = self[i] / r
            for j in range(r):
                new_values.append(v)
        return Series(new_values, self.label)

    def fft(self, cut=0, t=1):
        y: list = sp.fft(np.array(self.values))
        for i in range(cut):
            y[i] = 0
        y = list(map(abs, y))
        n = len(y)
        y = y[:n//2]
        x = np.linspace(0.0, n//(2*t), n//2)
        plt.plot(x, y, label=self.label)
        plt.title("fft {}".format("" if cut == 0 else "(with first {} elements cut)".format(cut)))
        plt.grid()
        plt.legend()
        plt.show()
