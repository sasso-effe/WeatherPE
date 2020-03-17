from weape.data import TRAINING_SET


def auto_correlation_main():
    data = TRAINING_SET
    data.weather = data.weather.normalize()
    data.weather.draw_correlogram()


auto_correlation_main()
