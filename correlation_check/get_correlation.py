import os
import pandas as pd
from tqdm import tqdm
import scipy.stats

from correlation_check.utils import get_col_values, find_cell, update_cell


if __name__ == "__main__":
    age = pd.read_feather("cleaning/data/demographics/demographics.feather", columns=["SEQN", "RIDAGEEX_extended"]).set_index("SEQN")["RIDAGEEX_extended"]

    for main_category in ["demographics", "examination", "laboratory", "questionnaire", "demographics", "mortality"]:      
        correlation_col = find_cell(main_category, "age correlation").col
        p_value_col = find_cell(main_category, "p-value").col

        variables = get_col_values(main_category, find_cell(main_category, "variable").col)[1:]            
        categories = get_col_values(main_category, find_cell(main_category, "category").col)[1:]            
        variables_categorized = pd.DataFrame.from_dict({"variable": variables, "category": categories})
        
        for (category, group_category) in tqdm(variables_categorized.groupby(by=["category"])):
            path_file = f"fusion/data/{main_category}/{category.replace('/', '_or_').replace(' ', '__').replace('.', '--')}.feather"

            if not os.path.exists(path_file):  # The file only contains variables that are not processed
                continue
            data_file = pd.read_feather(path_file).set_index("SEQN")

            for variable in group_category["variable"]:
                if variable not in data_file.columns:  # The file entails non unique SEQN
                    continue

                index_notna = data_file.index[data_file[variable].notna()]

                # If the variable is not categorical and the number of participants is higher than one
                if data_file.loc[index_notna, variable].dtype != "object" and len(index_notna) > 1 :
                    correlation, p_value = scipy.stats.pearsonr(data_file.loc[index_notna, variable], age.loc[index_notna])

                    variable_row = find_cell(main_category, variable).row
                    update_cell(main_category, variable_row, correlation_col, correlation)
                    update_cell(main_category, variable_row, p_value_col, p_value)