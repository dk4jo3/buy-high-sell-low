
from flask import Flask, render_template
import threading
import requests
import time
import datetime


app = Flask(__name__, template_folder="templates")

#sched = Scheduler()
#sched.start()

def get_data(url, dir, dir2):
    api_response = requests.get(url)
    if api_response.status_code != 200:
        api_price = 'error'
    else:
        api_data = api_response.json()
        if dir2 != 0:
            api_price = api_data[dir][dir2]
        else:
            api_price = api_data[dir]
        api_price = float(api_price)
        api_price = round(api_price, 2)
        return api_price

def unit_dif(p, cb):
    if isinstance(p, str) == True:
        return "---"
    else:
        result = round(p - cb, 2)
        return result

def percent_dif(p, cb):
    if isinstance(p, str) == True:
        return "---"
    else:
        result = round(((p - cb) / cb) * 100, 2)
        return result



def twd_usd(p, decimal):
    if isinstance(p, str) == True:
        return "___"
    else:
        twd_usd_rate = 31.0
        result = round(p / twd_usd_rate, decimal)
        return result


def add_price_sign(price):
    if price >= 0: 
        price = "+$" + str(price)
        return price
    else:
        price = price * -1
        price = "-$" + str(price)
        return price

def add_perc_sign(price):
    if price >= 0: 
        price = "+" + str(price)
        return price
    else:
        price = str(price)
        return price


price_dict = {
    'cb_price': 0,
    'mc_price': 0,
    'bito_price': 0,
    'bitopro_price': 0,
    'maimax_price': 0,
    'mc_perc_diff': 0,
    'mc_unit_diff': 0,
    'bito_perc_diff': 0,
    'bito_unit_diff': 0,
    'bitopro_perc_diff': 0,
    'bitopro_unit_diff': 0,
    'maimax_perc_diff': 0,
    'maimax_unit_diff': 0,
    'time_update': '',
}

def execute_order_66():
    price_dict['cb_price'] = get_data("https://api.coinbase.com/v2/prices/BTC-USD/buy", "data", "amount")

    price_dict['mc_price'] = get_data("https://api.maicoin.com/v1/prices/USD", "buy_price", 0)
    
    price_dict['bito_price'] = get_data("https://www.bitoex.com/api/v1/get_rate", "buy", 0)
    
    price_dict['maimax_price'] = get_data("https://max-api.maicoin.com/api/v2/tickers/btctwd", "last", 0)
    
    price_dict['bitopro_price'] = get_data("https://api.bitopro.com/v2/ticker/btc_twd", "lastPrice", 0)
    
    price_dict['bito_price'] = twd_usd(price_dict['bito_price'], 2)
    price_dict['bitopro_price'] = twd_usd(price_dict['bitopro_price'], 2)
    price_dict['maimax_price'] = twd_usd(price_dict['maimax_price'], 2)
    
    price_dict['mc_perc_diff'] = add_perc_sign(percent_dif(price_dict['mc_price'], price_dict['cb_price']))
    price_dict['mc_unit_diff'] = add_price_sign(unit_dif(price_dict['mc_price'], price_dict['cb_price']))
    
    price_dict['bito_perc_diff'] = add_perc_sign(percent_dif(price_dict['bito_price'], price_dict['cb_price']))
    price_dict['bito_unit_diff'] = add_price_sign(unit_dif(price_dict['bito_price'], price_dict['cb_price']))
    
    price_dict['bitopro_perc_diff'] = add_perc_sign(percent_dif(price_dict['bitopro_price'], price_dict['cb_price']))
    price_dict['bitopro_unit_diff'] = add_price_sign(unit_dif(price_dict['bitopro_price'], price_dict['cb_price']))

    price_dict['maimax_perc_diff'] = add_perc_sign(percent_dif(price_dict['maimax_price'], price_dict['cb_price']))
    price_dict['maimax_unit_diff'] = add_price_sign(unit_dif(price_dict['maimax_price'], price_dict['cb_price']))
    
    price_dict['time_update'] = datetime.datetime.now()
    price_dict['time_update'] = str(price_dict['time_update'])[:19]

    threading.Timer(66, execute_order_66).start()

execute_order_66()


@app.route("/hello")
def hello():
    return "Hello there, Gerneral Kenobi!"

@app.route("/")
@app.route("/index")
def index():
    user = {'username': price_dict['time_update']}
    #last_updated = {'time': price_dict['time_update']}
    posts = [
        {
            'market' : 'BitoEx',
            'price' : price_dict['bito_price'],
            'unit_diff' : price_dict['bito_unit_diff'],
            'percent_diff' : price_dict['bito_perc_diff'],
            'location' : '../static/style/img/facesbito-logo.png',
            'link' : "https://www.bitoex.com/",
            'btn_name' : 'LINK'
        },
        {
            'market' : 'Coinbase',
            'price' : price_dict['cb_price'],
            'unit_diff' : '0',
            'percent_diff' : '0',
            'location' : '../static/style/img/facescb-logo.png',
            'link' : 'https://www.coinbase.com/',
            'btn_name' : 'LINK'
        },
       {
            'market' : 'MaiCoin',
            'price' : price_dict['mc_price'],
            'unit_diff' : price_dict['mc_unit_diff'],
            'percent_diff' : price_dict['mc_perc_diff'],
            'location' : '../static/style/img/facesmc-logo.png',
            'link' : 'https://www.maicoin.com/en',
            'btn_name' : 'LINK'
        },
        {
            'market' : 'BitoPro',
            'price' : price_dict['bitopro_price'],
            'unit_diff' : price_dict['bitopro_unit_diff'],
            'percent_diff' : price_dict['bitopro_perc_diff'],
            'location' : '../static/style/img/bitopro-card-img.png',
            'link' : 'https://www.bitopro.com',
            'btn_name' : 'LINK'
        },
        {
            'market' : 'MaiMax',
            'price' : price_dict['maimax_price'],
            'unit_diff' : price_dict['maimax_unit_diff'],
            'percent_diff' : price_dict['maimax_perc_diff'],
            'location' : '../static/style/img/maimax-card-img.png',
            'link' : 'https://max.maicoin.com/',
            'btn_name' : 'LINK'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

if __name__ == "__main__":
    app.run(debug=True)
