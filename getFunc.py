'''
Author: chalan630
Date: 2021-07-20 17:25:38
LastEditTime: 2021-07-23 17:52:54
Description: 
'''
import re
import requests
import time
import datetime
import json


# 信息清洗
def advanceInfoCleanUp(resDic):
    index = 0
    # 加入敏感词
    sensitiveWord = ['pdf', 'test']
    warn = 0
    for i in range(20):
        warn = 0
        temp = resDic['items'][i]['description'].lower()
        temp_name = resDic['items'][i]['name'].lower()
        for word in sensitiveWord:
            if word in temp or word in temp_name:
                warn = 1
                break
        if warn == 1:
            continue
        else:
            index = i
            break

    # 获取仓库URL
    description = resDic['items'][index]['description']
    url = resDic['items'][index]['svn_url']
    

    return description,url


def getResponse(keyword_list, proxy, *args):
    type = ""
    # 可变参数
    if len(args) == 1:
        basicList = args[0]
        type = "basic"
    elif len(args) == 3:
        newList = args[0]
        urlList = args[1]
        descriptionList = args[2]
        type = "advance"

    i = 0    
    while i < len(keyword_list):
        try:
            if keyword_list[i] == "cve":
                year = time.localtime()[0]
                url = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated".format(year)
            else:
                url = "https://api.github.com/search/repositories?q={}&sort=updated".format(keyword_list[i])
            
            res = requests.get(url, proxy).text
            time.sleep(5)
            resDic = json.loads(res)
            if type == "basic":
                count = resDic['total_count']
                basicList.append(str(count))
            elif type == "advance":
                count = resDic['total_count']
                description,url = advanceInfoCleanUp(resDic)
                newList.append(str(count))
                descriptionList.append(str(description))
                urlList.append(str(url))
            print(keyword_list[i]+":"+str(count))
            i += 1
        except Exception:
            print(keyword_list[i], "github链接不通")
            time.sleep(10)


def getAdvanceInfo(keyword_list, proxy):
    localtime = time.asctime(time.localtime())
    print(localtime + '开启本轮爬取:')
    newList = []
    descriptionList = []
    urlList = []
    getResponse(keyword_list, proxy, newList, urlList, descriptionList)
    return newList, urlList, descriptionList


def getBasicItem(keyword_list, proxy):
    print('获取关键词基准条目:')
    basicList = []
    getResponse(keyword_list, proxy, basicList)
    return basicList
