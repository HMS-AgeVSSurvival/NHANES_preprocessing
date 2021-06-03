import pandas as pd
import json 


def get_file_description(main_category):
    files_main_category = pd.read_feather(f"extraction/data/files_{main_category}.feather", columns=["data_file_description", "data_file_name"])

    files_main_category.dropna(how="any", inplace=True)

    sorted_files_main_category = sorted(files_main_category["data_file_description"].drop_duplicates().tolist())

    with open(f"fusion/splitting/raw_file_descriptions_{main_category}.json", "w") as outfile:
        json.dump(sorted_files_main_category, outfile)


if __name__ == "__main__":
    get_file_description("examination")
    get_file_description("laboratory")