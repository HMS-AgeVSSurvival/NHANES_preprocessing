import pandas as pd
from tqdm import tqdm
import json


def fusion_examination():
    with open("fusion/splitting/split_examination.json") as json_file:
        splitting_examination = json.load(json_file)

    files_examination = pd.read_feather("extraction/raw_data/files_examination.feather")

    # Drop P_BMX and P_OHXDEN and P_OHXREF: files not accessible and covered by order files name
    files_examination.drop(
        index=files_examination.index[
            files_examination["data_file_name"].isna()
            | files_examination["data_file_name"].isin(["P_BMX", "P_OHXDEN", "P_OHXREF"])
        ],
        inplace=True,
    )

    files_examination.set_index("data_file_description", inplace=True)

    for category, data_file_description in splitting_examination.items():
        print(category)
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
            raw_data.drop(columns=["file_name", "cycle", "begin_year", "end_year"], inplace=True)

            data_category.loc[raw_data.index, raw_data.columns] = raw_data

        data_category.dropna(how="all").reset_index().to_feather(
            f"fusion/fusionned_data/examination/{category}.feather"
        )


if __name__ == "__main__":
    fusion_examination()
