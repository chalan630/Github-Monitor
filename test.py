'''
Author: chalan630
Date: 2021-07-22 18:41:55
LastEditTime: 2021-07-22 19:28:28
Description: 
'''

import json
import re
import requests


proxy = {
    '127.0.0.1': '7890'
}


url = "https://api.github.com/search/repositories?q=CVE-2021&sort=updated"

res = requests.get(url, proxies=proxy).text
list = json.loads(res)

test = list['items'][0]['svn_url']

print(test)
