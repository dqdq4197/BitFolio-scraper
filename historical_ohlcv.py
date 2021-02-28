from bs4 import BeautifulSoup
from datetime import datetime, timezone
import requests
import pandas as pd
import json
import time
import csv
import dateutil.parser as dp

# 2021.02.26 => 1614265200
# date: 2018.01.01 ~ 2021.02.27
# 2015.01.01 => 1420038000
# timestamp:  1514732400 ~ 1614384000.0

# historicalData_url = 'https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=1&convert=USD,KRW,EUR&time_start=1614265200&time_end=1614384000'
exam = [1,1027 ,2010 ,1839 ,825 ,6636 ,52 ,2]
ohlcv_EUR = []
ohlcv_KRW = []
ohlcv_USD = []
startTime = 1514732400
endTime = 1614384000
lastpage = 42
coins = []
empty_data_id = []

# date_string = '2018-01-01'
# dateobj = datetime.strptime(date_string, '%Y-%m-%d')
# print(time.mktime(dateobj.timetuple()))
#1681, 1305 누락된 데이터 

for page in range(1, lastpage + 1):
  cmc = requests.get(f'https://coinmarketcap.com/?page={page}')
  soup = BeautifulSoup(cmc.content, 'html.parser')
  data = soup.find('script', id="__NEXT_DATA__", type="application/json")
  
  #using data.contents[0] to remove script tags
  coin_data = json.loads(data.contents[0])
  listing = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
  for i in listing:
    coins.append(i['id'])

for i in coins:
  cmc = requests.get(f'https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id={i}&convert=USD,KRW,EUR&time_start={startTime}&time_end={endTime}')
  if 'data' in cmc.json():
    print(i, '성공')
    res = cmc.json()['data']
    coinId = res['id']
    for quote in res['quotes']:
      timestamp = time.mktime(datetime.strptime(quote['time_open'][:19], '%Y-%m-%dT%H:%M:%S').timetuple())
      ohlcv_EUR.append(
        {
          'coin_id' : coinId,
          'timestamp': timestamp,
          'time_open': quote['time_open'],
          'time_close': quote['time_close'],
          'time_high': quote['time_high'],
          'time_low': quote['time_low'],
          'open': quote['quote']['EUR']['open'],
          'close': quote['quote']['EUR']['close'],
          'high': quote['quote']['EUR']['high'],
          'low': quote['quote']['EUR']['low'],
          'volume': quote['quote']['EUR']['volume'],
          'market_cap': quote['quote']['EUR']['market_cap'],
          'quote_timestamp': quote['quote']['EUR']['timestamp'],
        }
      )
      ohlcv_KRW.append(
        {
          'coin_id' : coinId,
          'timestamp': timestamp,
          'time_open': quote['time_open'],
          'time_close': quote['time_close'],
          'time_high': quote['time_high'],
          'time_low': quote['time_low'],
          'open': quote['quote']['KRW']['open'],
          'close': quote['quote']['KRW']['close'],
          'high': quote['quote']['KRW']['high'],
          'low': quote['quote']['KRW']['low'],
          'volume': quote['quote']['KRW']['volume'],
          'market_cap': quote['quote']['KRW']['market_cap'],
          'quote_timestamp': quote['quote']['KRW']['timestamp'],
        }
      )
      ohlcv_USD.append(
        {
          'coin_id' : coinId,
          'timestamp': timestamp,
          'time_open': quote['time_open'],
          'time_close': quote['time_close'],
          'time_high': quote['time_high'],
          'time_low': quote['time_low'],
          'open': quote['quote']['USD']['open'],
          'close': quote['quote']['USD']['close'],
          'high': quote['quote']['USD']['high'],
          'low': quote['quote']['USD']['low'],
          'volume': quote['quote']['USD']['volume'],
          'market_cap': quote['quote']['USD']['market_cap'],
          'quote_timestamp': quote['quote']['USD']['timestamp'],
        }
      )
  else:
    print(i, '-----실패')
    empty_data_id.append(i)

print(empty_data_id)

with open('./coins/ohlcv_EUR.csv', mode = 'w') as ohlcv_list:
  ohlcv_writer = csv.writer(ohlcv_list)

  for ohlcv in ohlcv_EUR:
    ohlcv_writer.writerow([
      ohlcv['coin_id'],
      ohlcv['timestamp'],
      ohlcv['time_open'],
      ohlcv['time_close'],
      ohlcv['time_high'],
      ohlcv['time_low'],
      ohlcv['open'],
      ohlcv['close'],
      ohlcv['high'],
      ohlcv['low'],
      ohlcv['volume'],
      ohlcv['market_cap'],
      ohlcv['quote_timestamp']
    ])

with open('./coins/ohlcv_KRW.csv', mode = 'w') as ohlcv_list:
  ohlcv_writer = csv.writer(ohlcv_list)

  for ohlcv in ohlcv_KRW:
    ohlcv_writer.writerow([
      ohlcv['coin_id'],
      ohlcv['timestamp'],
      ohlcv['time_open'],
      ohlcv['time_close'],
      ohlcv['time_high'],
      ohlcv['time_low'],
      ohlcv['open'],
      ohlcv['close'],
      ohlcv['high'],
      ohlcv['low'],
      ohlcv['volume'],
      ohlcv['market_cap'],
      ohlcv['quote_timestamp']
    ])

with open('./coins/ohlcv_USD.csv', mode = 'w') as ohlcv_list:
  ohlcv_writer = csv.writer(ohlcv_list)

  for ohlcv in ohlcv_USD:
    ohlcv_writer.writerow([
      ohlcv['coin_id'],
      ohlcv['timestamp'],
      ohlcv['time_open'],
      ohlcv['time_close'],
      ohlcv['time_high'],
      ohlcv['time_low'],
      ohlcv['open'],
      ohlcv['close'],
      ohlcv['high'],
      ohlcv['low'],
      ohlcv['volume'],
      ohlcv['market_cap'],
      ohlcv['quote_timestamp']
    ])