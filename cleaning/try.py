import pandas as pd


data_category = pd.read_feather("fusion/data/mortality/mortality.feather").set_index("SEQN")

data_category.drop(index=data_category.index[data_category["ucod_leading"].isin([4.0, 10.0])], inplace=True)
data_category["survival_type"] = data_category["ucod_leading"].map({1.0: "cvd", 2.0: "cancer", 3.0: "other", 5.0: "other", 6.0: "other", 7.0: "other", 8.0: "other", 9.0: "other"})
data_category.loc[data_category["survival_type"].isna() & (data_category["mortstat"] == 1), "survival_type"] = "other"
data_category.loc[data_category["survival_type"].isna() & (data_category["mortstat"] == 0), "survival_type"] = "alive"

data_category["follow_up_time"] = data_category["permth_exm"]
data_category.loc[data_category["permth_exm"].isna(), "follow_up_time"] = data_category["permth_int"]

print(data_category)

