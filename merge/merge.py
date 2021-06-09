import sys
import argparse
import pandas as pd


def merge_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Merge the demographics and the mortality files with the files taken from the casting step")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory"], required=True)
    parser.add_argument("-c", "--category", help="Name of the category", required=True)

    args = parser.parse_args(argvs)
    print(args)

    merge(args.main_category, args.category)


def merge(main_category, category):
    demographics = pd.read_feather("casting/data/demographics/demographics.feather").set_index("SEQN")

    variable_examination = pd.read_feather("extraction/data/variables_examination.feather", columns=["variable_name", "variable_description"]).drop_duplicates()
    variable_demographics = pd.read_feather("extraction/data/variables_demographics.feather", columns=["variable_name", "variable_description"]).drop_duplicates()
    variable_laboratory = pd.read_feather("extraction/data/variables_laboratory.feather", columns=["variable_name", "variable_description"]).drop_duplicates()

    variable_description = pd.concat((variable_demographics, variable_examination, variable_laboratory)).reset_index(drop=True)
    variable_description.drop(index=variable_description.index[variable_description["variable_name"].duplicated()], inplace=True)
    variable_description.set_index("variable_name", inplace=True)

    data_category = pd.read_feather(f"casting/data/{main_category}/{category}.feather").set_index("SEQN")
    data_category[demographics.columns] = demographics.loc[data_category.index]

    pruned_variable_name = data_category.columns.str.split("_").map(lambda splitted_variable: splitted_variable[0])
    data_category.columns = data_category.columns + "; " + variable_description.loc[pruned_variable_name, "variable_description"]

    data_category.reset_index().to_feather(f"merge/data/{main_category}/{category}.feather")