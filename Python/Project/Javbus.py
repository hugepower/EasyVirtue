'''
Author: hugepower
Date: 2021-02-22 03:36:21
LastEditors: hugepower
LastEditTime: 2021-02-22 22:23:45
Description: 下载 javbus.com 的内容
'''

import json
import os
from contextlib import closing
from urllib.parse import urlencode

from lxml import etree
import pandas as pd
import requests

class Javbus(object):
    def __init__(self,download_path):
        self.download_path = download_path
        self.javbus_dict_path = os.path.join(download_path,"javbus_dict")
        self.javbus_markdown_path = os.path.join(download_path,"javbus_markdown")

    s = requests.Session()
    s.headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4424.0 Safari/537.36"
    }
    # 如能直连，取消本代理。
    s.proxies = {'https': 'http://127.0.0.1:1087'}

    def javbus_response(self, url):
        r = self.s.get(url)
        if r.status_code == 200:
            return r.text
        else:
            print(r.status_code)

    def javbus_parse(self,url):
        text = self.javbus_response(url)
        if text is not None:
            html = etree.HTML(text)
            javbus_dict = {}
            javbus_dict['識別碼'] = html.xpath("//div[@class='col-md-3 info']/p/span[2]/text()")[0]
            javbus_dict['發行日期'] = html.xpath("//div[@class='col-md-3 info']/p[2]/text()")[0].strip()
            javbus_dict['長度'] = html.xpath("//div[@class='col-md-3 info']/p[3]/text()")[0].strip()
            javbus_dict['導演'] = html.xpath("//div[@class='col-md-3 info']/p[4]/a/text()")[0].strip()
            javbus_dict['製作商'] = html.xpath("//div[@class='col-md-3 info']/p[5]/a/text()")[0].strip()
            javbus_dict['演員'] = html.xpath("//div[@class='col-md-3 info']/p/span[@class='genre']/a/text()")
            javbus_dict['封面图'] = html.xpath("//div[@class='col-md-9 screencap']/a/img/@src")[0]
            javbus_dict['标题'] = html.xpath("//div[@class='col-md-9 screencap']/a/img/@title")[0].strip()
            javbus_dict['预览图'] = html.xpath("//a[@class='sample-box']/@href")
            return javbus_dict

    def javbus_to_json(self,javbus_dict,filename):
        path = os.path.join(self.javbus_dict_path,filename + ".json")
        if os.path.isfile(path) is False:
            with open(path, "w+") as f:
                f.write(json.dumps(javbus_dict, indent=4, ensure_ascii=False))

    def javbus_to_markdown(self,javbus_dict,filename):
        #markdown_template = "# {}"
        path = os.path.join(self.javbus_markdown_path,filename + ".md")
        with open(path, "w+") as f:
            #| Bs | S |   |
            #|----|---|---|
            #| s  | S |   |
            f.write("# {}\n\n".format(filename))
            f.write("![{}]({})\n\n".format(filename,javbus_dict["封面图"]))
            f.write("| Javbus |  |\n")
            f.write("|----|---|\n")
            f.write("| 标题 | {} |\n".format(javbus_dict["标题"]))
            f.write("| 識別碼 | {} |\n".format(javbus_dict["識別碼"]))
            f.write("| 發行日期 | {} |\n".format(javbus_dict["發行日期"]))
            f.write("| 長度 | {} |\n".format(javbus_dict["長度"]))
            f.write("| 導演 | {} |\n".format(javbus_dict["導演"]))
            f.write("| 製作商 | {} |\n".format(javbus_dict["製作商"]))
            for name in javbus_dict["演員"]:
                f.write("| 演員 | {} |\n".format(name))
            f.write("\n\n")
            for img_src in javbus_dict["预览图"]:
                f.write("![{}]({})\n".format(filename,img_src))
        
    def javbus_main(self,url):
        javbus_dict = self.javbus_parse(url)
        javabus_format_name = "{},{}".format(javbus_dict["發行日期"],javbus_dict["識別碼"])
        self.javbus_to_json(javbus_dict, javabus_format_name)
        self.javbus_to_markdown(javbus_dict, javabus_format_name)

    def javbus_run(self,url):
        if os.path.isdir(self.javbus_dict_path) is False:
            os.makedirs(self.javbus_dict_path)
        if os.path.isdir(self.javbus_markdown_path) is False:
            os.makedirs(self.javbus_markdown_path)
        self.javbus_main(url)
        
if __name__ == "__main__":
    # /Users/你的用户名/Movies/
    path = os.path.join(os.environ['HOME'],"Movies")
    jb = Javbus(path)
    jb.javbus_run("https://www.javbus.com/KBI-054")
    