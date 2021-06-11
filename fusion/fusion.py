import os
import sys
import argparse
import pandas as pd
from tqdm import tqdm


def fusion_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Fusion of the files taken from NHANES website")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory", "questionnaire", "demographics", "mortality"], required=True)
    args = parser.parse_args(argvs)
    print(args)

    fusion(args.main_category)


def fusion(main_category):
    main_category_categorizer = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{os.environ.get('GOOGLE_SHEET_ID')}/gviz/tq?tqx=out:csv&sheet={main_category}", usecols=["variable", "category"]).set_index("variable")
    columns_to_take_description = {"variable_name": "variable", "data_file_name": "file_name"}
    main_category_description = pd.read_feather(f"extraction/data/variables_{main_category}.feather", columns=columns_to_take_description).rename(columns=columns_to_take_description).set_index("variable")
        
    main_category_description["category"] = main_category_categorizer["category"]
    main_category_description.drop(index=main_category_description.index[main_category_description["file_name"].isna() | main_category_description["category"].isna()], inplace=True)

    for (category, group_category) in tqdm(main_category_description.groupby(by=["category"])):
        print(category)
        min_seqn = float("inf")
        max_seqn = - float("inf")

        file_names = group_category["file_name"].drop_duplicates()
        for file_name in file_names:
            if not os.path.exists(f"extraction/data/{main_category}/{file_name}.csv"):
                print(f"extraction/data/{main_category}/{file_name}.csv")
                continue
            seqn = pd.read_csv(f"extraction/data/{main_category}/{file_name}.csv", usecols=["SEQN"])["SEQN"]
            if not seqn.is_unique:
                continue

            if seqn.min() < min_seqn:
                min_seqn = seqn.min()
            if seqn.max() > max_seqn:
                max_seqn = seqn.max()
        
        data_category = pd.DataFrame(
                None, index=pd.Index(range(int(min_seqn), int(max_seqn) + 1), name="SEQN")
            )
        for file_name in file_names:
            if not os.path.exists(f"extraction/data/{main_category}/{file_name}.csv"):
                continue
            data = pd.read_csv(f"extraction/data/{main_category}/{file_name}.csv").set_index("SEQN")
            if not data.index.is_unique:
                continue

            data.drop(columns=data.columns[~data.columns.isin(group_category.index)], inplace=True)

            data_category.loc[data.index, data.columns] = data

        columns_object = data_category.columns[data_category.dtypes == "object"]
        data_category[columns_object] = data_category[columns_object].astype(
            str, copy=False
        )

        data_category.dropna(how="all", inplace=True)
        print("shape:", data_category.shape)
        data_category.reset_index().to_feather(
            f"fusion/data/{main_category}/{category}.feather"
        )