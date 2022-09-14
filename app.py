from array import array
from encodings.utf_8 import decode
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import requests

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
url = "https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a"
request = requests.get(url, headers=header)

tables = pd.read_html(request.text)
df = tables[0]

#caso a origem tenha mais de uma tabela, você consegue identificar cada uma com um indice
#for i , tabela in enumerate(tables):
#    print("-----------------------------------")
#    print(i)
#    print(tabela)

#removendo colunas indesejadas
df.drop("Próx", axis = 1, inplace=True)
df.drop("%", axis = 1, inplace=True)

#dividindo a coluna posição em 3: Ranking, variação de posição e nome do time
posi = df["Posição"].str.split("  ", n = 3, expand=True)
df.insert(column='Ranking', value=posi[0], loc=0)
df.insert(column='Variação de Posição', value=posi[1], loc=1)
df.insert(column='Time', value=posi[2], loc=2)
#deletando a coluna Posição, original
del df['Posição']

#divide a coluna Time em Time e UF usando regex com grupos não nomeados
teams_ufs = df["Time"].str.extract('(^.*[^\s])\s+\-\s+([A-Z]{2})', expand=True)
del df["Time"]
df.insert(column="Time", value=teams_ufs[0], loc=1)
df.insert(column="UF", value=teams_ufs[1], loc=2)

#dividindo a coluna Recentes em 6: Ultimo jogo - vitoria, ultimo jogo - empate, ultimo jogo - derrota.
recent_results = df["Recentes"].str.extract('(?P<antepunultima>[A-Z]{1})\s*(?P<penultima>[A-Z]{1})\s*(?P<ultima>[A-Z]{1})', expand=True)
df.insert(column="Antepenúltimo", value=recent_results["antepunultima"], loc=df.shape[1])
df.insert(column="Penúltimo", value=recent_results["penultima"], loc=df.shape[1])
df.insert(column="Último", value=recent_results["ultima"], loc=df.shape[1])

#  remove a coluna 'Recentes'
del df["Recentes"]

# aplicamos a função get_dummies para converter as colunas categóricas em variáveis dummy
# https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html
df = pd.get_dummies(df, columns=["Antepenúltimo", "Penúltimo", "Último"])

#print(df)

#exportando dataframe em excel
df.to_excel("Brasileirao_serie_a.xlsx", sheet_name="Teste", na_rep="#n/a", header=True, index=True)

#exportando dataframe em json
df.to_json("Brasileirao_serie_a.json")

#exportando dataframe em excel
df.to_csv("Brasileirao_serie_a.csv", encoding="ISO-8859-1")
