#testing.py 

from bhsl import * 



cb_price = get_data("https://api.coinbase.com/v2/prices/BTC-USD/buy", "data", "amount") 

print (cb_price)
