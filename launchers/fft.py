from weape.argv import get_data_from_txt, get_data_from_xlsx

date, pressure = get_data_from_txt(0, 3)
hospitalizations = get_data_from_xlsx(13)[0].dilute(48)
pressure.fft(t=48)
pressure.fft(cut=1, t=48)
hospitalizations.fft(t=48)
hospitalizations.fft(cut=1, t=48)
