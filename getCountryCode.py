# -*- coding: utf-8 -*-
# @Time    : 2018年12月23日 12:34
# @Author  : 李思原
# @Email   : shulisiyuan@163.com
# @File    : getCountryCode.py
# @Software: PyCharm
# @Describe: Please describe the code here.

import requests
from bs4 import BeautifulSoup
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dataSet"]
mycol = mydb["countryCode"]

url = 'http://doc.chacuo.net/iso-3166-1'

html = requests.get(url).text
html = BeautifulSoup(html, 'lxml')

datas = html.find('tbody').find_all('tr')

for data in datas:
    data = data.find_all('td')
    code2 = data[0].text
    code3 = data[1].text
    number = data[2].text
    ISOCode = data[3].text
    EnglishCountryName = data[4].text
    ChineseCountryName = data[5].text
    TaiwanCountryName = data[6].text
    HongKongCountryName = data[7].text

    data = {
        'code2': code2,
        'code3': code3,
        'number': number,
        'ISOCode': ISOCode,
        'EnglishCountryName': EnglishCountryName,
        'ChineseCountryName': ChineseCountryName,
        'TaiwanCountryName': TaiwanCountryName,
        'HongKongCountryName': HongKongCountryName,
    }
    try:
        mycol.ensure_index('EnglishCountryName', unique=True)
        mycol.insert_one(data)
        print(EnglishCountryName, ChineseCountryName, code2)
    except:
        pass
