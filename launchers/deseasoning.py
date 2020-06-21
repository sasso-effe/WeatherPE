from weape.argv import get_data_from_xlsx
pressure, hospitalizations = get_data_from_xlsx(11, 13)

pressure.mobile_mean(365).plot()
hospitalizations.mobile_mean(365).plot()


