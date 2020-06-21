from weape.argv import get_data_from_xlsx

pressure, hospitalizations = get_data_from_xlsx(11, 13)

pressure.plot()
hospitalizations.plot()
