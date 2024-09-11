from os import listdir
from os.path import isfile, join
from typing import List

import pandas as pd


def read_dir(dir_path: str) -> pd.DataFrame:
    files = [join(dir_path,f) for f in listdir(dir_path) if isfile((join(dir_path, f)))]
    dtfs: List[pd.DataFrame] = []
    for file in files:
        csv = pd.read_csv(file)
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
    return combined_dtfs

if __name__ == '__main__':
    path = "../Datasets/dados_emprestimos"
    print(read_dir(path))
