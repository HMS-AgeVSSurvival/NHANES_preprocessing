# This file creates a file "variables_mortality.feather" to match with
# the ones from the other main_category given by NHANES

import pandas as pd


FILES = [
    "NHANES_2007_2008",
    "NHANES_2001_2002",
    "NHANES_III",
    "NHANES_2013_2014",
    "NHANES_2011_2012",
    "NHANES_2009_2010",
    "NHANES_2003_2004",
    "NHANES_2005_2006",
    "NHANES_1999_2000",
]

VARIABLES = ["mortstat", "ucod_leading", "permth_int", "permth_exm"]


if __name__ == "__main__":
    files_mortality = pd.DataFrame(None, columns=["variable_name", "data_file_name"])

    variable_names = []
    data_file_names = []
    for file in FILES:
        for variable in VARIABLES:
            variable_names.append(variable)
            data_file_names.append(file)

    files_mortality["variable_name"] = variable_names
    files_mortality["data_file_name"] = data_file_names
    files_mortality.reset_index(drop=True).to_feather(
        "extraction/data/variables_mortality.feather"
    )
