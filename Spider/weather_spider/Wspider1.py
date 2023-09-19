# -*- coding = utf-8 -*-
# @Time : 2021/12/20 21:50
# @Author : 沈奥 
# @File : Wspider.py
# @Software : PyCharm

import sqlite3
import urllib
import urllib.request
import time
from bs4 import BeautifulSoup

conn = sqlite3.connect("weather.db")  #直接在同级目录下创建名为weather的数据库
c = conn.cursor()
c.execute('''create table weather
            (positionId int not null,
            name text not null,
            date_time date not null,
            temperature int,
            rain int,
            humidity int,
            windDirection text,
            windPower int,
            fullName text not null,
            createTime text not null DEFAULT (datetime('now','localtime')));''')

def getPositionName(soup, num):  #soup：beautiful的soup对象，num城市编码
    position_name = soup.find(class_="crumbs")  #进入crumbs目录下
    name = []
    for i in range(len(position_name.find_all("a"))):
        name.append(position_name.find_all("a")[i].text)
        print(name)
    name.append(position_name.find_all("span")[len(position_name.find_all("span")) - 1].text)
    name_str = "-".join(name)
    print(name)
    return name_str

def spider(url, num):  # url，num：城市编码
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    res_data = soup.findAll('script')
    weather_data = res_data[3]
    fullName = getPositionName(soup, num)
    for x in weather_data:
        weather = x
    index_start = weather.find("{")
    index_end = weather.find(";")
    weather_str = weather[index_start:index_end]
    weather = eval(weather_str)
    weather_dict = weather["od"]
    weather_date = weather_dict["od0"]
    weather_position_name = weather_dict["od1"]
    weather_list = list(reversed(weather["od"]["od2"]))

    # 将数据存入数据库
    save_in_db(num, weather_date, weather_position_name, weather_list, fullName)
    return True

def save_in_db(num,weather_date, weather_position_name, weather_list, fullName):
    insert_list = []
    for item in weather_list:
        #od21小时，od22温度，od26降雨，od24风向，od25风力
        weather_item = {}
        weather_item['time'] = item['od21']
        weather_item['temperature'] = item['od22']
        weather_item['rain'] = item['od26']
        weather_item['humidity'] = item['od27']
        weather_item['windDirection'] = item['od24']
        weather_item['windPower'] = item['od25']
        weather_item['od23'] = item['od23']
        insert_list.append(weather_item)
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    for item in insert_list:
        c.execute("insert into weather (positionId,name,date_time,temperature,rain,humidity,windDirection,windPower,fullName) \
            values(?,?,?,?,?,?,?,?,?)", (num, weather_position_name, item['time'], item['temperature'], item['rain'], item['humidity'], item['windDirection'], item['windPower'], fullName))
    conn.commit()
    conn.close()




def start():
    base_url = "http://www.weather.com.cn/weather1d/101"
    province_num = 5
    while(province_num < 35):
        city_num = 1
        position_num = 1
        while (city_num < 25):
            try:
                num_str = str(province_num).zfill(2) + str(city_num).zfill(2) + str(position_num).zfill(2)
                url = base_url + num_str + ".shtml"
                time.sleep(1)
                print(url)
                flag = spider(url, num_str)
                position_num += 1
            except IndexError:
                position_num = 1
                city_num += 1
            except KeyError:
                position_num = 1
                city_num += 1
        province_num += 1

if __name__ == "__main__":
    start()
