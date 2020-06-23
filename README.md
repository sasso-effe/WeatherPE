# WeatherPE
weape package contains a framework to be used to represent and analyse historical series; launchers folders contains some script used to generate graphics for a study about correlation between Pulmonary Emboly hospitaliations and weather conditions.

## Data sources
Data in lamma.txt are provided by:

Consorzio LAMMA.
Laboratorio di Monitoraggio e Modellistica Ambientale per lo sviluppo sostenibile - 
Laboratory for Meteorology and Environmental Modelling

Any copy or use of the data must always quote the source of the data in full.

## How To Run
Each script in the launchers folder can be run by:

```
python -m launchers.SCRIPT_NAME.py [XLSX_FILE_LOCATION]
```
If XLSX_FILE_LOCATION is not specified, weape/res/data.xlsx will be read. This could not work on OS different from Windows, so please use XLSX_FILE_LOCATION to explicitly specify the data.xlsx location using your OS's path conventions.
If you want to use a file different from data.xlsx, please mantain the same structure of the file.

The script correlation_finder.py allows to costumise some parameters, read the comments in the script to know how to do it.
