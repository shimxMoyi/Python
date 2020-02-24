#!/usr/bin/python3

'''钉钉机器人-天气助手'''

import requests
import json
import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus

def get_weather():
    url = 'http://www.weather.com.cn/data/sk/101010100.html'
    result = requests.get(url)
    result.encoding = 'utf8'
    weather = result.json()['weatherinfo']
    return [weather['city'], weather['temp'], weather['WD'], weather['WS'], weather['SD'], weather['time']]

def get_secret(secret):
    timestamp = int(round(time.time() * 1000))
    string_to_sign = '%s\n%s' % (timestamp, secret)
    hmac_code = hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    sign = quote_plus(base64.b64encode(hmac_code))
    return [timestamp, sign]

def ding_talk(url, secret, weather):
    url = url % (secret[0], secret[1])
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "今日天气情况",
            "text": "**城市:** %s \t\t" % weather[0] + "**温度:** %s ℃ \n\n" % weather[1] +
                    "**风向:** %s \t\t" % weather[2] + "**风力:** %s \n\n" % weather[3] +
                    "**湿度:** %s \t\t" % weather[4] + "**更新:** %s \n\n" % weather[5]
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)

if __name__ == '__main__':
    secret = 'SECa3cdb0fcd73cbdddba6ebc8f924342aab24b5efef3251b4b239d3470e21f6b4c'
    url = 'https://oapi.dingtalk.com/robot/send?access_token=51637853748be7fb18413312250d28cc82fe7904966b0a649da28d5a94eaeae4&timestamp=%s&sign=%s'
    weather = get_weather()
    secret = get_secret(secret)
    ding_talk(url, secret, weather)

