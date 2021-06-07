import json


def sort_split(main_category):
    with open(f"fusion/splitting/split_{main_category}.json") as json_file:
        splitting_main_category = json.load(json_file)

    sorted_splitting_main_category = {}
    for key, value in splitting_main_category.items():
        sorted_splitting_main_category[key] = sorted(value)

    with open(f"fusion/splitting/split_{main_category}.json", "w") as outfile:
        json.dump(sorted_splitting_main_category, outfile)


if __name__ == "__main__":
    sort_split("examination")
    sort_split("laboratory")
