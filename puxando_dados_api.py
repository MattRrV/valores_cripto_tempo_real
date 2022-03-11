from requests import Request, Session
import json
import pprint
import pandas as pd
from IPython.display import display

pd.set_option("display.max_columns", None)
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
bitcoin_real = {
    'slug':'bitcoin',
    'convert':'BRL',

}
bitcoin_dolar = {
    'slug':'bitcoin',
    'convert':'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'f1702e3a-85ec-40de-8c9b-885b7542f01d'
}

session = Session()
session.headers.update(headers)

response_btc_real = session.get(url, params=bitcoin_real)
btc_real = json.loads(response_btc_real.text)

response_btc_doll = session.get(url, params=bitcoin_dolar)
btc_dolar = json.loads(response_btc_doll.text)

#pprint.pprint(data)
#pprint.pprint(f"Data de pesquisa: {str(btc_real['data']['1']['quote']['BRL']['last_updated'])}")
#pprint.pprint(f"Valor Bitcoin em real: {btc_real['data']['1']['quote']['BRL']['price']}")
#print("\n")
#pprint.pprint((f"Valor Bitcoin em Dollar {btc_dolar['data']['1']['quote']['USD']['price']}"))
#Final API
# ----------------------------------------------------

#pprint.pprint(btc_dolar)

# ----------------------------------------------------
# começo pandas

#pprint.pprint(btc_real)

#btc_real_df = pd.DataFrame(btc_real)  #Criando dataframe/Tabela
btc_real_df = pd.json_normalize(btc_real)
display(btc_real_df)
btc_real_df = btc_real_df[['data','1','quote','BRL','price']]
#pprint.pprint(btc_real_df)  # mostrando dados da tabela
#print(btc_real_df.head())  # mostra os primeiros dados da tabela
#print(btc_real_df.shape)   # mostra número de linhas e colunas da tabela
#print(btc_real_df.describe())

























