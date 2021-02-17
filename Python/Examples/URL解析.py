from urllib.parse import urlparse
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