'''
Author: hugepower
Date: 2021-02-19 21:08:55
LastEditors: hugepower
LastEditTime: 2021-02-22 20:42:09
Description: file content
'''
import base64
import json
from urllib.parse import urlencode

import requests

def get_short_link(url):
    s = requests.Session()
    s.headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4424.0 Safari/537.36",
        "cookie":"" #需要添加cookie值才能正常获取到信息
    }
    bytes_url = url.encode("utf-8")
    str_url = base64.b64encode(bytes_url) 
    sina_lt_api = "https://sina.lt/api.php?"
    params = {
        "from":"w",
        "url":str_url,
        "site":"dwz.date"
    }
    short_link_api = sina_lt_api + urlencode(params)
    print(short_link_api)
    r = s.get(short_link_api)
    if r.status_code == 200:
        sina_lt_dict = json.loads(r.text)
        print(sina_lt_dict)
        short_link = sina_lt_dict.get('data').get('short_url')
        return short_link

url = "https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd=288"
get_short_link(url)
