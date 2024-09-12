from os import listdir
from os.path import isfile, join
from typing import List

import pandas as pd


def read_dir(dir_path: str) -> pd.DataFrame:
    files = [join(dir_path,f) for f in listdir(dir_path) if isfile((join(dir_path, f)))]
    dtfs: List[pd.DataFrame] = []
    date_format = "%Y/%m/%d %H:%M:%S.%f"
    for file in files:
        csv = pd.read_csv(file)
        csv["data_devolucao"] = pd.to_datetime(csv["data_devolucao"], format=date_format)
        csv["data_renovacao"] = pd.to_datetime(csv["data_renovacao"], format=date_format)
        csv["data_emprestimo"] = pd.to_datetime(csv["data_emprestimo"], format=date_format)
        dtfs.append(csv)
    embeded = pd.concat(dtfs, ignore_index=True)
    combined_dtfs = embeded.astype({
        'id_emprestimo': 'int',
        'codigo_barras': 'str',
        'data_renovacao': 'str',
        'data_emprestimo': 'str',
        'data_devolucao': 'str',
        'matricula_ou_siape': 'str',
        'tipo_vinculo_usuario': 'str'
    })
    # dtfs["DATA"] = pd.to_datetime(dtfs["DATA"], format="%d/%m/%Y", errors='coerce')
    return combined_dtfs

if __name__ == '__main__':
    path = "../Datasets/dados_emprestimos"
    print(read_dir(path)["data_emprestimo"])
    
