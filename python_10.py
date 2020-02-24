#!/usr/bin/python3

'''
获取北京天气
api: http://www.weather.com.cn/data/sk/101010100.html
'''

import requests

def get_weather():
    url = 'http://www.weather.com.cn/data/sk/101010100.html'
    result = requests.get(url)
    result.encoding = 'utf8'
    weather = result.json()['weatherinfo']
    data = ('''城市: %s
温度: %s ℃
风向: %s
风力: %s
湿度: %s
时间: %s
    ''' % (weather['city'], weather['temp'], weather['WD'], weather['WS'], weather['SD'], weather['time']))
    return data

if __name__ == '__main__':
    print(get_weather())