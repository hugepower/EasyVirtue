'''
Author: hugepower
Date: 2021-02-05 09:22:43
LastEditors: hugepower
LastEditTime: 2021-02-06 13:21:20
Description: 微博下载
'''
import os
import pandas as pd
import requests
import json
import time
from contextlib import closing
from urllib.parse import urlparse


class MyWeibo(object):
    def __init__(self, weibo_usernick, weibo_uid, page, weibo_path):
        self.weibo_usernick = weibo_usernick
        self.weibo_uid = weibo_uid 
        self.page = page
        self.weibo_path = weibo_path
        self.weibo_user_dirpath = os.path.join(
            weibo_path, "{},{}".format(weibo_usernick, weibo_uid))
        self.weibo_dict_path = os.path.join(self.weibo_user_dirpath, "Weibo_Dict")

    s = requests.Session()
    s.headers = {
        'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3968.0 Safari/537.36'
    }

    def weibo_response(self, url):
        r = self.s.get(url)
        if r.status_code == 200:
            try:
                weibo_dict = json.loads(r.text)
                return weibo_dict
            except:
                pass
        elif r.status_code == 418:
            print("微博已启动反爬")
        else:
            print("status code：{}".format(r.status_code))

    def download_file(self, url, path, time_stamp):
        try:
            filename = os.path.basename(path)
            if os.path.isfile(path) is False:
                temp_path = path + ".part"
                with closing(self.s.get(url, stream=True)) as response:
                    chunk_size = 30240
                    content_size = int(response.headers['content-length'])
                    data_count = 0
                    with open(temp_path, "wb") as file:
                        for data in response.iter_content(
                                chunk_size=chunk_size):
                            file.write(data)

                            data_count = data_count + len(data)
                            now_jd = (data_count / content_size) * 100
                            print("\r 【%s】下载进度：%d%%(%d/%d)" %
                                  (filename, now_jd, data_count, content_size),
                                  end="")
                    if int(os.path.getsize(temp_path)) == content_size:
                        os.rename(temp_path, path)
                    os.utime(path, (time_stamp, time_stamp))
                    print('\n【%s】下载完成!' % filename)
            else:
                print("「{}」已经下载过！".format(filename))
        except Exception as ex:
            print("Error message: %s" % ex)

    def weibo_parse(self, weibo_dict):
        weibo_cards = weibo_dict.get('cards')
        for card in weibo_cards:
            weibo_mid = card.get('mblog').get('mid')
            weibo_mid_url = "https://m.weibo.cn/statuses/show?id={}".format(
                weibo_mid)
            weibo_mblog = self.weibo_response(weibo_mid_url)
            if weibo_mblog is not None:
                weibo_created_at = weibo_mblog.get('data').get('created_at')
                #weibo_text = weibo_mblog.get('data').get('text')
                #weibo_source = weibo_mblog.get('data').get('source')
                time_array = time.strptime(weibo_created_at,
                                           "%a %b %d %H:%M:%S +0800 %Y")
                time_stamp = int(time.mktime(time_array))  # 毫秒
                last_modified = time.strftime('%Y%m%d%H%M%S', time_array)

                weibo_video_urls = weibo_mblog.get('data').get(
                    "page_info", {}).get("urls")
                if weibo_video_urls is not None:
                    quality_rule = [
                        'mp4_1080p_mp4', 'mp4_720p_mp4', 'mp4_720p',
                        'hevc_mp4_hd', 'mp4_hd_mp4', 'mp4_hd', 'inch_4_mp4_hd',
                        'inch_5_mp4_hd', 'inch_5_5_mp4_hd', 'ts_hd',
                        'hevc_mp4_ld', 'mp4_ld_mp4', 'pre_ld_mp4', 'mp4_ld',
                        'ts_ld'
                    ]
                    quality_best = sorted(weibo_video_urls,
                                          key=quality_rule.index)[0]
                    quality_best_url = weibo_video_urls[quality_best]
                    parsed = urlparse(quality_best_url)
                    video_name = os.path.basename(parsed.path)
                    video_filepath = os.path.join(
                        self.weibo_user_dirpath,
                        "{}_{}".format(last_modified, video_name))
                    #print("微博视频:{}".format(video_name))
                    self.download_file(quality_best_url, video_filepath,
                                       time_stamp)

                weibo_pics = weibo_mblog.get('data').get('pics')
                if weibo_pics is not None:
                    for pic in weibo_pics:
                        pic_url = pic.get('large').get('url')
                        pic_name = os.path.basename(pic_url)
                        pic_filepath = os.path.join(
                            self.weibo_user_dirpath,
                            "{}_{}".format(last_modified,
                                           os.path.basename(pic_url)))
                        self.download_file(pic_url, pic_filepath, time_stamp)
                        #print("普通照片:{}".format(pic_name))

                pic_video = weibo_mblog.get('data').get('pic_video')
                if pic_video is not None:
                    pic_videos = dict(
                        map(lambda x: x.split(":"), pic_video.split(",")))
                    for v in pic_videos.values():
                        pic_video_url = "https://video.weibo.com/media/play?livephoto=https://livephoto.us.sinaimg.cn/{}.mov".format(
                            v)
                        pic_video_format_name = "{}_{}.mov".format(
                            last_modified, v)
                        pic_video_path = os.path.join(self.weibo_user_dirpath,
                                                      pic_video_format_name)
                        self.download_file(pic_video_url, pic_video_path,
                                           time_stamp)
                        #print("实况照片:{}".format(pic_video_format_name))

                mblog_dict_name = "{}_{}.json".format(
                    last_modified,
                    weibo_mblog.get('data').get('mid'))
                mblog_dict_path = os.path.join(self.weibo_dict_path,
                                               mblog_dict_name)
                with open(mblog_dict_path, "w+") as f:
                    f.write(
                        json.dumps(weibo_mblog, indent=4, ensure_ascii=False))
                os.utime(mblog_dict_path, (time_stamp, time_stamp))

    def weibo_download(self, page):
        url = "https://m.weibo.cn/api/container/getIndex?containerid=107603{}&page={}".format(
            self.weibo_uid, page)
        print(url)
        weibo_dict = self.weibo_response(url)
        if weibo_dict.get('ok') == 1:
            self.weibo_parse(weibo_dict.get('data'))
            self.weibo_download(page + 1)
        else:
            print(weibo_dict)
            print("「{},{}」爬取完毕!\n\n".format(self.weibo_usernick,
                                            self.weibo_uid))

    def weibo_run(self):
        if os.path.isdir(self.weibo_dict_path) is False:
            os.makedirs(self.weibo_dict_path)
        self.weibo_download(self.page)


if __name__ == "__main__":
    weibo_userlist_path = os.environ[
        'HOME'] + "/Desktop/EasyVirtue/weibo_userlist.txt"
    weibo_save_path = os.path.join(os.environ['HOME'], "Downloads",
                                   "www.weibo.com")
    data = pd.read_table(weibo_userlist_path,
                         header=None,
                         names=["微博昵称", "微博uid"],
                         sep=",")
    print(data)
    data_dict = data.to_dict("records")

    for item in data_dict[0:1]:
        weibo = MyWeibo(item["微博昵称"], item["微博uid"], 1, weibo_save_path)
        print("\n{}\n".format(weibo.weibo_user_dirpath))
        print("\n{}\n".format(weibo.weibo_dict_path))
        weibo.weibo_run()
