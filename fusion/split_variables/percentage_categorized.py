import pandas as pd

COLUMNS_TO_TAKE = {
    "var": "variable",
    "var_desc": "variable_description",
    "category": "category",
    "module": "main_category",
}

if __name__ == "__main__":
    variable_description = pd.read_csv(
        "fusion/data/VarDescription_Chirag.csv", usecols=COLUMNS_TO_TAKE
    ).rename(columns=COLUMNS_TO_TAKE)

    for main_category in ["examination", "laboratory", "demographics", "questionnaire"]:
        variable_main_category = pd.read_feather(
            f"extraction/data/variables_{main_category}.feather"
        )

        unique_variable_main_category = variable_main_category[
            "variable_name"
        ].drop_duplicates()

        categorized_from_main_category = unique_variable_main_category.isin(
            variable_description["variable"]
        ).sum()

        print(
            f"Percentage categorized in {main_category}",
            100 * categorized_from_main_category / len(unique_variable_main_category),
        )
