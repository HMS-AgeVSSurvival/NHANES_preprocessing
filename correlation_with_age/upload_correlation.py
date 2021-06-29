import os
import sys
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm
import scipy.stats

from correlation_with_age.utils import find_cell, update_cell


def correlation_with_age_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Compute and upload the correlations between the variables and the age from NHANES dataset")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory", "questionnaire", "demographics", "mortality"], required=True)
    args = parser.parse_args(argvs)
    print(args)

    correlation_with_age(args.main_category)


def correlation_with_age(main_category):
    age = pd.read_feather("cleaning/data/demographics/demographics.feather", columns=["SEQN", "RIDAGEEX_extended"]).set_index("SEQN")["RIDAGEEX_extended"]
    age_indexes = age.index

    correlation_col = find_cell(main_category, "age correlation").col
    p_value_col = find_cell(main_category, "p-value").col

    for category_feather in tqdm(os.listdir(f"fusion/data/{main_category}")):
        data_category = pd.read_feather(f"fusion/data/{main_category}/{category_feather}").set_index("SEQN")

        for variable in data_category.columns:
            index_notna = data_category.index[data_category[variable].notna()].intersection(age_indexes)

            if len(index_notna) <= 1:
                continue

            if data_category.loc[index_notna, variable].dtype == "object":
                dummies = pd.get_dummies(data_category.loc[index_notna, variable], prefix=variable, drop_first=False, dtype=np.float32)

                correlations, p_values = [], []
                for dummy_variable in dummies.columns:
                    correlation_dummy, p_value_dummy = scipy.stats.pearsonr(dummies.loc[index_notna, dummy_variable], age.loc[index_notna])
                    correlations.append(correlation_dummy)
                    p_values.append(p_value_dummy)

                correlation = np.max(correlations)
                p_value = p_values[np.argmax(correlations)]
            else:
                correlation, p_value = scipy.stats.pearsonr(data_category.loc[index_notna, variable], age.loc[index_notna])

            variable_row = find_cell(main_category, variable).row
            if not np.isnan(correlation):
                update_cell(main_category, variable_row, correlation_col, correlation)
            if not np.isnan(p_value):
                update_cell(main_category, variable_row, p_value_col, p_value)
