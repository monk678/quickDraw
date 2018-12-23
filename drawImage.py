# -*- coding: utf-8 -*-
# @Time    : 2018年10月16日 下午9:34
# @Author  : 李思原
# @Email   : shulisiyuan@163.com
# @File    : drawImage.py
# @Software: PyCharm
# @Describe: 根据MongoDB中的数据画画


import pymongo
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from multiprocessing import Pool

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# 获取所有的画画名次类别
quickDrawdbcol = myclient["quickDraw"]
words = quickDrawdbcol.list_collection_names(session=None)
print(words)

# 获取所有的国家简称
countrycodesdb = myclient["dataSet"]
countrycodescol = countrycodesdb["countryCode"]
countrycodes = countrycodescol.distinct('code2')
print(countrycodes)


# 获取线条粗细
def getLineWidth(num):
    if num < 100:
        lineWidth = 0.5
    elif num < 1000:
        lineWidth = 0.01
    elif num < 10000:
        lineWidth = (10000 - num) / 100000 * 0.1
    elif num < 100000:
        lineWidth = (100000 - num) / 10000000 * 0.1
    else:
        lineWidth = 0.00001
    return lineWidth


def drawImageByWord(word, countrycode):
    imgSavePath = './image/total/'
    myquery = {"countrycode": countrycode}
    mydoc = quickDrawdbcol[word].find(myquery)
    plt.clf()

    print(quickDrawdbcol[word].count(myquery))

    if quickDrawdbcol[word].count(myquery) > 10:
        ChineseCountryName = countrycodescol.find_one({"code2": countrycode})['ChineseCountryName']
        EnglishCountryName = countrycodescol.find_one({"code2": countrycode})['EnglishCountryName']
        i = 0
        lineWidth = getLineWidth(num=quickDrawdbcol[word].count(myquery))
        imgSavePath = '%s/%s' % (imgSavePath, word)
        imgSaveName = ChineseCountryName + '_' + countrycode + '_' + EnglishCountryName + '_' + word + '_' + str(
            quickDrawdbcol[word].count(myquery)) + '_' + str(lineWidth)

        if not os.path.exists('%s/%s.png' % (imgSavePath, imgSaveName)):
            print('\n>>>>>>:', ChineseCountryName, EnglishCountryName, word, countrycode, 'count:',
                  quickDrawdbcol[word].count(myquery))
            for x in tqdm(mydoc):
                i += 1
                fig = plt.gcf()
                plt.axis('off')
                # plt.title(word + '_' + countrycode + '_' + quickDrawdbcol[word].count(myquery))
                plt.plot(x['xData'], x['yData'], color="black", linewidth=lineWidth)

            if not os.path.exists(imgSavePath):
                os.makedirs(imgSavePath)
            fig.savefig('%s/%s.png' % (imgSavePath, imgSaveName), dpi=200)
            plt.close(fig)
            print('图片%s保存成功', imgSaveName)
        else:
            print(imgSaveName, '文件已经存在')
    else:
        print(word, countrycode, '没有找到图片，或图片数据太少')


if __name__ == '__main__':
    # for word in words:
    #     # for countrycode in countrycodes:
    #     # print(word)
    #     # countrycode = 'US'
    #     # drawImageByWord(word=word, countrycode=countrycode)

    p = Pool(5)
    for word in words:
        print('/n>>>>>>>>>>>>>>>>>>>>/n开始处理关键字:%s' % word)
        for countrycode in countrycodes:
            p.apply_async(drawImageByWord, args=(word, countrycode))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
