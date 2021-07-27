import os
import pandas as pd


if __name__ == "__main__":
    for file_name in os.listdir("extraction/data/mortality/"):
        if file_name[-8:] == ".feather":
            pd.read_feather(f"extraction/data/mortality/{file_name}").rename(columns={"seqn": "SEQN"}).to_csv(f"extraction/data/mortality/{file_name.replace('.feather', '.csv')}")