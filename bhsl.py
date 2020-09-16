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

def unit_diff(cb_price, other_price):
    if isinstance(other_price, str) == True:
        return "---"
    else:
        result = round(other_price - cb_price, 2)
        return result

def percent_dif(cb_price, other_price):
    if isinstance(other_price, str) == True:
        return "---"
    else:
        result = round(((other_price - cb_price) / cb_price) * 100, 2)
        return result

def export_JSON(directory, dict_name):
	filename = directory
	with open(filename, 'r') as f:
	    data = json.load(f)

	    # overwrite existing obj in json
	    print (data)
	    data = dict_name

	os.remove(filename)
	with open(filename, 'w') as f:
	    # sort key = true to remain the key order
	    json.dump(data, f, indent=4, sort_keys=True)

def package_dict(cb_price, bito_price, mc_price): #takes those three prices and return a complete dict
    subDict = { 'coinbase': 
                        {'url': "https://www.coinbase.com/",
                         'price': cb_price,
                         'unitDif': 0,
                         'percDif': 0,
                         'img': "../buyHighSellLow/static/style/img/coinbase-card-img.png"
                         },
                'bitopro': 
                        {'url': "https://www.bitoex.com/",
                         'price': bito_price,
                         'unitDif': unit_diff(cb_price, bito_price),
                         'percDif': percent_dif(cb_price, bito_price),
                         'img': "../buyHighSellLow/static/style/img/bitopro-card-img.png"
                         },
                'maicoin': 
                        {'url': "https://www.maicoin.com/en",
                         'price': mc_price,
                         'unitDif': unit_diff(cb_price, mc_price),
                         'percDif': percent_dif(cb_price, mc_price),
                         'img': "../buyHighSellLow/static/style/img/maimax-card-img.png"
                         }
                         }
    return subDict



now = datetime.now()
current_time = now.strftime("%b %d %Y %H:%M:%S")
# print("Current Time =", current_time)

btcCoinbasePrice = getData("https://api.coinbase.com/v2/prices/BTC-USD/buy", "data", "amount") 
btcBitoPrice = getData("https://api.bitopro.com/v3/tickers/btc_usdt", "data", 'lastPrice')
btcMaicoinPrice = getData("https://max-api.maicoin.com/api/v2/tickers/btcusdt", "last", 0)

ethCoinbasePrice = getData("https://api.coinbase.com/v2/prices/ETH-USD/buy", "data", "amount") 
ethBitoPrice = getData("https://api.bitopro.com/v3/tickers/eth_usdt", "data", 'lastPrice')
ethMaicoinPrice = getData("https://max-api.maicoin.com/api/v2/tickers/ethusdt", "last", 0)

timeDict = {'currentTime': current_time }
            
priceDict = {}

priceDict['btc'] = package_dict(btcCoinbasePrice, btcBitoPrice, btcMaicoinPrice)
priceDict['eth'] = package_dict(ethCoinbasePrice, ethBitoPrice, ethMaicoinPrice)
priceDict['time'] = timeDict

# write and dump data to json

export_JSON('../buyHighSellLow/static/style/js/btcPriceData.json', priceDict)
