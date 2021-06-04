import sys
import argparse
import numpy as np
import pandas as pd


def casting_examination_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Cast the examination files to dummy float vectors")
    parser.add_argument("-c", "--category", help="Name of the category", required=True)

    args = parser.parse_args(argvs)
    print(args)

    casting_examination(args.category)


def casting_examination(category):
    data_category = pd.read_feather(f"cleaning/data/examination/{category}.feather")

    columns_to_dummies = data_category.columns[data_category.dtypes == "object"]
    if len(columns_to_dummies) > 0:
        dummies = pd.get_dummies(data_category[columns_to_dummies], prefix=columns_to_dummies, drop_first=True, dtype=np.float32)
        
        data_category.drop(columns=columns_to_dummies, inplace=True)
        data_category[dummies.columns] = dummies
    
    data_category.astype(np.float32, copy=False).reset_index().to_feather(f"casting/data/examination/{category}.feather")