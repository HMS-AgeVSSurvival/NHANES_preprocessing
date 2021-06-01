import sys
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm


def cleaning_examination_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Cleaning of the examination files")
    parser.add_argument("-c", "--category", help="Name of the category", required=True)

    args = parser.parse_args(argvs)
    print(args)

    cleaning_examination(args.category)


def optimal_function(data_frame):
    return data_frame.shape[0] ** 2 * data_frame.shape[1]


def remove_nans(data_category, raw_nan_matrix, seqn_variable_trade_off):
    nan_matrix = raw_nan_matrix.copy()

    while nan_matrix.sum().sum() > 0:
        percentage_nan_per_variable = nan_matrix.sum() / nan_matrix.shape[0]
        percentage_nan_per_seqn = nan_matrix.T.sum() / nan_matrix.shape[1]

        max_percentage_nan_per_variable = percentage_nan_per_variable.max()
        max_percentage_nan_per_seqn = percentage_nan_per_seqn.max()

        if max_percentage_nan_per_seqn / max_percentage_nan_per_variable > seqn_variable_trade_off:
            nan_matrix.drop(index=nan_matrix.index[percentage_nan_per_seqn == max_percentage_nan_per_seqn], inplace=True)
        else:
            nan_matrix.drop(columns=nan_matrix.columns[percentage_nan_per_variable == max_percentage_nan_per_variable], inplace=True)

    cleaned_data_category = data_category.loc[nan_matrix.index, nan_matrix.columns]
    
    return cleaned_data_category.drop(columns=cleaned_data_category.columns[cleaned_data_category.std() == 0])



def cleaning_examination(category):
    data_category = pd.read_feather(f"fusion/fusionned_data/examination/{category}.feather").set_index("SEQN")
    raw_nan_matrix = data_category.isna()

    seqn_variable_trade_offs = np.logspace(-1, 1, num=4)
    results_on_trade_off = []

    print("Initial shape:", data_category.shape)
    
    for seqn_variable_trade_off in tqdm(seqn_variable_trade_offs):
        cleaned_data_category = remove_nans(data_category, raw_nan_matrix, seqn_variable_trade_off)        
        
        print(f"Shape of the cleaned data for a trade-off of {seqn_variable_trade_off}:", cleaned_data_category.shape)

        results_on_trade_off.append(optimal_function(cleaned_data_category))

    print("Final scores:\n", results_on_trade_off)

    cleaned_data_category = remove_nans(data_category, raw_nan_matrix, seqn_variable_trade_offs[np.argmax(results_on_trade_off)]) 

    cleaned_data_category.reset_index().to_feather(f"nan_cleaning/data/examination/{category}.feather")       

