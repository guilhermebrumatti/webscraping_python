from encodings.utf_8 import decode
import pandas as pd
import requests

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a'
request = requests.get(url, headers=header)

df = pd.read_html(request.text)


#caso a origem tenha mais de uma tabela, você consegue identificar cada uma com um indice
#for i , tabela in enumerate(df):
#    print('-----------------------------------')
#    print(i)
#    print(tabela)

#transformando a tabela que vem como lista em dataframe.
#removendo colunas indesejadas
#removendo caracteres indesejados da coluna Posição
df = pd.DataFrame(df[0])
df.drop('Próx', axis = 1, inplace=True)
df.drop('%', axis = 1, inplace=True)
df['Posição'].replace('  0  ', ' ', regex=True, inplace=True)
print(df)

#exportando dataframe em excel
df.to_excel('ex.xlsx', sheet_name='Teste', na_rep='#n/a', header=True, index=True)

#exportando dataframe em json
df.to_json('ex.json')

#exportando dataframe em excel
df.to_csv('ex.csv', encoding='ISO-8859-1')
