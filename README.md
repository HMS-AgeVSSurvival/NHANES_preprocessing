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

The file [extraction.Rmd](./extraction/extraction.Rmd) scrape [NHANES website](https://www.cdc.gov/nchs/nhanes/index.htm) and store the files in *./extraction/data/*.

Some files are only available with the format *.sas7dbat* so you need to convert them to the *.csv* format with the file [sas7bdat_to_csv.Rmd](./extraction/sas7bdat_to_csv.Rmd).

For the mortality dataset, files have been download from the [ftp server](https://ftp.cdc.gov/pub/health_statistics/nchs/datalinkage/linked_mortality/) of the 
Centers for Disease Control. Then, they have been processed using the file [mortality.Rmd](./extraction/mortality.Rmd).

## [II Fusion](./fusion)
[Code in Python]\
Start by installing the Python package thanks the the [setup.py](./setup.py) file:
```Python
pip install -e .[dev]
```
This stage has the goal to fusion the different files, given by the previous step, into one single file, representing a category. The way the categories are formed is shown in the google sheet [variable_categorizer](https://docs.google.com/spreadsheets/d/1wyfNAD_SgmIlKXK-2QFcBu7eH4xPJKbWe4PLOIIlriI/edit#gid=303839131). This google sheet reports the name of the variables with their description and the category they have been assigned to, along with other information.


## [III Cleaning](./cleaning)
[Code in Python]\
This stage cleans the files obtained in the previous step by removing the nans. After removing the nans, the columns with a null standard deviation are removed. Create the age of the participants for *demographics*. Create a variable called __survival_type__ for *mortality* that tells the cause of death (cvd, cancer, other or alive).


## [IV Casting](./casting)
[Code in Python]\
This stage casts the files obtained in the previous step by casting the types of the variables to float32. When a categorical variable is encountered, the variable is converted in dummy vectors.


## [V Merge](./merge)
[Code in Python]\
This stage merges the files obtained in the previous step with the demographics files and the mortality data. It also adds the description of the variables to their name.
