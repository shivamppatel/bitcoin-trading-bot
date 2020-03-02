import requests
import DateTime
import time
import json
import BinanceKey
from hashlib import sha256
from urllib.parse import urlencode
import hmac

# Information used for developing api calls was found at https://github.com/binance-exchange/binance-official-api-docs
# Each method that sends json in the api call uses the "data" variable to pass in json information 


apiKey = BinanceKey.BinanceKey1.get('api_key')
apiSecret = BinanceKey.BinanceKey1.get('api_secret')


baseApiUrl = 'https://api.binance.us'
connectivityEndpoint = '/api/v3/ping'
klineDataEndpoint = '/api/v3/klines'
testOrderEndpoint = '/api/v3/order/test'
tickerEndpoint = '/api/v3/ticker/price'
placeOrderEndpoint = '/api/v3/order'


#default header value
header = {'Content-type': 'application/json', 'Accept': 'application/json'}


#method used to get historical kline values, interval time can be changed. Also start and end time for data can be added to call
def getHistoricalData():
    url = baseApiUrl + klineDataEndpoint
    data = {'symbol': 'BTCUSDT', 'interval': '1m'}
    jsonData = json.loads(data)
    try:
        response = requests.get(url, data=jsonData, header = header)
        if(response.status_code == 200):
            return response
        else:
            return 'recieved error code '+ response.status_code + ' when attempting to retrieve historical kline data'
    except:
        return 'error making historical data call to Binanace Exchange'

#method makes call to ping endpoint, reccomended to check connectivity with this    
def testConnectivity():
    url = baseApiUrl + connectivityEndpoint
    try:
        response = requests.get(url)
        if(response.status_code == 200):
            return "connection is valid"
        else:
            return "error connecting to Binance exchange"
    
    except:
        return 'exception thrown while trying to ping binance exchange'

# Method makes call to the ticker endpoint, symbol can be subtituted with other symbols
def getLatestPrice():
    url = baseApiUrl + tickerEndpoint
    data = {"symbol": "BTCUSDT"}
    jsonData = json.loads(data)
    try:
        response = requests.get(url, data=jsonData)
        if(response.status_code == 200):
            return response
        else:
            return 'recieved error code '+ response.status_code + ' when attempting to retrieve ticker data'
    except:
        return 'exception thrown while trying to ping binance exchange'

#call to make a purchase
#makes purchase based on dollar amount being spent
def makePurchase(amt):
    url = baseApiUrl + placeOrderEndpoint
    data = {'symbol': 'BTCUSDT', 'side': 'BUY', 'type':'MARKET', 'quoteOrderQty': amt}
   

    #encodes order request
    m = hmac.new(apiSecret.encode('utf-8'), urlencode(data).encode('utf-8'), sha256)
    
    try:
        response = requests.post(url, data=m)
        if(response.status_code == 200):
            return response
        else:
            return 'recieved error code '+ response.status_code + ' when attempting to retrieve ticker data'
    except:
        return 'exception thrown while trying to ping binance exchange'
    

#call to test placing an order
def makeTestOrder():
    url = baseApiUrl + placeOrderEndpoint
    data = {'symbol': 'BTCUSDT', 'side': 'BUY', 'type':'MARKET', 'quoteOrderQty': 1000}
    

    #encodes order request
    m = hmac.new(apiSecret.encode('utf-8'), urlencode(data).encode('utf-8'), sha256)
    
    try:
        response = requests.post(url, data=m)
        if(response.status_code == 200):
            return response
        else:
            return 'recieved error code '+ response.status_code + ' when attempting to retrieve ticker data'
    except:
        return 'exception thrown while trying to ping binance exchange'


#call to make a sale
def makeSale():
    url = baseApiUrl + placeOrderEndpoint
    data = {'symbol': 'BTCUSDT', 'side': 'SELL', 'type':'MARKET', 'quoteOrderQty': 1000}
    

    #encodes order request
    m = hmac.new(apiSecret.encode('utf-8'), urlencode(data).encode('utf-8'), sha256)
    data.update({'signature': m})
    try:
        response = requests.post(url, data=m)
        if(response.status_code == 200):
            return response
        else:
            return 'recieved error code '+ response.status_code + ' when attempting to retrieve ticker data'
    except:
        return 'exception thrown while trying to ping binance exchange'



