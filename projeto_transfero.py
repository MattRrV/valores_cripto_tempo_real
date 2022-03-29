# import bibliotecas
import pandas as pd
import json
import pprint

# import data frame
dados = pd.read_csv('transferoacademy_transações.csv', sep=';', encoding='latin-1')
#pprint.pprint(dados.loc[0])
dados.rename({
    'moeda recebida em reais': 'c_entrada',
    'moeda enviada em reais' : 'c_saida'
}, axis=1, inplace=True)
#print(dados.loc[0])

# Tratando os números floats
#colunas1 = ['Entrou', 'Saiu', 'Taxa', 'moeda recebida em reais', 'moeda enviada em reais']
colunas = ['Entrou', 'Saiu', 'Taxa', 'c_entrada', 'c_saida']
dados[colunas] = dados[colunas].apply(lambda x : x.str.replace(',', '.')).astype('float')
#pprint.pprint(dados.dtypes)  #Verificando se as colunas passaram para float

# tratando as transações trades
dados_trade = dados[dados['tipo de operação'] == 'trade']
#pprint.pprint(dados_trade['tipo de operação'].head(20))
moedas = ['BCH', 'DOGE', 'USDT', "XLM", 'XRP']
trade_moedas = dados_trade[dados_trade['Moeda que Entrou'].isin(moedas)][['horario', 'Conta', 'Moeda que Entrou', 'Entrou', 'c_entrada']]
trade_moedas.sort_values('Moeda que Entrou')
#pprint.pprint(trade_moedas['Moeda que Entrou'].unique()) # conferindo se as moedas que entraram estão corretas
#pprint.pprint(trade_moedas.loc[0])

# calculo doido saida trade
s_trade = dados_trade[dados_trade['Moeda que Saiu'].isin(moedas)][['horario', 'Conta', 'Moeda que Saiu', 'Saiu', 'c_saida']]
t_trade = dados_trade[dados_trade['Moeda de Taxa'].isin(moedas)][['horario', 'Conta', 'Moeda que Entrou', 'Saiu', 'c_entrada']]
#retorno_trade.sort_values('Moeda') tenho que mudar dx os nomes das colunas iguais
s_trade.rename(columns={
    'Moeda que Saiu' : 'Moeda',
    'c_saida'        : 'Cotacao'
}, inplace=True)
t_trade.rename(columns={
    'Moeda que Entrou' : 'Moeda',
    'c_entrada'        : 'Cotacao'
}, inplace=True)
retorno_trade = pd.concat([s_trade, t_trade])
retorno_trade.sort_values('Moeda')  #Value error: The column label 'Moeda' is not unique. #erro concertado
#print(retorno_trade.loc[0])

# adicionando entrada do trade
dados_trade = pd.concat([trade_moedas, retorno_trade])
dados_trade = dados_trade.sort_index()
#pprint.pprint(dados_trade)

# selecionando os depositos
retorno_deposito = dados[dados['tipo de operação']=='deposit']
#print(retorno_deposito['tipo de operação'])
retorno_deposito = retorno_deposito[retorno_deposito['Moeda que Entrou'].isin(moedas)]
retorno_deposito = retorno_deposito[['horario', 'Conta', 'Moeda que Entrou', 'Entrou', 'c_entrada']]
#pprint.pprint(retorno_deposito)

# selecionando withdraw
dados_withdraw = dados[dados['tipo de operação'] == 'withdraw']
#pprint.pprint(dados_withdraw['tipo de operação'])  # verificando só withdraw
dados_withdraw = dados_withdraw[dados_withdraw['Moeda que Saiu'].isin(moedas)]
dados_withdraw_tax = dados_withdraw.loc[:,['horario', 'Conta', 'Moeda de Taxa', 'Taxa', 'c_saida']]
dados_withdraw_tax = dados_withdraw_tax[~dados_withdraw_tax['Moeda de Taxa'].isnull()]
#pprint.pprint(dados_withdraw.loc[360])  #conferindo dados

# concatenando withdraw
dados_withdraw.rename({
    'Moeda que saiu' : 'Moeda',
    'c_saida'        : 'Cotação'
}, inplace=True, axis=1)
dados_withdraw_tax.rename({
    'Moeda de Taxa' : 'Moeda',
    'Taxa': 'Saiu',
    'c_saida' : 'Cotacao'
}, inplace=True, axis=1)
withdraw = pd.concat([dados_withdraw, dados_withdraw_tax])
#print(withdraw)

# montando DF final
df_fim = pd.concat([retorno_deposito, retorno_trade, withdraw])
df_fim[['Saiu','Entrou']] = df_fim[['Saiu','Entrou']].fillna(0.0)
df_fim = df_fim.sort_index(kind='mergesort')
df_fim = df_fim.reset_index(drop=True)
pprint.pp(df_fim.info())
























