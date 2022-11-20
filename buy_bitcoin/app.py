import requests
import json
import hmac
import hashlib
import time
from datetime import datetime
import os
import math


publicEndpoint = 'https://api.coin.z.com/public'
privateEndpoint = 'https://api.coin.z.com/private'

apiKey    = os.environ['API_KEY']
secretKey = os.environ['SECRET_KEY']


def lambda_handler(event, context):
    result = function()
    return {
        'statusCode': 200,
        'body': json.dumps(result, indent=2)
    }

def function():
    availableAmount = get_available_amount()
    
    ask = get_ask()
    
    availableAmount -= 3000
    n = 4
    size = math.floor((availableAmount * 10 ** n)  / ask) / (10 ** n)
    print(size)
    
    res = post_order(size)
    
    return res.json()

def get_available_amount():
    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    method    = 'GET'
    path      = '/v1/account/margin'

    text = timestamp + method + path
    sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

    headers = {
        "API-KEY": apiKey,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }

    res = requests.get(privateEndpoint + path, headers=headers)
    print (json.dumps(res.json(), indent=2))

    availableAmount = int(res.json()['data']['availableAmount'])
    return availableAmount
    
def get_ask():
    path     = '/v1/ticker?symbol=BTC'
    response = requests.get(publicEndpoint + path)
    print(json.dumps(response.json(), indent=2))

    ask = int(response.json()['data'][0]['ask'])
    return ask

def post_order(size):
    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    method    = 'POST'
    endPoint  = 'https://api.coin.z.com/private'
    path      = '/v1/order'
    reqBody = {
        "symbol": "BTC",
        "side": "BUY",
        "executionType": "MARKET",
        "size": str(size)
    }
    
    text = timestamp + method + path + json.dumps(reqBody)
    sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
    
    headers = {
        "API-KEY": apiKey,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }
    
    res = requests.post(endPoint + path, headers=headers, data=json.dumps(reqBody))
    print (json.dumps(res.json(), indent=2))
    
    return res