from weape.correlation import Correlation
from weape.argv import get_data_from_xlsx, get_data_from_txt
from weape.series import Series


def plot_graph(series, hosp, w):
    series = series.mobile_mean(w)
    for k in range(w - 1):
        hosp.values.pop(0)
    corr = Correlation(hosp, series)
    corr.draw_means(_max=2,
                    ylabel="Average pressure variation during the same day and previous {} (mbar)".format(w - 1),
                    hlabel="Average pressure variation during a day")


hospitalizations = get_data_from_xlsx(13)[0]
pressure = get_data_from_txt(3)[0]
daily_variations = []
for i in range(0, len(pressure), 48):
    total = 0
    for j in range(i + 1, i + 47):
        total = total + abs(pressure.values[j] - pressure.values[j - 1])
    daily_variations.append(total)
var_series = Series(daily_variations, "")

var_series_test = var_series[:366]
hospitalizations_test = hospitalizations[:366]
plot_graph(var_series_test, hospitalizations_test, 4)
plot_graph(var_series, hospitalizations, 4)
