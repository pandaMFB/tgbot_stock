from time import sleep

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {

}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'd9164526-f588-4e12-8bcf-f82d9aaa2a5c',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  crypto_data = json.loads(response.text)

  info_crypto_all = []

  for elem in crypto_data['data']:
    crypto_id = elem['id']
    crypto_name = elem['name']
    crypto_symbol = elem['symbol']
    crypto_slug = elem['slug']

    print(crypto_id,':',crypto_name,':',crypto_symbol,':',crypto_slug)

#https://ru.tradingview.com/symbols/SPX/

    # info_crypto_all.append(crypto_id)
    # info_crypto_all.append(crypto_name)
    # info_crypto_all.append(crypto_symbol)
    # info_crypto_all.append(crypto_slug)

    # list_info_crypto = {
    #   'id': crypto_id,
    #   'name': crypto_name,
    #   'symbol': crypto_symbol,
    #   'slug': crypto_slug
    # }

  # with open('C:/Users/abutoveo/PycharmProjects/TelegramBot/files_info/cryptocurrency_info.txt', 'w') as crypto:
  #   json.dump(info_crypto_all, crypto, indent=4)


except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


