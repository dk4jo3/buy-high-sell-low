import requests
import json
from datetime import datetime
import os

# function to get price

def getData(url, dir, dir2):
	while True: 
	    api_response = requests.get(url)
	    if api_response.status_code != 200:
	        api_price = 'Error'
	    else:
	        api_data = api_response.json()
	        if dir2 != 0:
	            api_price = api_data[dir][dir2]
	        else:
	            api_price = api_data[dir]
	        api_price = float(api_price)
	        api_price = round(api_price, 2)
	        return api_price

#calculate unit difference

def unitDiff(p):
    if isinstance(p, str) == True:
        return "---"
    else:
        result = round(p - coinbasePrice, 2)
        return result

def percent_dif(p):
    if isinstance(p, str) == True:
        return "---"
    else:
        result = round(((p - coinbasePrice) / coinbasePrice) * 100, 2)
        return result

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)

coinbasePrice = getData("https://api.coinbase.com/v2/prices/BTC-USD/buy", "data", "amount") 
maicoinPrice = getData("https://max-api.maicoin.com/api/v2/tickers/btcusdt", "last", 0)
bitoPrice = getData("https://api.bitopro.com/v3/tickers/btc_usdt", "data", 'lastPrice')

dataDict = { 'coinbase': 
                    {'url': "https://www.coinbase.com/",
                     'price': getData("https://api.coinbase.com/v2/prices/BTC-USD/buy", "data", "amount"),
                     'unitDif': 0,
                     'percDif': 0,
                     'img': "../buyHighSellLow/static/style/img/coinbase-card-img.png"
                     },
            'bitopro': 
                    {'url': "https://www.bitoex.com/",
                     'price': getData("https://max-api.maicoin.com/api/v2/tickers/btcusdt", "last", 0),
                     'unitDif': unitDiff(bitoPrice),
                     'percDif': percent_dif(bitoPrice),
                     'img': "../buyHighSellLow/static/style/img/bitopro-card-img.png"
                     },
            'maicoin': 
                    {'url': "https://www.maicoin.com/en",
                     'price': getData("https://api.bitopro.com/v3/tickers/btc_usdt", "data", 'lastPrice'),
                     'unitDif': unitDiff(maicoinPrice),
                     'percDif': percent_dif(maicoinPrice),
                     'img': "../buyHighSellLow/static/style/img/maimax-card-img.png"
                     },
            'time': 
                    {'currentTime': current_time
                     }
                }

print (dataDict)

# write and dump data to json


# github directory bath
filename = '../buyHighSellLow/static/style/js/priceData.json'
with open(filename, 'r') as f:
    data = json.load(f)
    

    # overwrite existing obj in json
    print (data)
    data = dataDict

os.remove(filename)
with open(filename, 'w') as f:
    # sort key = true to remain the key order
    json.dump(data, f, indent=4, sort_keys=True)
