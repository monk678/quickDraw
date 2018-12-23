# -*- coding: utf-8 -*-
# @Time    : 2018年12月19日 20:14
# @Author  : 李思原
# @Email   : shulisiyuan@163.com
# @File    : insertData.py
# @Software: PyCharm
# @Describe: 将quickdraw数据插入MongoDB中.


import jsonlines
from tqdm import tqdm
import os
from datetime import datetime
import pymongo
from colorama import Fore, Back, Style

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["quickDraw"]


# 获得x,y坐标，忽略笔画顺序
def plot_image(datas, word, key_id):
    xData = []
    yData = []
    for data in datas:
        x = data[0]
        y = data[1]
        for i in range(len(x)):
            xData.append(x[i])
            yData.append(y[i])
    return xData, yData


# 将数据插入MongoDB
def insertToMongo(fileName, mycol):
    mycol.ensure_index('key_id', unique=True)
    with jsonlines.open(fileName) as reader:
        for data in reader:
            word = data['word']
            key_id = data['key_id']
            try:
                xData, yData = plot_image(datas=data['drawing'], word=word, key_id=key_id)
                dataXY = {
                    'xData': xData,
                    'yData': yData
                }
                dataDict = dict(data, **dataXY)
                mycol.insert_one(dataDict)
            except:
                pass


def gci(filepath):
    # 遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in tqdm(files):
        print(Fore.YELLOW, fi)
        print(Style.RESET_ALL)
        t1 = datetime.now()

        fi_d = os.path.join(filepath, fi)
        keyWord = fi_d.split('.')[2].split('/')[-1]
        mycol = mydb[keyWord]
        try:
            insertToMongo(fileName=fi_d, mycol=mycol)
        except pymongo.errors.ServerSelectionTimeoutError:
            print(Fore.Red, 'MongoDB链接异常')
            break
        except FileNotFoundError:
            pass
        t2 = datetime.now()

        print(fi, '耗时：', (t2-t1))



if __name__ == '__main__':
    # #递归遍历/root目录下所有文件
    gci('../quickdraw_simplified')

    # file = '../quickdraw_simplified/strawberry.ndjson'
    # keyWord = file.split('.')[2].split('/')[-1]
    # print(keyWord)
    # mycol = mydb[keyWord]
    # #
    # insertToMongo(fileName=file, mycol=mycol)
