import os
import sys
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm

from utils.google_sheets_sdk import get_col_values


def fusion_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Fusion of the files taken from NHANES website")
    parser.add_argument(
        "-mc",
        "--main_category",
        help="Name of the main category",
        choices=[
            "examination",
            "laboratory",
            "questionnaire",
            "demographics",
            "mortality",
        ],
        required=True,
    )
    args = parser.parse_args(argvs)
    print(args)

    fusion(args.main_category)


def fusion(main_category):
    categorized_variable = pd.DataFrame(
        np.array(
            [
                get_col_values(main_category, "category")[1:],
                get_col_values(main_category, "to remove")[1:],
            ]
        ).T,
        columns=["category", "to remove"],
        index=get_col_values(main_category, "variable")[1:],
    )

    columns_to_take_description = {
        "variable_name": "variable",
        "data_file_name": "file_name",
    }
    splitter = (
        pd.read_feather(
            f"extraction/data/variables_{main_category}.feather",
            columns=columns_to_take_description,
        )
        .rename(columns=columns_to_take_description)
        .set_index("variable")
    )

    splitter["category"] = categorized_variable["category"]
    splitter.drop(
        index=splitter.index[
            splitter["file_name"].isna()
            | splitter["category"].isna()
            | splitter.index.isin(
                categorized_variable.index[categorized_variable["to remove"] == "TRUE"]
            )
        ],
        inplace=True,
    )

    for (category, group_category) in tqdm(splitter.groupby(by=["category"])):
        print(category)
        min_seqn = float("inf")
        max_seqn = -float("inf")

        no_file = True

        file_names = group_category["file_name"].drop_duplicates()
        for file_name in file_names:
            if not os.path.exists(f"extraction/data/{main_category}/{file_name}.csv"):
                continue
            seqn = pd.read_csv(f"extraction/data/{main_category}/{file_name}.csv")
            if "SEQN" not in seqn.columns or not seqn["SEQN"].is_unique:
                continue

            no_file = False
            if seqn["SEQN"].min() < min_seqn:
                min_seqn = seqn["SEQN"].min()
            if seqn["SEQN"].max() > max_seqn:
                max_seqn = seqn["SEQN"].max()

        if no_file:
            print("No file for this category \n\n")
            continue

        data_category = pd.DataFrame(
            None, index=pd.Index(range(int(min_seqn), int(max_seqn) + 1), name="SEQN")
        )

        for file_name in file_names:
            if not os.path.exists(f"extraction/data/{main_category}/{file_name}.csv"):
                continue
            data = pd.read_csv(f"extraction/data/{main_category}/{file_name}.csv")
            if "SEQN" not in data.columns or not data["SEQN"].is_unique:
                continue

            data.set_index("SEQN", inplace=True)

            data.drop(
                columns=data.columns[~data.columns.isin(group_category.index)],
                inplace=True,
            )

            data_category.loc[data.index, data.columns] = data

        # Need to remove object dtype to store in feather format
        columns_object = data_category.columns[data_category.dtypes == "object"]
        data_category[columns_object] = data_category[columns_object].astype(
            str, copy=False
        )

        data_category.dropna(axis="index", how="all", inplace=True)
        print("Shape: ", data_category.shape)
        data_category.reset_index().to_feather(
            f"fusion/data/{main_category}/{category.replace('/', '_or_').replace(' ', '__').replace('.', '--')}.feather"
        )
