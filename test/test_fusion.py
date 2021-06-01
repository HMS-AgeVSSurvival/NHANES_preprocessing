import unittest
import pandas as pd

from fusion.fusion import load_information_files, get_file_names


class TestLoadInformationFiles(unittest.TestCase):
    def test_matching_file_description(self):
        # Test if all the files descriptions in the file split_examination.json are matching with
        # the files descriptions in the information file given by NHANES.
        splitting_examination, information_files = load_information_files(prefix="../")

        list_file_descriptions = []
        for file_descriptions in splitting_examination.values():
            list_file_descriptions.extend(file_descriptions)
        index_file_descriptions =pd.Index(list_file_descriptions)

        self.assertTrue(all(information_files["data_file_description"].isin(index_file_descriptions)))
        self.assertTrue(all(index_file_descriptions.isin(information_files["data_file_description"])))

    def test_seqn(self):
        # Test if the files, that are going to be loaded, contain SEQN 
        # and if SEQN contains are duplicated rows
        splitting_examination, information_files = load_information_files(prefix="../")

        for category in splitting_examination.keys():
            print(category)
            file_names = get_file_names(splitting_examination, information_files, category)

            for file_name in file_names:
                raw_data = pd.read_csv(
                    "../extraction/raw_data/examination/" + file_name + ".csv"
                )

                self.assertTrue("SEQN" in raw_data.columns)
                self.assertTrue(raw_data["SEQN"].is_unique)


