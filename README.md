# WeatherPE
A study about correlation between Pulmonary Emboly hospitaliations and weather conditions

## How To Run

```
python -m weape/correlation.py XLSX_FILE_LOCATION
```
```
python -m weape/auto_correlation.py XLSX_FILE_LOCATION
```

Dates must stay on column 1 (B).
Weather values must stay on column 11 (L).
Hospitalizations number must stay on column 13 (N).
The first row must contains columns' labels
