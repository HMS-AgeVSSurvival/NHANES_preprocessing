import sys
import argparse
import numpy as np
import pandas as pd


def casting_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Cast the files from the cleaning steps to dummy float vectors")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory", "demographics"], required=True)
    parser.add_argument("-c", "--category", help="Name of the category", required=True)

    args = parser.parse_args(argvs)
    print(args)

    if args.main_category == "demographics":
        casting_demographics()
    else:
        casting(args.main_category, args.category)


def casting(main_category, category):
    data_category = pd.read_feather(f"cleaning/data/{main_category}/{category}.feather").set_index("SEQN")

    columns_to_dummies = data_category.columns[data_category.dtypes == "object"]
    if len(columns_to_dummies) > 0:
        dummies = pd.get_dummies(data_category[columns_to_dummies], prefix=columns_to_dummies, drop_first=True, dtype=np.float32)
        
        data_category.drop(columns=columns_to_dummies, inplace=True)
        data_category[dummies.columns] = dummies
    
    data_category.astype(np.float32, copy=False).reset_index().to_feather(f"casting/data/{main_category}/{category}.feather")


def casting_demographics():
    data_category = pd.read_feather("cleaning/data/demographics/demographics.feather").set_index("SEQN")

    data_category["RIDRETH1"] = data_category["RIDRETH1"].map(
        {
            1: "Mexican American",
            2: "Other Hispanic",
            3: "Non-Hispanic White",
            4: "Non-Hispanic Black",
            5: "Other Race - Including Multi-Racial",
        }
    )

    dummies = pd.get_dummies(data_category["RIDRETH1"], prefix="RIDRETH1", drop_first=True, dtype=np.float32)
    data_category.drop(columns="RIDRETH1", inplace=True)
    data_category[dummies.columns] = dummies

    data_category.astype(np.float32, copy=False).reset_index().to_feather(f"casting/data/demographics/demographics.feather")

