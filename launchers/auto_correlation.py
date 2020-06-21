from weape.argv import get_data_from_xlsx

pressure, hospitalizations = get_data_from_xlsx(11, 13)

pressure.draw_correlogram()
hospitalizations.draw_correlogram()
pressure.normalize().draw_correlogram()
