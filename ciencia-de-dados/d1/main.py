from os import listdir
from os.path import isfile, join

import pandas as pd


def read_dir(dir_path: str):
    files = [join(dir_path,f) for f in listdir(dir_path) if isfile((join(dir_path, f)))]
    dtfs: list[pd.DataFrame] = []

    for file in files:
        df = pd.read_csv(file, sep=";",encoding='ISO-8859-1', on_bad_lines='skip', skiprows=1)
        dtfs.append(df)
    concat_dtfs = pd.concat(dtfs, ignore_index=True)
    return concat_dtfs

if __name__ == "__main__":
    path = "../data"
    dtfs = read_dir(path)
    # 04/01/2019
    dtfs["DATA"] = pd.to_datetime(dtfs["DATA"], format="%d/%m/%Y", errors='coerce')
    cols = dtfs.columns
