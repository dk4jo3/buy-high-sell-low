
def get_data(url, dir, dir2):
	import requests
	api_response = requests.get(url)
	api_data = api_response.json()
	if dir2 != 0:
		api_price = api_data[dir][dir2]
	else: 
		api_price = api_data[dir]
	api_price = float(api_price)
	api_price = round(api_price, 2)
	return api_price

def unit_dif(p, cb):
	result = round(p - cb, 2)
	return result

def percent_dif(p, cb):
	result = round(((p - cb) / cb) * 100, 2)
	return result 



cb_price = get_data("https://api.coinbase.com/v2/prices/BTC-USD/buy", "data", "amount") 
mc_price = get_data("https://api.maicoin.com/v1/prices/USD", "buy_price", 0)
bito_price = get_data("https://www.bitoex.com/api/v1/get_rate", "buy", 0)
bito_price = round(bito_price / 29.5, 2)
mc_perc_diff = percent_dif(mc_price, cb_price)
mc_unit_diff = unit_dif(mc_price, cb_price)
bito_perc_diff = percent_dif(bito_price, cb_price)
bito_unit_diff = unit_dif(bito_price, cb_price)
now = datetime.datetime.now()
now = str(now)[:19]

#print ("Current time:", now)
#print ("Coinbase price is USD, %s" % (cb_price))
#print ("Maicoin price is USD, %s" % (mc_price))
#print ("BitoEx price is USD, %s" % (bito_price))
#print ("=========================================")
#print ("Maicoin price is %s percent or %s dollars higher" % (mc_perc_diff, mc_unit_diff))
#print ("BitoEx price is %s percent or %s dollars higher" % (bito_perc_diff, bito_unit_diff))





