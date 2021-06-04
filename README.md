# NHANES_preprocessing
Preprocessing of NHANES into different categories.

The main categories that we are going to leverage are:
- demographics
- laboratory
- examination


## [I Extraction](./extraction)
[Code in R]\
Start by restoring the R environment thanks to the [renv.lock](./renv.lock) file :
```R
renv::restore()
```
If you don't already have the package renv installed. Please install it following the [docs](https://github.com/rstudio/renv).

The file [./extraction/extraction.Rmd] scrape [NHANES website](https://www.cdc.gov/nchs/nhanes/index.htm) and store the files in *./extraction/data/*.

Some files are only available with the format *.sas7dbat* so you need to convert them to the *.csv* format with the [sas7bdat_to_csv](./extraction/sas7bdat_to_csv.Rmd).


## [II Fusion](./fusion)
[Code in Python]\
Start by installing the Python package thanks the the [setup.py](./setup.py) file:
```Python
pip install -e .[dev]
```
This stage has the goal to fusion the different files, given by the previous step, into one single file, representing a category. The way the categories are formed is shown in the file [split_*main_category*](./fusion/splitting/split_examination.json)

## [III Cleaning](./cleaning)
[Code in Python]\
This stage cleans the files obtained in the previous step by removing the nans.

## [IV Casting](./casting)
[Code in Python]\
This stage casts the files obtained in the previous step by casting the types of the variables to float32. When a categorical variable in encountered, the variable is converted in dummy vectors.

## [V Merge demographics](./merge_demographics)
[Code in Python]\
This stage merges the files obtained in the previous step with the demographics files. It also adds the description of the variables to their name.
