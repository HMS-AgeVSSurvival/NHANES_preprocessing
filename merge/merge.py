import sys
import argparse
import pandas as pd


def merge_cli(argvs=sys.argv[1:]):
    parser = argparse.ArgumentParser("Merge the demographics and the mortality files with the files taken from the casting step")
    parser.add_argument("-mc", "--main_category", help="Name of the main category", choices=["examination", "laboratory", "questionnaire"], required=True)
    parser.add_argument("-c", "--category", help="Name of the category", required=True)

    args = parser.parse_args(argvs)
    print(args)

    merge(args.main_category, args.category)


def merge(main_category, category):
    demographics = pd.read_feather("casting/data/demographics/demographics.feather").set_index("SEQN")
    mortality = pd.read_feather("casting/data/mortality/mortality.feather").set_index("SEQN")

    variable_main_category = pd.read_feather(f"extraction/data/variables_{main_category}.feather", columns=["variable_name", "variable_description"]).drop_duplicates()
    variable_main_category.drop(index=variable_main_category.index[variable_main_category["variable_name"].isin(["RIAGENDR", "RIDRETH1"])], inplace=True)
    variable_demographics = pd.read_feather("extraction/data/variables_demographics.feather", columns=["variable_name", "variable_description"]).drop_duplicates()
    
    variable_description = pd.concat((variable_main_category, variable_demographics)).reset_index(drop=True)
    variable_description.drop(index=variable_description.index[variable_description["variable_name"].duplicated()], inplace=True)
    variable_description.set_index("variable_name", inplace=True)

    data_category = pd.read_feather(f"casting/data/{main_category}/{category}.feather").set_index("SEQN")
    data_category[demographics.columns] = demographics
    data_category[mortality.columns] = mortality


    # Recover origin name before conversion to dummies
    pruned_variable_name = data_category.columns.drop(mortality.columns).str.split("_").map(lambda splitted_variable: splitted_variable[0])
    if category == "Fatty__Acids__-__Plasma__(Surplus)":
        series_pruned_variable_name = pruned_variable_name.to_series()
        series_pruned_variable_name[(~series_pruned_variable_name.isin(variable_description.index))] += "_N"

        pruned_variable_name = pd.Index(series_pruned_variable_name.values)

    columns_to_rename = dict(zip(data_category.columns.drop(mortality.columns), data_category.columns.drop(mortality.columns) + "; " + variable_description.loc[pruned_variable_name, "variable_description"]))

    data_category.rename(columns=columns_to_rename).reset_index().to_feather(f"merge/data/{main_category}/{category}.feather")