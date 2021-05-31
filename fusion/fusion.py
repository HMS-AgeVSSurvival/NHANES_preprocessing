import sys
import argparse
import pandas as pd
from tqdm import tqdm
import json


def fusion_examination_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Fusion of the examination files")
    parser.add_argument("-c", "--category", help="Name of the category", required=True)
    
    args = parser.parse_args(argvs)
    print(args)

    fusion_examination(args.category)


def fusion_examination(category):
    with open("fusion/splitting/split_examination.json") as json_file:
        splitting_examination = json.load(json_file)
    data_file_description = splitting_examination[category]

    files_examination = pd.read_feather("extraction/raw_data/files_examination.feather")
    # Drop PAXRAW_D: cannot be downloaded properly
    # Drop P_BPXO, P_BMX, P_OHXDEN and P_OHXREF: files not accessible and convered by others.
    files_examination.drop(index=files_examination.index[files_examination["data_file_name"].isna() | files_examination["data_file_name"].isin(["PAXRAW_D", "P_BPXO", "P_BMX", "P_OHXDEN", "P_OHXREF"])], inplace=True)
    files_examination.set_index("data_file_description", inplace=True)


    file_names = files_examination.loc[data_file_description, "data_file_name"].drop_duplicates()
    
    min_seqn = float("inf")
    max_seqn = -float("inf")
    for file_name in tqdm(file_names):
        raw_data = pd.read_csv("extraction/raw_data/examination/" + file_name + ".csv")
        if "SEQN" not in raw_data.columns:
            continue

        if raw_data["SEQN"].min() < min_seqn:
            min_seqn = raw_data["SEQN"].min()
        if max_seqn < raw_data["SEQN"].max():
            max_seqn = raw_data["SEQN"].max()
    
    data_category = pd.DataFrame(None, index=pd.Index(range(int(min_seqn), int(max_seqn) + 1), name="SEQN"))
    
    for file_name in tqdm(file_names):
        raw_data = pd.read_csv("extraction/raw_data/examination/" + file_name + ".csv")
        if "SEQN" not in raw_data.columns:
            continue

        raw_data.set_index("SEQN", inplace=True)
        if "SPXRAW" not in file_name:  # "Spirometry - Raw Curve Data" does not contain extra columns
            raw_data.drop(columns=["file_name", "cycle", "begin_year", "end_year"], inplace=True)
    
        data_category.loc[raw_data.index, raw_data.columns] = raw_data

    
    object_columns = data_category.columns[data_category.dtypes == "object"]
    data_category[object_columns] = data_category[object_columns].astype(str, copy=False)
    
    data_category.dropna(how="all", inplace=True)
    data_category.reset_index().to_feather(f"fusion/fusionned_data/examination/{category}.feather")
