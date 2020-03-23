# WeatherPE
A study about correlation between Pulmonary Emboly hospitaliations and weather conditions

## How To Run

```
python -m weape/correlation_finder.py [XLSX_FILE_LOCATION]
```
If XLSX_FILE_LOCATION is not specified, weape/res/data.xlsx will be read. This could not work on OS different from Windows, so please use XLSX_FILE_LOCATION to explicitly specify the data.xlsx location using your OS's path conventions.
If you want to use a file different from data.xlsx, please mantain the same structure of the file.

If you want to costumise some parameters, read the comments in weape/correlation_finder.py
