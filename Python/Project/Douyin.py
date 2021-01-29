import os
import requests
import time
import json
import re
from contextlib import closing
import pandas as pd

json_dir_path = os.environ["HOME"] + "/Movies/www.douyin.com/Json_Data"
video_dir_path = os.environ["HOME"] + "/Movies/www.douyin.com/Videos"

s = requests.Session()
s.headers = {
    "User-Agent":
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}
''' 读取用户列表 '''


def read_userlist(path):
    data = pd.read_table(path,
                         header=None,
                         names=["user_id", "sec_uid"],
                         sep=",")
    # dropping null value columns to avoid errors
    data.dropna(inplace=True)
    print(data)
    data_dict = data.to_dict("records")
    return data_dict


''' 保存视频信息 '''


def save_json(json_data, filename, last_modified):

    json_file_path = os.path.join(json_dir_path, filename + ".json")
    with open(json_file_path, "w+") as f:
        f.write(json.dumps(json_data, indent=4, ensure_ascii=False))
    os.utime(json_file_path, (last_modified, last_modified))


''' 下载视频文件 '''


def download_file(url, filename, last_modified):
    try:
        with closing(s.get(url)) as response:
            chunk_size = 30240
            content_size = int(response.headers["content-length"])
            data_count = 0
            with open(os.path.join(video_dir_path, filename), "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    data_count = data_count + len(data)
                    now_jd = (data_count / content_size) * 100
                    print("\r 【%s】文件下载进度：%d%%(%d/%d)" %
                          (filename, now_jd, data_count, content_size),
                          end="")
            os.utime(os.path.join(video_dir_path, filename),
                     (last_modified, last_modified))
            if content_size < 200:
                download_file(url, filename, last_modified)
                print("重新下载")

        print("\n")
    except Exception as ex:
        print("错误的消息: %s" % ex)


''' 获取视频列表 '''


def get_videolist(user_id, sec_uid, max_cursor, isEnd):
    json_url = (
        "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=%s&count=21&max_cursor=%s&aid=1128&_signature=&"
        % (sec_uid, max_cursor))
    print(user_id, sec_uid, max_cursor)
    while isEnd:
        json_data = json.loads(s.get(json_url).text)
        if json_data["has_more"] is True:
            print(json_url)
            for item in json_data["aweme_list"]:
                try:
                    video_id = item["video"]["play_addr"]["uri"]
                    max_cursor = json_data['max_cursor']
                    user_id = item["author"]["uid"]
                    if "_" in item["video"]["origin_cover"]["uri"]:
                        last_modified = int(
                            item["video"]["origin_cover"]["uri"].split("_")[1])
                    else:
                        last_modified = max_cursor / 1000
                    video_uri = (
                        "https://aweme-hl.snssdk.com/aweme/v1/play/?video_id="
                        + video_id +
                        "&line=0&ratio=720p&watermark=1&media_type=4&vr_type=0&improve_bitrate=0&logo_name=aweme_self"
                    )
                    video_name = "user_" + user_id + "_" + video_id
                    if (os.path.isfile(
                            os.path.join(video_dir_path, video_name + ".mp4"))
                            is False):
                        download_file(video_uri, video_name + ".mp4",
                                      last_modified)
                        save_json(item, video_name, last_modified)
                    else:
                        print("「%s」文件已存在！" % video_name)
                        isEnd = False
                except Exception as ex:
                    print(ex, last_modified, video_uri,
                          item["video"]["origin_cover"])
            # break
            get_videolist(user_id, sec_uid, max_cursor, isEnd)


''' 扩展短链接 '''


def revertShortLink(url):
    res = s.head(url)
    newUrl = res.headers.get('location')
    if newUrl is None:
        return url
    else:
        return newUrl


''' 提取链接信息 '''


def get_url_info(url):
    url = revertShortLink(url)
    sec_uid_search = re.compile(r"sec_uid=(.*?)&")
    sec_uid = re.search(sec_uid_search, url).group(1)
    print(sec_uid)

    user_id_search = re.compile(r"user/(.*?)\?")
    user_id = re.search(user_id_search, url).group(1)
    print(user_id)


''' 程序主方法 '''


def douyin_main(path):
    userlist_dict = read_userlist(path)
    for item in reversed(userlist_dict[0:]):
        user_id = item["user_id"]
        sec_uid = item["sec_uid"]
        get_videolist(user_id, sec_uid, 0, True)


if __name__ == "__main__":
    path = os.environ[
        "HOME"] + "/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/douyin_userlist.txt"
    douyin_main(path)
