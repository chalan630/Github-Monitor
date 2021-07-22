'''
Modify: chalan630
Date: 2021-07-19 17:32:41
LastEditTime: 2021-07-22 20:06:05
GitHub: https://github.com/JustYoomoon/CVEAP
Description: 主函数
'''


import time,sys
import sendMessage
import getFunc


# 从文件中读取黑名单
def getBlackList():
    fileName = 'blackList.txt'
    black_list = []
    import os
    fp = os.path.exists(fileName)
    if fp == True:
        f = open(fileName, 'r')
        contents = f.readlines()
        for content in contents:
            content = content.strip('\n')
            black_list.append(content)
    return black_list


# 将黑名单写入文件
def setBlackList(black_list):
    fileName = 'blackList.txt'
    f = open(fileName, 'w')
    for content in black_list:
        f.write(content)
        f.write('\n')


def sendNews(keyword_list, proxy):
    print("初始化数据中！！！")
    # 基准关键词 条目表
    basicList = getFunc.getBasicItem(keyword_list, proxy)

    print("GitHub实时监控中 ...")

    print(basicList)
    black_list = getBlackList()
    while True:
        try:
            newList = []
            # 仓库URL 列表
            urlList = []
            # 描述信息列表
            descriptionList = []
            time.sleep(180)

            newList, urlList, descriptionList = getFunc.getAdvanceInfo(keyword_list, proxy)
            # 推送正文内容
            str(newList)
            str(urlList)
            str(descriptionList)
            # 推送标题
            text = r'GitHub监控消息提醒！！！'
            print(text)
            for index in range(len(basicList)):
                if basicList[index] != newList[index]:
                    if urlList[index] in black_list:
                        print(str(urlList[index]) + " 已经存在于黑名单中")
                    else:
                        msg ='\n更新了：' + str(keyword_list[index]) + '\n描述：' \
                            + str(descriptionList[index]) + '\nURL：' + str(urlList[index])
                        try:
                            # 三选一即可，没配置的 注释或者删掉
                            sendMessage.server(text, msg)
                            # sendMessage.dingding(text, msg)
                            sendMessage.tgbot(text,msg)
                            # sendMessage.mail(text, msg)
                        except BaseException:
                            continue
                        else:
                            print("正在添加到黑名单：" + str(urlList[index]))
                            black_list.append(str(urlList[index]))
                            print("添加成功！！！")
                else:
                    print(keyword_list[index] + "数据无更新！！！")
                    
            print(newList)

        except IndexError:
            print('GitHub暂时无法访问！！！')
            continue
        except KeyboardInterrupt:
            setBlackList(black_list)
            print('程序退出')
            sys.exit(0)
        

if __name__ == '__main__':
    keyword_list = ["免杀", "cve", "漏洞利用", "红队", "蓝队", "redteam", "取证", "应急响应", "后渗透", "内网", "攻防", "网络安全",
                    "主机安全", "信息收集", "溯源"]
    proxy = {
        '127.0.0.1': '7890'
    }
    sendNews(keyword_list, proxy)