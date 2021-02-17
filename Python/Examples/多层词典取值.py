'''
Author: hugepower
Date: 2021-02-04 02:18:00
LastEditors: hugepower
LastEditTime: 2021-02-09 18:54:34
Description: file content
'''

weibo_mblog = {
    "pic_video":
    "4:000xTMIagx07K2gwScVF0f0f0100Ar2v0k01,3:000xTMI2dfrgK2gwScVF0f0f0100Ar2v0k01"
}
# 方法一
if weibo_mblog.__contains__("pic_video"):
    if weibo_mblog.get('pic_video') is not None:
        pic_videos = [x.split(":") for x in weibo_mblog.get('pic_video').split(',')]
        print("-----第一种写法-----")
        print(pic_videos)
# 方法二
pic_videos = weibo_mblog.get('pic_video')
if pic_videos is not None:
    pic_videos = [x.split(":") for x in pic_videos.split(',')]
    print("-----第二种写法-----")
    print(pic_videos)