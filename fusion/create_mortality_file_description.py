# This file creates a file "files_mortality.feather" to match with 
# the ones from the other main_category given by NHANES

import pandas as pd


FILES = ["NHANES_2007_2008.feather",
 "NHANES_2001_2002.feather",
 "NHANES_III.feather",
 "NHANES_2013_2014.feather",
 "NHANES_2011_2012.feather",
 "NHANES_2009_2010.feather",
 "NHANES_2003_2004.feather",
 "NHANES_2005_2006.feather",
 "NHANES_1999_2000.feather"]


if __name__ == "__main__":
    files_mortality = pd.DataFrame(None, columns=["data_file_description", "data_file_name"])

    files_mortality["data_file_description"] = FILES
    files_mortality["data_file_name"] = FILES

    files_mortality.to_feather("extraction/data/files_mortality.feather")