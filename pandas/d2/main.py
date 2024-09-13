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
    combined_dtfs = combined_dtfs.drop_duplicates()
    return combined_dtfs

if __name__ == '__main__':
    path = "../Datasets/dados_emprestimos"
    emprestimos_biblioteca = read_dir(path)
    dados_exemplares = pd.read_parquet('../Datasets/dados_exemplares.parquet')
    emprestimos = emprestimos_biblioteca.merge(dados_exemplares)
    CDU_lista = []
    for CDU in emprestimos['localizacao']:
      if(CDU < 100):
        CDU_lista.append('Generalidades')
      elif(CDU < 200):
        CDU_lista.append('Filosofia e psicologia')
      elif(CDU < 300):
        CDU_lista.append('Religião')
      elif(CDU < 400):
        CDU_lista.append('Ciências sociais')
      elif(CDU < 500):
        CDU_lista.append('Classe vaga')
      elif(CDU < 600):
        CDU_lista.append('Matemática e ciências naturais')
      elif(CDU < 700):
        CDU_lista.append('Ciências aplicadas')
      elif(CDU < 800):
        CDU_lista.append('Belas artes')
      elif(CDU < 900):
        CDU_lista.append('Linguagem')
      else:
        CDU_lista.append('Geografia. Biografia. História.')
    emprestimos["CDU_geral"] = CDU_lista
    emprestimos.drop(columns=['registro_sistema'], inplace=True)
    emprestimos['matricula_ou_siape'] = emprestimos['matricula_ou_siape'].astype('string')
    print(emprestimos.head())
