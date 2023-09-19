# -*- coding = utf-8 -*-
# @Time : 2021/12/20 20:12
# @Author : 沈奥 
# @File : Weather_spider.py
# @Software : PyCharm

# 导入模块
import requests # 题代浏览器进行网络请求
from lxml import etree # 进行数据预处理
import csv #写入csv文件

def getWeather(url):
    weather_info = []       # {'日期':...,'最高气温':...,'天气':...}
    # 请求头
    headers ={
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    # 发起请求

#url的规律 ... +年份 + 月份.html --指定年月的数据
for year in range(2015,2021):
    for month in range(1,13): #包头不含尾 1-12
        # 某年某月的天气信息
        # 三元表达式
        weather_time = str(year)+('0'+str(month) if month < 10 else str(month))
        url =f'https://lishi.tianqi.com/ezhou/{weather_time}.html'
        # 爬虫获取每个月的天气数据
        weather = getWeather(url)
