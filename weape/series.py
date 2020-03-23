import matplotlib.pyplot as plt


class Series:
    def __init__(self, values: list, label: str = None):
        self.values = list(values)
        self.label = self.values.pop(0) if label is None else label

    def __getitem__(self, item):
        if isinstance(item, slice):
            return Series(self.values[item.start:item.stop:item.step], self.label)
        else:
            return self.values[item]

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
