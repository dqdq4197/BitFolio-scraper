from bs4 import BeautifulSoup
from datetime import datetime, timezone
import requests
import pandas as pd
import json
import time
import csv

lastpage = 42
coins = []

for page in range(1, lastpage + 1):
  cmc = requests.get(f'https://coinmarketcap.com/?page={page}')
  soup = BeautifulSoup(cmc.content, 'html.parser')
  data = soup.find('script', id="__NEXT_DATA__", type="application/json")
  
  #using data.contents[0] to remove script tags
  coin_data = json.loads(data.contents[0])
  listing = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
  for i in listing:
    coins.append({
      'coin_id': i['id'],
      'name': i['name'],
      'symbol': i['symbol'],
      'slug': i['slug']
    })

with open('./coins/coin_list.csv', mode = 'w') as coin_list:
  coin_writer = csv.writer(coin_list)

  for coin in coins:
    coin_writer.writerow([coin['coin_id'], coin['name'], coin['symbol'], coin['slug']])







