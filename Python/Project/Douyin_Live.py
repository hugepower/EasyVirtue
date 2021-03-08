'''
Author: hugepower
Date: 2021-03-08 15:41:17
LastEditors: hugepower
LastEditTime: 2021-03-08 23:13:00
Description: 获取抖音直播房间的dict
'''

import json
import re

import requests

"""
网上有类似的提取直播间m3u8链接的案例，但是他们的代码我不喜欢。
比如https://github.com/wbt5/real-url/blob/master/douyin.py
"""

def get_live_info(room_id):
    """
    "FULL_HD1": "蓝光",
    "HD1": "超清",
    "ORIGION": "原画",
    "SD1": "标清",
    "SD2": "高清"
    """
    text = requests.get(f"https://webcast.amemv.com/webcast/reflow/{room_id}").text
    json_str = re.search('(?<=window.__INIT_PROPS__ = )(.*?)(?=\<\/script)',text).group(0)
    douyin_live_dict = json.loads(json_str)
    room_dict = douyin_live_dict.get('/webcast/reflow/:id').get('room')
    room_info = {}
    room_info['room_id'] = room_dict.get('id')
    room_info['room_id_str'] = room_dict.get('id_str')
    room_info['room_create_time'] = room_dict.get('create_time')
    room_info['room_finish_time'] = room_dict.get('finish_time')
    room_info['room_m3u8'] = room_dict.get('stream_url').get('hls_pull_url_map').get('FULL_HD1')
    return room_dict,room_info

if __name__ == "__main__":
    #url = "https://webcast.amemv.com/webcast/reflow/6937173523291343651"
    get_live_info(6937173523291343651)