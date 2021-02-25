'''
Author: hugepower
Date: 2021-02-25 21:23:38
LastEditors: hugepower
LastEditTime: 2021-02-25 21:46:51
Description: 格式化文件夹的名称
'''

"""
macOS 照片图库导出的相册的文件夹是【大理白族自治州, 2015年12月9日】的格式。
我希望调换他们的顺序，改成【2015年12月9日,大理白族自治州】的格式。
"""

import os

def dir_rename(path):
    """
    遍历路径下所有文件夹，含子目录里的文件夹，\n
    并将包含“,”字符的文件夹进行重命名
    """
    for root,dirs,files in os.walk(path):
        for dir in dirs:
            if "," in dir:
                dst_dirname = "{},{}".format(dir.split(",")[1].split(),dir.split(",")[0])
                # /Volumes/SN550/照片图库/大理白族自治州, 2015年12月9日
                src_path = os.path.join(root,dir)
                # /Volumes/SN550/照片图库/2015年12月9日,大理白族自治州
                dst_path = os.path.join(root,dst_dirname)
                os.rename(src_path , dst_path)
                print(src_path,dst_path)

if __name__ == '__main__':
    path = "/Volumes/SN550/照片图库"
    dir_rename(path)