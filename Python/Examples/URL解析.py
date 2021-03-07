'''
Author: hugepower
Date: 2021-02-03 03:38:43
LastEditors: hugepower
LastEditTime: 2021-03-07 11:34:14
Description: file content
'''
from urllib.parse import urlparse,parse_qs
import os

url1 = "http:\/\/f.video.weibocdn.com\/002KcEQfgx07IlginQT601041201mEPC0E010.mp4?label=mp4_ld&template=640x360.25.0&trans_finger=6006a648d0db83b7d9951b3cee381a9c&ori=0&ps=1BThihd3VLAY5R&Expires=1612298351&ssig=GwDMPtOB39&KID=unistore,video"

parsed = urlparse(url1)
print('scheme  :', parsed.scheme)
print('netloc  :', parsed.netloc)
print('path    :', parsed.path)
print('os.path.basename:', os.path.basename(parsed.path))
print('params  :', parsed.params)
print('query   :', parsed.query)
print('fragment:', parsed.fragment)
print('username:', parsed.username)
print('password:', parsed.password)
print('hostname:', parsed.hostname)
print('port    :', parsed.port)
# 将字符串转换为字典
params = parse_qs(parsed.query)
print('params    :', params)
"""所得的字典的value都是以列表的形式存在，若列表中都只有一个值"""
result = {key: params[key][0] for key in params}
print('将字符串转换为字典 :',result)