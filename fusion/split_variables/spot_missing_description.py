import os 
from tqdm import tqdm
import pandas as pd
import json

COLUMNS_TO_TAKE = {"var": "variable", "var_desc": "variable_description", "category": "category"}


if __name__ == "__main__":
    variable_description_raw = pd.read_csv("fusion/data/VarDescription.csv", usecols=COLUMNS_TO_TAKE).rename(columns=COLUMNS_TO_TAKE)
    variable_description = variable_description_raw.drop_duplicates().set_index("variable")

    for main_category in ["examination", "laboratory"]:
        missing_entire_files = {}
        list_missing_variables_description = []
        for file in tqdm(os.listdir(f"extraction/data/{main_category}/")):
            if file[-4:] == ".csv":
                variables = pd.read_csv(f"extraction/data/{main_category}/{file}").columns

                missing_variables = variables[~variables.isin(variable_description.index)]

                if len(missing_variables) == len(variables):
                    missing_entire_files[file] = variables.tolist()
                elif len(missing_variables) > 0:
                    list_missing_variables_description.append(dict(zip(missing_variables.tolist(), [file] * len(missing_variables))))

        sorted_missing_entire_files = dict(sorted(missing_entire_files.items()))

        missing_variables_description = {k: v for missing_variables_description in list_missing_variables_description for k, v in missing_variables_description.items()}
        sorted_missing_variables_description = dict(sorted(missing_variables_description.items()))
        
        with open(f"fusion/split_variables/splitting/{main_category}_missing_entire_file.json", "w") as outfile:
            json.dump(sorted_missing_entire_files, outfile)
        with open(f"fusion/split_variables/splitting/{main_category}_missing_variables_description.json", "w") as outfile:
            json.dump(sorted_missing_variables_description, outfile)