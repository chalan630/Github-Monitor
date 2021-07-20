'''
Author: chalan630
Date: 2021-07-20 17:25:38
LastEditTime: 2021-07-20 17:47:41
Description: 
'''
import re
import requests
import time
import datetime


# 信息清洗
def advanceInfoCleanUp(res):
    index = 0
    # 加入敏感词
    sensitiveWord = ['pdf']
    descriptions = re.findall('"description":*.{1,200}"fork"', res)
    warn = 0
    for i in range(20):
        warn = 0
        temp = descriptions[i].lower()
        for word in sensitiveWord:
            if word in temp:
                warn = 1
                break
        if warn == 1:
            continue
        else:
            index = i
            break


    description = re.findall('"description":*.{1,200}"fork"', res)[index].replace("\",\"fork\"", '').replace(
                    "\"description\":\"", '')
    # 获取仓库URL
    url = re.findall('"svn_url":*.{1,200}"homepage"', res)[index].replace("\",\"homepage\"", '').replace(
                    "\"svn_url\":\"", '')
    

    return description,url


def getResponse(keyword_list, *args):
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
    
    for item in keyword_list:
        try:
            if item == "cve":
                year = datetime.datetime.now().year
                api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated".format(year)
            else:
                api = "https://api.github.com/search/repositories?q={}&sort=updated".format(item)
            
            res = requests.get(api).text
            time.sleep(5)
            if type == "basic":
                s = re.findall('"total_count":*.{1,10}"incomplete_results"', res)
                print(s)
                s1 = str(s).replace(',"incomplete_results"\']', "").replace('[\'"total_count":', "")
                basicList.append(s1)
            elif type == "advance":
                s = re.findall('"total_count":*.{1,10}"incomplete_results"', res)
                print(s)
                s1 = str(s).replace(',"incomplete_results"\']', "").replace('[\'"total_count":', "")
                description,url = advanceInfoCleanUp(res)
                newList.append(s1)
                descriptionList.append(description)
                urlList.append(url)
        except Exception as e:
            print(e, "github链接不通")



def getAdvanceInfo(keyword_list):
    print('开启本轮爬取:')
    newList = []
    descriptionList = []
    urlList = []
    getResponse(keyword_list, newList, urlList, descriptionList)
    return newList, urlList, descriptionList



def getBasicItem(keyword_list):
    print('获取关键词基准条目:')
    basicList = []
    getResponse(keyword_list, basicList)
    return basicList
