from weape.argv import get_data_from_xlsx


def main():
    dates, pressure, hospitalizations = get_data_from_xlsx()
    series = hospitalizations.mobile_mean(730)
    eventuality = hospitalizations.eventuality().mobile_mean(730)
    series.plot()
    eventuality.plot()


main()
