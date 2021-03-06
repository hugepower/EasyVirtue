'''
Author: hugepower
Date: 2021-02-14 16:24:05
LastEditors: hugepower
LastEditTime: 2021-02-21 00:48:29
Description: 抖音视频下载
'''

import json
import os
from contextlib import closing
from urllib.parse import urlencode

import pandas as pd
import requests


class MyDouyin(object):
    def __init__(self, nickname, user_id, sec_uid, max_cursor):
        self.nickname = nickname
        self.user_id = user_id
        self.sec_uid = sec_uid
        self.max_cursor = max_cursor
        self.douyin_home_path = os.path.join(os.environ["HOME"],
                                             "Movies/www.douyin.com")
        self.user_home_path = os.path.join(self.douyin_home_path,
                                           "{},{}".format(nickname, user_id))
        self.user_dictDir_path = os.path.join(self.user_home_path,
                                              "douyin_dict")
        self.user_videosDir_path = os.path.join(self.user_home_path, "videos")

    s = requests.Session()
    s.headers = {
        "User-Agent":
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }

    def download_video(self, url, path, last_modified):
        filename = os.path.basename(path)
        temp_path = path + ".part"
        try:
            with closing(self.s.get(url, stream=True)) as response:
                chunk_size = 30240
                content_size = int(response.headers['content-length'])
                data_count = 0
                with open(temp_path, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)

                        data_count = data_count + len(data)
                        now_jd = (data_count / content_size) * 100
                        print("\r 【%s】下载进度：%d%%(%d/%d)" %
                              (filename, now_jd, data_count, content_size),
                              end="")
                if int(os.path.getsize(temp_path)) == content_size:
                    os.rename(temp_path, path)
                os.utime(path, (last_modified, last_modified))
                print('\n【%s】Download completed!' % filename)
        except Exception as ex:
            print("Error message: %s" % ex)
            self.download_video(url, path, last_modified)

    def download_aweme_dict(self, aweme_dict, file_name, last_modified):
        path = os.path.join(self.user_dictDir_path, file_name + ".json")
        if os.path.isfile(path) is False:
            with open(path, "w+") as f:
                f.write(json.dumps(aweme_dict, indent=4, ensure_ascii=False))
            os.utime(path, (last_modified, last_modified))

    def get_aweme_list_url(self, max_cursor):
        aweme_list_api = "https://www.iesdouyin.com/web/api/v2/aweme/post/?"
        params = {
            "sec_uid": self.sec_uid,
            "count": 21,
            "max_cursor": max_cursor,
            "aid": 1128,
            "_signature": "tPJ5fAAA1M.HBHMThwCZhrTyeW",
            "dytk":"",
        }
        aweme_list_url = aweme_list_api + urlencode(params)
        return aweme_list_url

    def get_video_url(self, video_id):
        video_url_api = "https://aweme-hl.snssdk.com/aweme/v1/play/?"
        params = {
            "video_id": video_id,
            "line": 0,
            "ratio": "720p",
            "watermark": 1,
            "media_type": 4,
            "vr_type": 0,
            "improve_bitrate": 0,
            "logo_name": "aweme_self"
        }
        video_url = video_url_api + urlencode(params)
        return video_url

    def get_last_modified(self, aweme_dict, max_cursor):
        uri = aweme_dict.get("video").get("origin_cover").get("uri")
        if "_" in uri:
            last_modified = int(uri.split("_")[1])
        else:
            last_modified = max_cursor / 1000
        return last_modified

    def get_video_id(self, aweme_dict):
        return aweme_dict.get("video").get("vid")

    def get_user_id(self, aweme_dict):
        return aweme_dict.get("author").get("uid")

    def get_douyin_dict(self, url):
        try:
            response = self.s.get(url)
            if response.status_code == 200:
                douyin_dict = response.json()
                return douyin_dict
        except self.s.ConnectionError as e:
            print('Error', e.args)

    def download_douyin(self, max_cursor, isEnd=False, update_download=False):
        aweme_list_url = self.get_aweme_list_url(max_cursor)
        print(aweme_list_url)
        douyin_dict = self.get_douyin_dict(aweme_list_url)
        next_max_cursor = douyin_dict.get("max_cursor")
        aweme_list_dict = douyin_dict.get("aweme_list")
        for aweme_dict in aweme_list_dict:
            video_id = self.get_video_id(aweme_dict)
            user_id = self.get_user_id(aweme_dict)
            last_modified = self.get_last_modified(aweme_dict, next_max_cursor)
            video_url = self.get_video_url(video_id)
            video_name = "user_{}_{}".format(user_id, video_id)
            video_save_path = os.path.join(self.user_videosDir_path,
                                           video_name + ".mp4")
            if os.path.isfile(video_save_path) is False:
                self.download_video(video_url, video_save_path, last_modified)
            else:
                isEnd = update_download
                print("「{}」已经存在!".format(video_name))
            self.download_aweme_dict(aweme_dict, video_name, last_modified)
        if douyin_dict.get("has_more") is True and isEnd is False:
            self.download_douyin(next_max_cursor)
        else:
            print("已经没有更多的视频可以下载了。")

    def douyin_run(self):
        if os.path.isdir(self.user_dictDir_path) is False:
            os.makedirs(self.user_dictDir_path)
        if os.path.isdir(self.user_videosDir_path) is False:
            os.makedirs(self.user_videosDir_path)
        self.download_douyin(self.max_cursor, update_download=True)


def read_userlist(path):

    data = pd.read_table(path,
                         header=None,
                         names=["nickname", "user_id", "sec_uid"],
                         sep=",")
    # dropping null value columns to avoid errors
    data.dropna(inplace=True)
    print(data)
    data_dict = data.to_dict("records")
    return data_dict


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "douyin_userlist.txt")
    userlist = read_userlist(path)
    for item in userlist[0:]:
        nickname = item.get("nickname")
        user_id = item.get("user_id")
        sec_uid = item.get("sec_uid")
        print("\n\n正在下载用户【{},{}】的所有视频\n\n".format(nickname, user_id))
        douyin = MyDouyin(nickname, user_id, sec_uid, 0)
        douyin.douyin_run()
