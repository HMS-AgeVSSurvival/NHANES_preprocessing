import pandas as pd
import os


if __name__ == "__main__":
    with pd.ExcelWriter("export_shapes/data/shapes.xlsx") as writer:  
        for main_category in ["examination", "laboratory", "questionnaire"]:
            list_shapes = []

            for file_category in os.listdir(f"merge/data/{main_category}"):
                n_partipants, n_variables = pd.read_feather(f"merge/data/{main_category}/{file_category}").shape
                list_shapes.append([file_category.split(".")[0], n_partipants, n_variables])

            pd.DataFrame(list_shapes, columns=["category", "n_particapants", "n_variables"]).set_index("category").to_excel(writer, sheet_name=main_category)
