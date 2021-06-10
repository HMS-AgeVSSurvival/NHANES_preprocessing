import pandas as pd
from tqdm import tqdm 
import json


COLUMNS_TO_TAKE = {"var": "variable", "var_desc": "variable_description", "category": "category", "module": "main_category"}


if __name__ == "__main__":
    variable_description_raw = pd.read_csv("fusion/data/VarDescription.csv", usecols=COLUMNS_TO_TAKE).rename(columns=COLUMNS_TO_TAKE)
    variable_description = variable_description_raw.drop_duplicates().set_index("main_category")

    for main_category in tqdm(["examination", "laboratory"]):
        main_category_dict = {}
        categories = variable_description.loc[main_category, "category"].drop_duplicates()
        category_description = variable_description.set_index("category")
        
        for category in categories:
            variable_category_description = category_description.loc[[category]].set_index("variable")
            variable_category_description.sort_values(by="variable", inplace=True)

            main_category_dict[category] = variable_category_description["variable_description"].to_dict()
        
        with open(f"fusion/split_variables/splitting/{main_category}_split.json", "w") as outfile:
            json.dump(main_category_dict, outfile)




