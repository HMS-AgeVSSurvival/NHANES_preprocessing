import os
import sys
import argparse
import pandas as pd
from tqdm import tqdm
import scipy.stats

from correlation_with_age.utils import get_col_values, find_cell, update_cell


def correlation_with_age_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Compute and upload the correlations between the variables and the age from NHANES dataset")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory", "questionnaire", "demographics", "mortality"], required=True)
    args = parser.parse_args(argvs)
    print(args)

    correlation_with_age(args.main_category)


def correlation_with_age(main_category):
    age = pd.read_feather("cleaning/data/demographics/demographics.feather", columns=["SEQN", "RIDAGEEX_extended"]).set_index("SEQN")["RIDAGEEX_extended"]

    correlation_col = find_cell(main_category, "age correlation").col
    p_value_col = find_cell(main_category, "p-value").col

    variables = get_col_values(main_category, find_cell(main_category, "variable").col)[1:]            
    categories = get_col_values(main_category, find_cell(main_category, "category").col)[1:]            
    variables_categorized = pd.DataFrame.from_dict({"variable": variables, "category": categories})
    
    for (category, group_category) in tqdm(variables_categorized.groupby(by=["category"])):
        path_file = f"fusion/data/{main_category}/{category.replace('/', '_or_').replace(' ', '__').replace('.', '--')}.feather"

        if not os.path.exists(path_file):  # The file only contains variables that are not processed
            continue
        data_file = pd.read_feather(path_file).set_index("SEQN")

        for variable in group_category["variable"]:
            if variable not in data_file.columns:  # The file entails non unique SEQN
                continue

            index_notna = data_file.index[data_file[variable].notna()]

            # If the variable is not categorical and the number of participants is higher than one
            if data_file.loc[index_notna, variable].dtype != "object" and len(index_notna) > 1 :
                correlation, p_value = scipy.stats.pearsonr(data_file.loc[index_notna, variable], age.loc[index_notna])

                variable_row = find_cell(main_category, variable).row
                update_cell(main_category, variable_row, correlation_col, correlation)
                update_cell(main_category, variable_row, p_value_col, p_value)