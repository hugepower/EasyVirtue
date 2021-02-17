'''
Author: hugepower
Date: 2021-02-03 03:51:01
LastEditors: hugepower
LastEditTime: 2021-02-17 21:01:45
Description: file content
'''
urls = {
		"mp4_1080p_mp4": "http:\/\/f.video.weibocdn.com\/0489AhZgx07Ilglbi1h01044204xV080E020.mp4?label=mp4_1080p&template=1280x720.25.0&trans_finger=775cb0ab963a74099cf9f840cd1987f1&ori=0&ps=1BThihd3VLAY5R&Expires=1612205822&ssig=NaT3ZjZ86W&KID=unistore,video",
		"mp4_720p_mp4": "http:\/\/f.video.weibocdn.com\/0489AhZgx07Ilglbi1h01041204xV080E020.mp4?label=mp4_720p&template=1280x720.25.0&trans_finger=775cb0ab963a74099cf9f840cd1987f1&ori=0&ps=1BThihd3VLAY5R&Expires=1612205822&ssig=NaT3ZjZ86W&KID=unistore,video",
        "mp4_hd_mp4": "http:\/\/f.video.weibocdn.com\/04dtDqqgx07Ilgi0R230104122o09H0E010.mp4?label=mp4_hd&template=852x480.25.0&trans_finger=d8257cc71422c9ad30fe69ce9523c87b&ori=0&ps=1BThihd3VLAY5R&Expires=1612205822&ssig=gE0Z%2FjNGml&KID=unistore,video",
        "mp4_ld_mp4": "http:\/\/f.video.weibocdn.com\/02KcEQfgx07IlginQ60104101mEPC0E010.mp4?label=mp4_ld&template=640x360.25.0&trans_finger=6006a648d0db83b7d9951b3cee381a9c&ori=0&ps=1BThihd3VLAY5R&Expires=1612205822&ssig=FycY1ZxuLI&KID=unistore,video"
}

#mp4_1080p_mp4 > mp4_720p_mp4 > mp4_hd_mp4 > mp4_ld_mp4

#方案一
quality_rule = ['mp4_1080p_mp4','mp4_720p_mp4','mp4_hd_mp4','mp4_ld_mp4']

print(sorted(urls, key=quality_rule.index))
print("\n------方案一---------")
quality_best = sorted(urls, key=quality_rule.index)[0]
#quality_best = max(urls, key=quality_rule.index)
print(urls[quality_best])

#方案二
url = urls.get("mp4_720p_mp4") or urls.get("mp4_1080p_mp4")
print("\n------方案二---------")
print(url)