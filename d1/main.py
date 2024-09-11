from os import listdir
from os.path import isfile, join
from typing import List

import pandas as pd

dir_path = "./Datasets/dados_emprestimos/"

files = [join(dir_path,f) for f in listdir(dir_path) if isfile((join(dir_path, f)))]

# id_emprestimo,codigo_barras,data_renovacao,data_emprestimo,data_devolucao,matricula_ou_siape,tipo_vinculo_usuario

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

print(combined_dtfs["data_emprestimo"])
