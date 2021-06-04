import sys
import argparse
import pandas as pd
from tqdm import tqdm
import json


def fusion_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Fusion of the files taken from NHANES website")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory", "demographics"], required=True)
    parser.add_argument("-c", "--category", help="Name of the category", required=True)

    args = parser.parse_args(argvs)
    print(args)

    fusion(args.main_category, args.category)


def load_information_files(main_category, prefix=""):
    with open(prefix + f"fusion/splitting/split_{main_category}.json") as json_file:
        splitting_examination = json.load(json_file)

    information_files = pd.read_feather(prefix + f"extraction/data/files_{main_category}.feather", columns=["data_file_description", "data_file_name"])

    information_files.dropna(how="any", inplace=True)

    return splitting_examination, information_files


def get_file_names(main_category, splitting_examination, information_files, category):
    if main_category == "examination":
        # Drop files that are not corresponding to the category
        # Drop PAXRAW_D: cannot be downloaded properly
        # Drop P_BPXO, P_BMX, P_OHXDEN and P_OHXREF: files not accessible and convered by others
        # Drop AUXAR_I, AUXTYM_I, AUXWBR_I, PAXRAW_C, SPXRAW_E, SPXRAW_F, SPXRAW_G, PAXDAY_G, PAXDAY_H, PAXHR_G, PAXHR_H, PAXMIN_G, PAXMIN_H: those files are time series
        files_to_drop = [
            "PAXRAW_D",
            "P_BPXO",
            "P_BMX",
            "P_OHXDEN",
            "P_OHXREF",
            "AUXAR_I",
            "AUXTYM_I",
            "AUXWBR_I",
            "PAXRAW_C",
            "SPXRAW_E",
            "SPXRAW_F",
            "SPXRAW_G",
            "PAXDAY_G",
            "PAXDAY_H",
            "PAXHR_G",
            "PAXHR_H",
            "PAXMIN_G",
            "PAXMIN_H",
        ]
    else:
        # Drop P_DEMO: files not accessible and convered by others
        files_to_drop = ["P_DEMO"]

    cleaned_information_files = information_files.drop(
        index=information_files.index[
            (
                ~information_files["data_file_description"].isin(
                    splitting_examination[category]
                )
            )
            | information_files["data_file_name"].isin(files_to_drop)
        ]
    )

    return cleaned_information_files["data_file_name"].drop_duplicates()


def fusion(main_category, category):
    splitting_examination, information_files = load_information_files(main_category)
    file_names = get_file_names(main_category, splitting_examination, information_files, category)
     
    # Get the SEQN numbers range
    min_seqn = float("inf")
    max_seqn = -float("inf")
    for file_name in tqdm(file_names):
        data = pd.read_csv(f"extraction/data/{main_category}/" + file_name + ".csv")

        if data["SEQN"].min() < min_seqn:
            min_seqn = data["SEQN"].min()
        if max_seqn < data["SEQN"].max():
            max_seqn = data["SEQN"].max()

    # Fill the dataframe
    data_category = pd.DataFrame(
        None, index=pd.Index(range(int(min_seqn), int(max_seqn) + 1), name="SEQN")
    )

    for file_name in tqdm(file_names):
        data = pd.read_csv(
            f"extraction/data/{main_category}/" + file_name + ".csv"
        ).set_index("SEQN")

        if main_category == "demographics":
            data.drop(columns=data.columns[~data.columns.isin(["SDDSRVYR", "RIAGENDR", "RIDAGEYR", "RIDAGEEX", "RIDRETH1"])], inplace=True)
        else:
            if (
                "SPXRAW" not in file_name
            ):  # "Spirometry - Raw Curve Data" does not contain extra columns
                data.drop(
                    columns=["file_name", "cycle", "begin_year", "end_year"], inplace=True
                )

        data_category.loc[data.index, data.columns] = data

    columns_object = data_category.columns[data_category.dtypes == "object"]
    data_category[columns_object] = data_category[columns_object].astype(
        str, copy=False
    )

    data_category.dropna(how="all", inplace=True)
    data_category.reset_index().to_feather(
        f"fusion/data/{main_category}/{category}.feather"
    )
