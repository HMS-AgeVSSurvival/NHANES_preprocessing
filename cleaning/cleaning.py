import sys
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm


def cleaning_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Cleaning of the files after the fusion step")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory", "demographics"], required=True)
    parser.add_argument("-c", "--category", help="Name of the category", required=True)
    parser.add_argument("-n", "--number_tradeoffs", help="Number of tradeoffs to try", type=int)

    args = parser.parse_args(argvs)
    print(args)

    if args.main_category == "demographics":
        cleaning_demographics()
    else:
        cleaning(args.main_category, args.category, args.number_tradeoffs)


def optimal_function(data_frame):
    return data_frame.shape[0] * data_frame.shape[1]


def remove_nans(data_category, raw_nan_matrix, seqn_variable_trade_off):
    nan_matrix = raw_nan_matrix.copy()

    while nan_matrix.shape[0] * nan_matrix.shape[0] > 0 and nan_matrix.sum().sum() > 0:
        percentage_nan_per_variable = nan_matrix.sum() / nan_matrix.shape[0]
        percentage_nan_per_seqn = nan_matrix.T.sum() / nan_matrix.shape[1]

        max_percentage_nan_per_variable = percentage_nan_per_variable.max()
        max_percentage_nan_per_seqn = percentage_nan_per_seqn.max()

        if max_percentage_nan_per_seqn / max_percentage_nan_per_variable > seqn_variable_trade_off:
            nan_matrix.drop(index=nan_matrix.index[percentage_nan_per_seqn == max_percentage_nan_per_seqn], inplace=True)
        else:
            nan_matrix.drop(columns=nan_matrix.columns[percentage_nan_per_variable == max_percentage_nan_per_variable], inplace=True)

    if nan_matrix.shape[0] * nan_matrix.shape[0] > 0:
        cleaned_data_category = data_category.loc[nan_matrix.index, nan_matrix.columns]
        
        none_object_columns = cleaned_data_category.columns[cleaned_data_category.dtypes != "object"]
        return cleaned_data_category.drop(columns=none_object_columns[cleaned_data_category[none_object_columns].std() == 0])
    else:
        return pd.DataFrame()



def cleaning(main_category, category, number_tradeoffs):
    data_category = pd.read_feather(f"fusion/data/{main_category}/{category}.feather").set_index("SEQN")
    object_column =  data_category.columns[data_category.dtypes == "object"]
    raw_nan_matrix = data_category.isna()
    raw_nan_matrix[object_column] = (data_category[object_column] == "NA") | (data_category[object_column] == "") | (data_category[object_column] == str(np.nan)) | raw_nan_matrix[object_column]

    seqn_variable_trade_offs = np.logspace(-1, 1, num=number_tradeoffs)
    results_on_trade_off = []

    print("Initial shape:", data_category.shape)
    
    for seqn_variable_trade_off in tqdm(seqn_variable_trade_offs):
        cleaned_data_category = remove_nans(data_category, raw_nan_matrix, seqn_variable_trade_off)        
        
        print(f"Shape of the cleaned data for a trade-off of {seqn_variable_trade_off}:", cleaned_data_category.shape)

        results_on_trade_off.append(optimal_function(cleaned_data_category))

    print("Final scores:\n", results_on_trade_off)

    if sum(results_on_trade_off) > 0:
        cleaned_data_category = remove_nans(data_category, raw_nan_matrix, seqn_variable_trade_offs[np.argmax(results_on_trade_off)]) 

        cleaned_data_category.reset_index().to_feather(f"cleaning/data/{main_category}/{category}.feather")
    else:
        print("None of the preprocessing attempts worked...")       



def cleaning_demographics():
    data_category = pd.read_feather("fusion/data/demographics/demographics.feather").set_index("SEQN")

    cleaned_age_in_month = data_category["RIDAGEYR"] * 12
    cleaned_age_in_month.loc[data_category["RIDAGEEX"].notna()] = data_category.loc[data_category["RIDAGEEX"].notna(), "RIDAGEEX"]
    data_category["RIDAGEEX_extended"] = cleaned_age_in_month

    data_category.drop(columns=["RIDAGEYR", "RIDAGEEX"]).reset_index().to_feather(f"cleaning/data/demographics/demographics.feather")
