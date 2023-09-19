# -*- coding = utf-8 -*-
# @Time : 2021/12/20 22:47
# @Author : 沈奥 
# @File : test2.py
# @Software : PyCharm
import requests
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
}


def getCitySign() -> dict:
    r = requests.get('http://www.cma.gov.cn/',headers=headers)
    if r.status_code != 200:
        print('访问气象局网站错误！')
        return None
    r.encoding = r.apparent_encoding

    city = re.findall('c\[\d{,2}\] = new Array\("选择城市",(.*?)\)',r.text)
    city = re.findall('"([\u4e00-\u9fa5]*?)"',str(city))
    # 不存在佛山的网页
    city.remove('佛山')

    sign = re.findall('n\[\d{,2}\] = new Array.*?\("0",(.*?)\)',r.text,re.S)
    sign = re.findall('"(\d*?)"',str(sign))

    city_sign = dict(zip(city,sign))
    return city_sign


def getCityInfo(url:str) ->(list,list,list,list):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    # 时间，需要反转一下，因为最后一条数据对应第一个
    _time = re.findall('"od21":"(.*?)"',response.text)
    _time.reverse()
    _time[24] = _time[24] + ' '
    # 温度
    _temp = re.findall('"od22":"(.*?)"',response.text)
    _temp.reverse()
    # 湿度
    _humidity = re.findall('"od27":"(.*?)"',response.text)
    _humidity.reverse()
    # 空气质量
    _air = re.findall('"od28":"(.*?)"',response.text)
    _air.reverse()

    return _time,_temp,_humidity,_air


city_list = getCitySign()

while 1:
    query_city = input("输入查询的城市：")
    try:
        city_sign = city_list[query_city]
    except KeyError as e:
        print("无此城市信息，请重新输入！")
    else:
        break

url = 'http://www.weather.com.cn/html/weather/%s.shtml'%city_sign

time_ ,temp_ ,hum_ ,air_ = getCityInfo(url)


os.system(os.getcwd()+'\\'+query_city+"气温变化图.html")
