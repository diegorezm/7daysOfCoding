from os import listdir
from os.path import isfile, join
from typing import List

import matplotlib.pyplot as plt
import pandas as pd


def read_dir(dir_path: str) -> pd.DataFrame:
    files = [join(dir_path,f) for f in listdir(dir_path) if isfile((join(dir_path, f)))]
    dtfs: List[pd.DataFrame] = []
    for file in files:
        csv = pd.read_csv(file)
        dtfs.append(csv)
    embeded = pd.concat(dtfs, ignore_index=True)
    combined_dtfs = embeded.drop_duplicates()
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
    date_format = "%Y/%m/%d %H:%M:%S.%f"
    emprestimos["data_devolucao"] = pd.to_datetime(emprestimos["data_devolucao"], format=date_format)
    emprestimos["data_renovacao"] = pd.to_datetime(emprestimos["data_renovacao"], format=date_format)
    emprestimos["data_emprestimo"] = pd.to_datetime(emprestimos["data_emprestimo"], format=date_format)

    # ['id_emprestimo', 'codigo_barras', 'data_renovacao', 'data_emprestimo',                           
    #   'data_devolucao', 'matricula_ou_siape', 'tipo_vinculo_usuario',                                  
    #   'id_exemplar', 'colecao', 'biblioteca', 'status_material',                                       
    #   'localizacao', 'CDU_geral']
    #   print(emprestimos.columns)

    emprestimos['month'] = emprestimos['data_emprestimo'].dt.strftime('%B')
    numero_emprestimos_por_mes = emprestimos.groupby('month').size().sort_index()

    df = numero_emprestimos_por_mes.reset_index()

    df.columns = ['mes', 'emprestimos']
    df = df.sort_values(by=["emprestimos"])

    df.plot(kind='bar', x='mes', y='emprestimos', color='skyblue') 

    # Add titles and labels
    plt.title("Number of Loans per Month", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Number of Loans", fontsize=12)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

    worst_months = df.head(2)
    print("Os meses com menor movimento são: \n")
    for index, row in worst_months.iterrows():
        print(f"{row['mes']}\n")
