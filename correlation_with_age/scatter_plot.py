import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap

from utils.google_sheets_sdk import find_cell, get_cell


def scatter_plot_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        "Plot the scatter plot of a variable of NHANES dataset"
    )
    parser.add_argument(
        "-mc",
        "--main_category",
        help="Name of the main category",
        choices=[
            "examination",
            "laboratory",
            "questionnaire",
            "demographics",
            "mortality",
        ],
        required=True,
    )
    parser.add_argument("-v", "--variable", help="Name of the varaible", required=True)
    args = parser.parse_args(argvs)
    print(args)

    scatter_plot(args.main_category, args.variable)


def scatter_plot(main_category, variable):
    variable_row = find_cell(main_category, variable).row
    category_col = find_cell(main_category, "category").col
    variable_description_col = find_cell(main_category, "variable_description").col

    category = get_cell(main_category, variable_row, category_col).value
    description = get_cell(main_category, variable_row, variable_description_col).value

    data_variable = pd.read_feather(
        f"fusion/data/{main_category}/{category.replace('/', '_or_').replace(' ', '__').replace('.', '--')}.feather",
        columns=["SEQN", variable],
    ).set_index("SEQN")[variable]
    age = pd.read_feather(
        "cleaning/data/demographics/demographics.feather",
        columns=["SEQN", "RIDAGEEX_extended"],
    ).set_index("SEQN")["RIDAGEEX_extended"]

    valid_indexes = age.index.intersection(data_variable.index[data_variable.notna()])
    min_age = int((age.loc[valid_indexes].min() / 12).round())
    max_age = int((age.loc[valid_indexes].max() / 12).round())

    plt.scatter(age.loc[valid_indexes] / 12, data_variable.loc[valid_indexes])
    plt.xlabel("Age at date of examination (in months)")
    plt.ylabel("\n".join(wrap(f"{description} ({variable})", 60)))
    plt.title(f"{len(valid_indexes)} participants. Age range {min_age} to {max_age}")

    plt.savefig(f"correlation_with_age/scatter_plots/{variable}.png")
