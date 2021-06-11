import pandas as pd
from tqdm import tqdm 
import json


COLUMNS_TO_TAKE_CATEGORIZER = {"module": "main_category", "var": "variable", "category": "category"}
COLUMNS_TO_TAKE_VARIABLES = {"variable_name": "variable", "variable_description": "variable_description", "data_file_name": "file_name", "data_file_description": "file_description"}

if __name__ == "__main__":
    categorizer = pd.read_csv("fusion/data/VarDescription.csv", usecols=COLUMNS_TO_TAKE_CATEGORIZER).rename(columns=COLUMNS_TO_TAKE_CATEGORIZER)
    categorizer.drop(index=categorizer.index[categorizer["variable"].duplicated()], inplace=True)
    categorizer.set_index("main_category", inplace=True)

    variables_overview = {}

    for main_category in ["examination", "laboratory", "questionnaire"]:
        variables_main_category = pd.read_feather(f"extraction/data/variables_{main_category}.feather", columns=COLUMNS_TO_TAKE_VARIABLES).rename(columns=COLUMNS_TO_TAKE_VARIABLES)
        variables_main_category.drop(index=variables_main_category.index[variables_main_category["variable"].duplicated()], inplace=True)
        variables_main_category.set_index("variable", inplace=True)

        variables_main_category["category"] = categorizer.loc[main_category].set_index("variable")["category"]

        variables_overview[main_category] = variables_main_category

    with pd.ExcelWriter('fusion/data/variable_categorizer.xlsx') as writer:  
        for main_category in tqdm(["examination", "laboratory", "questionnaire"]):
            variables_overview[main_category].to_excel(writer, sheet_name=main_category)

