import pprint
import pandas as pd

# ----------------- Importando bibliotecas
transacoes_df = pd.read_csv("C:/Users/aluno02.TSACBRRJLP04B/Downloads/transferoacademy_transações.csv", sep=';', encoding="latin-1")  # importa csv_transações
#pprint.pprint(transacoes_df)  # Mostrando todas a tabela  # visualização do arquivo
#pprint.pprint(transacoes_df.columns.tolist())  # Mostrando todas as colunas da tabela


#pprint.pprint(transacoes_df.head())  # metodo head mostra as 5 primeiras linhas
#pprint.pprint(transacoes_df.shape)  # metodo shape mostra a quantidade de linhas e colunas
#pprint.pprint(transacoes_df.describe())  # metodo mostra informações sobre a tabela

#tabela_completa = transacoes_df[['Conta','tipo de operação', 'Entrou', 'Moeda que Saiu', 'Saiu', 'Moeda de Taxa', 'Taxa', 'moeda recebida em reais', 'moeda enviada em reais']]
#pprint.pprint(tabela_completa)

#pprint.pprint(transacoes_df.loc[1])  # puxa todas as infotmações de uma linha

#transacoes_trade_df = (transacoes_df[transacoes_df['tipo de operação'] == 'trade'])  # Filtrando apenas transações trade
#pprint.pp(transacoes_trade_df)
#moedas_ponto = transacoes_df.replace(value='.', to_replace=',', regex=True)  # tratando ',' por '.'

colunas = ['Entrou', 'Saiu', 'Taxa', 'moeda recebida em reais', 'moeda enviada em reais']
transacoes_df[colunas] = transacoes_df[colunas].apply(lambda x: x.str.replace(',', '.', regex=True)).astype(float)
#pprint.pprint(transacoes_df.loc[1])
#moedas_ponto['Entrou'] = moedas_ponto['Entrou'].astype(float)
#print(transacoes_df['Entrou'].info)
#pprint.pprint(transacoes_df.loc[1])

#saida_btc = transacoes_df.loc[transacoes_df['Moeda que Saiu'] == 'BTC' ]  # pegando a moeda que saiu


transacoes_numero = transacoes_df['Conta'].value_counts()  # Quantidade de transações de cada conta
#transacoes_df['Saldo'] = transacoes_df['Entrou'] * transacoes_df['moeda recebida em reais'] - transacoes_df['Saiu'] * transacoes_df['moeda recebida em reais']

transacoes_df['Saldo'] = (transacoes_df['Entrou'] - transacoes_df['Taxa']) * (transacoes_df['moeda recebida em reais'])

transacoes_df['horario'].sum()
pprint.pprint(transacoes_df.loc[0])


"""transacoes_df['Entrada taxada'] = transacoes_df['Entrou'] - transacoes_df['Taxa']

for i in transacoes_df.iterrows():
    print(i)
    if transacoes_df['Moeda que Saiu'].items() == 'BTC':
        transacoes_df['Saldo'] = sum(transacoes_df['Saiu'])
    else:
        pass
"""
