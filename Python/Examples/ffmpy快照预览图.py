'''
Author: hugepower
Date: 2021-03-02 20:58:40
LastEditors: hugepower
LastEditTime: 2021-03-09 13:24:12
Description: 使用ffmpy来获取视频快照预览图
'''

from ffmpy import FFmpeg, FFprobe
from subprocess import PIPE
from PIL import Image
import os


class MyFFmpeg(object):
    def __init__(self, video_path, number):
        """
        初始化
        :video_path 视频路径
        :number 截图数量
        """
        self.number = number
        self.video_path = video_path
        self.video_name = os.path.basename(video_path)
        self.temp_path = video_path.replace(self.video_name, "")

    def get_playtime_from_video(self):
        """
        获取视频的播放时长
        """
        #ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i /Users/yefeng/macOS系统里的“其他”文件.mp4
        ff = FFprobe(
            global_options=
            '-v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1',
            inputs={self.video_path: None},
        )
        playtime = ff.run(stdout=PIPE, stderr=PIPE)[0].strip().decode('utf-8')
        return playtime

    def get_thumbnail_from_video(self):
        playtime = self.get_playtime_from_video()
        """
        生成视频的快照预览图
        """
        #ffmpeg -i 影片文件的路径 -vf fps=12/视频总时长 img%03d.png
        #ffmpeg -i video_path -ss 00:00:00.000 -vframes 1 thumbnail_path
        ff = FFmpeg(
            global_options=
            f'-vf fps={self.number}/{playtime} {self.temp_path}/img%03d.png',
            inputs={self.video_path: None},
        )
        ff.run()

    def run(self):
        self.get_thumbnail_from_video()


if __name__ == "__main__":
    video_path = "macOS系统里的“其他”文件.mp4"
    MyFFmpeg(video_path, 12).run()
