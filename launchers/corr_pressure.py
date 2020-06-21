from weape.argv import get_data_from_xlsx
from weape.correlation import Correlation

pressure, hospitalizations = get_data_from_xlsx(11, 13)

corr = Correlation(pressure, hospitalizations)
corr.scatter()
print(corr.spearman_coefficient())
print(corr.pearson_coefficient())


hospitalizations.values.pop(0)
corr_variation = Correlation(pressure.variation_series(1), hospitalizations)
corr_variation.scatter()
print(corr_variation.spearman_coefficient())
print(corr_variation.pearson_coefficient())
