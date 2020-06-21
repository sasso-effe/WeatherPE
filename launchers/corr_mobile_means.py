from weape.argv import get_data_from_xlsx
from weape.correlation import Correlation


pressure, hospitalizations = get_data_from_xlsx(11, 13)
for w in 7, 30, 120, 365:
    corr = Correlation(pressure.mobile_mean(w), hospitalizations.mobile_mean(w))
    corr.scatter()
    print("w = {}".format(w))
    sp = corr.spearman_coefficient()
    print("\tSpearman: corr = {}, p = {}".format(sp[0], sp[1]))
    pe = corr.pearson_coefficient()
    print("\tPearson: corr = {}, p = {}".format(pe[0], pe[1]))
