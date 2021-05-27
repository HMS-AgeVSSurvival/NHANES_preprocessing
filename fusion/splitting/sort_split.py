import json


def sort_split():
    with open("fusion/splitting/splitting_examination.json") as json_file:
        splitting_examination = json.load(json_file)

    sorted_splitting_examination = {}
    for key, value in splitting_examination.items():
        sorted_splitting_examination[key] = sorted(value)

    with open("fusion/splitting/splitting_examination.json", "w") as outfile:
        json.dump(sorted_splitting_examination, outfile)


if __name__ == "__main__":
    sort_split()
