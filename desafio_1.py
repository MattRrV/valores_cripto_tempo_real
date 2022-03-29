import os
import csv
import pandas as pd
from pathlib import Path

arquivo_caminho = input(('Insira o arquivo raiz: ').upper()) #onde esta o caminho do arquivo raiz
arquivo_final = input(('Insira onde o saldos finais devem ser escritos: ').upper()) #onde o arquivo final vai ser escrito
arquivo_auxiliar = 'saldos_temp.csv'

d = Path(arquivo_auxiliar)
if d.is_file():
    f2 = open(arquivo_auxiliar, 'r+')
    f2.truncate(0)
      
df = pd.read_csv(arquivo_caminho , sep=';', encoding='latin-1')
print(df.info())
cols = ['Entrou', 'Saiu', 'Taxa', 'moeda recebida em reais', 'moeda enviada em reais']

df[cols] = df[cols].apply(lambda x : x.str.replace(',', '.')).astype('float')


"""#tratamento das colunas
df['moeda recebida em reais'] = df['moeda recebida em reais']
df['moeda recebida em reais'] = pd.to_numeric(df['moeda recebida em reais'])
#df['moeda enviada em reais'] = df['moeda enviada em reais'].str.replace(',', '.')
df['moeda enviada em reais'] = pd.to_numeric(df['moeda enviada em reais'])
df['Entrou'] = df['Entrou'].str.replace(',', '.')
df['Entrou'] = pd.to_numeric(df['Entrou'])
df['Saiu'] = df['Saiu'].str.replace(',', '.')
df['Saiu'] = pd.to_numeric(df['Saiu'])
df['Taxa'] = df['Taxa'].str.replace(',', '.')
#df['Taxa'] = pd.to_numeric(df['Taxa'])"""

#transformacao em reais
df['cot_entrou'] = df['moeda recebida em reais'] * df['Entrou']
df['cot_saiu'] = df['moeda enviada em reais'] * df['Saiu']
df['cot_taxa'] = df['moeda recebida em reais'] * df['Taxa']

f = open(arquivo_auxiliar, 'a')

writer = csv.writer(f)

writer.writerow(['horario','Conta','Moeda','Entrou','Saiu','Cot_Entrou','Cot_Saiu'])

#Entradas
for i, rows in df.iterrows():
    writer.writerow([rows['horario'],rows['Conta'],rows['Moeda que Entrou'],rows['Entrou'],0.0,rows['cot_entrou'],0.0])

#Saida
for i, rows in df.iterrows():
    writer.writerow([rows['horario'],rows['Conta'],rows['Moeda que Saiu'],0.0,rows['Saiu'],0.0,rows['cot_saiu']])

#Taxa que tbm eh saida
for i, rows in df.iterrows():
    writer.writerow([rows['horario'],rows['Conta'],rows['Moeda de Taxa'],0.0,rows['Taxa'],0.0,rows['cot_taxa']])

df_1 = pd.read_csv(arquivo_auxiliar)

moedas=['BCH','DOGE','USDT','XLM','XRP']

df_1 = df_1[df_1['Moeda'].isin(moedas)]

print (df_1)

df_1.sort_values(by=['Moeda'], inplace= True)

df_1['horario'] = pd.to_datetime(df_1['horario'], format='%d/%m/%Y %H:%M')

df_1.sort_values(by=['Moeda','horario'], inplace = True)

df_1['Valor'] = df_1['Entrou'] - df_1['Saiu']
df_1['Valor_2'] = df_1['Cot_Entrou'] - df_1['Cot_Saiu']
df_1['Saldo'] = df_1.groupby('Moeda')['Valor'].cumsum()
df_1['Saldo_em_Reais'] = df_1.groupby('Moeda')['Valor_2'].cumsum()
df_1 = df_1.drop(['Valor','Cot_Saiu','Valor_2','Cot_Entrou'], axis = 1)

print(df_1)

df_1.to_csv(arquivo_final, index = False)

f.close()
