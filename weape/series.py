import matplotlib.pyplot as plt


class Series:
    def __init__(self, values: list):
        self.label: str = values.pop(0)
        self.values: list = values

    def normalize(self, feature_range=(0, 1)):
        min_ = min(self.values)
        max_ = max(self.values)
        normalized = [self.label]
        for v in self.values:
            v = (v - min_) / (max_ - min_)
            v *= feature_range[1] - feature_range[0]
            v += feature_range[0]
            normalized.append(v)
        return Series(normalized)

    def draw_correlogram(self):
        plt.acorr(self.values)
        plt.title("Correlogram of " + self.label)
        plt.show()
