'''
Author: hugepower
Date: 2021-02-01 00:44:20
LastEditors: hugepower
LastEditTime: 2021-02-05 13:53:44
Description: 下载用户的微博内容
Statement: 代码很垃圾，尝试重写了三次，最终放弃了。将就着用吧。
'''

import os
import pandas as pd
import requests
import json
import time
from contextlib import closing
from urllib.parse import urlparse

s = requests.Session()
header = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3968.0 Safari/537.36'
}

def session_test(func, url):
    res = func.get(url=url, headers=header)
    return res

def new_user_dir(user_dirname):
    weibo_home_path = os.environ['HOME'] + "/Downloads/www.weibo.com/"
    weibo_user_path = os.path.join(weibo_home_path, user_dirname)
    weibo_dict_path = os.path.join(weibo_user_path, "Weibo_Dict")
    if os.path.isdir(weibo_dict_path) is False:
        os.makedirs(weibo_dict_path)
    return weibo_user_path


def download_file(url, path, time_stamp):
    try:
        filename = os.path.basename(path)
        if os.path.isfile(path) is False:
            with closing(s.get(url, stream=True)) as response:
                chunk_size = 30240
                content_size = int(response.headers['content-length'])
                data_count = 0
                with open(path, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)

                        data_count = data_count + len(data)
                        now_jd = (data_count / content_size) * 100
                        print("\r 【%s】下载进度：%d%%(%d/%d)" %
                              (filename, now_jd, data_count, content_size),
                              end="")
                os.utime(path, (time_stamp, time_stamp))
                print('\n【%s】下载完成!' % filename)
        else:
            print("「{}」已经下载过！".format(filename))
    except Exception as ex:
        print("Error message: %s" % ex)


def check_request_status(url):
    r = session_test(func=s, url=url)
    if r.status_code == 200:
        data_dict = json.loads(r.text)
        return data_dict
    else:
        print("r.status_code:{}".format(r.status_code))
        return None


def weibo_parse(weibo_dict, user_dirpath):
    mid_list = [weibo.get('mblog').get('mid') for weibo in weibo_dict]
    weibo_mblogs = []
    for mid in mid_list:
        url = "https://m.weibo.cn/statuses/show?id={}".format(mid)
        print(url)
        r = session_test(func=s, url=url)
        if r.status_code == 200:
            try:
                weibo_dict = json.loads(r.text)
                weibo_mblogs.append(weibo_dict.get('data'))
            except:
                pass
        else:
            print("r.status_code:{}".format(r.status_code))
        time.sleep(1)

    for weibo_mblog in weibo_mblogs:
        #uid = weibo.get('mblog').get('user').get('id')
        created_at = weibo_mblog.get('created_at')
        time_array = time.strptime(created_at, "%a %b %d %H:%M:%S +0800 %Y")
        time_stamp = int(time.mktime(time_array))  # 毫秒
        last_modified = time.strftime('%Y%m%d%H%M%S', time_array)
        #source = weibo_mblog.get('source')
        #text = weibo_mblog.get('text')
        #print("本条微博的视频信息{}".format(weibo_mblog.get('page_info')))
        #print("本条微博的图片信息{}".format(weibo_mblog.get('pics')))
        #print("本条微博的实况照片信息{}".format(weibo_mblog.get('pic_video')))
        video_urls = weibo_mblog.get("page_info", {}).get("urls")
        if video_urls is not None:
            # 感谢 TG中文交流群 @he19260817 提供的方法
            quality_rule = [
                'mp4_1080p_mp4', 'mp4_720p_mp4', 'mp4_720p',
                'hevc_mp4_hd', 'mp4_hd_mp4', 'mp4_hd', 'inch_4_mp4_hd',
                'inch_5_mp4_hd', 'inch_5_5_mp4_hd','ts_hd', 'hevc_mp4_ld','mp4_ld_mp4',
                'pre_ld_mp4', 'mp4_ld', 'ts_ld'
            ]
            quality_best = sorted(video_urls,
                                key=quality_rule.index)[0]
            quality_best_url = video_urls[quality_best]
            parsed = urlparse(quality_best_url)
            video_name = os.path.basename(parsed.path)
            video_filepath = os.path.join(
                user_dirpath, "{}_{}".format(last_modified,
                                            video_name))
            download_file(quality_best_url, video_filepath, time_stamp)

        pics = weibo_mblog.get('pics')
        if pics is not None:
            for pic in pics:
                pic_url = pic.get('large').get('url')
                pic_filepath = os.path.join(
                    user_dirpath, "{}_{}".format(last_modified,
                                                 os.path.basename(pic_url)))
                download_file(pic_url, pic_filepath, time_stamp)
        
        pic_video = weibo_mblog.get('pic_video')
        if pic_video is not None:
            pic_videos = [x.split(":") for x in pic_video.split(',')]
            for pic_video in pic_videos:
                livephoto_url = "https://video.weibo.com/media/play?livephoto=https://livephoto.us.sinaimg.cn/{}.mov".format(
                    pic_video[1])
                livephoto_format_name = "{}_{}.mov".format(
                    last_modified, pic_video[1])
                livephoto_path = os.path.join(user_dirpath,
                                                livephoto_format_name)
                download_file(livephoto_url, livephoto_path, time_stamp)

        dict_name = "{}_{}.json".format(last_modified, weibo_mblog.get('mid'))
        dict_path = os.path.join(user_dirpath, "Weibo_Dict", dict_name)
        with open(dict_path, "w+") as f:
            f.write(json.dumps(weibo_mblog, indent=4, ensure_ascii=False))
        os.utime(dict_path, (time_stamp, time_stamp))


def get_weibolist(weibo_nickname, weibo_uid, page, user_dirpath):

    url = "https://m.weibo.cn/api/container/getIndex?containerid=107603{}&page={}".format(
        weibo_uid, page)
    print(weibo_nickname, weibo_uid, page)
    data_dict = check_request_status(url)
    if not check_request_status(url) is None:
        if data_dict['ok'] == 1:
            weibo_parse(data_dict['data']['cards'], user_dirpath)
            get_weibolist(weibo_nickname, weibo_uid, page + 1, user_dirpath)
        else:
            print("「{},{}」已经爬取完毕！".format(weibo_nickname, weibo_uid))
    else:
        print("😭爬取频率过快，微博启动了反爬！")


if __name__ == '__main__':
    #weibo_userlist的数据列表格式：昵称,uid
    weibo_userlist_path = os.environ[
        'HOME'] + "/Desktop/EasyVirtue/weibo_userlist.txt"
    data = pd.read_table(weibo_userlist_path,
                         header=None,
                         names=["微博昵称", "微博uid"],
                         sep=",")
    print(data)
    data_dict = data.to_dict("records")

    for item in data_dict[0:1]:
        weibo_nickname = item["微博昵称"]
        weibo_uid = item["微博uid"]
        user_dirname = "{},{}".format(weibo_nickname, weibo_uid)
        user_dirpath = new_user_dir(user_dirname)
        #微博昵称，微博ID，从第1页开始下载，存储目录
        get_weibolist(weibo_nickname, weibo_uid, 1, user_dirpath)
