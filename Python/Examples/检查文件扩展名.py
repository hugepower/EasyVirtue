'''
Author: hugepower
Date: 2021-03-01 14:03:29
LastEditors: hugepower
LastEditTime: 2021-03-01 14:05:18
Description: 检查以扩展列表中存在的扩展名结尾的文件名
'''

extensions = ['.mp3','.m4a','.wma']
filenames = ['foo1.mp3','foo2.txt','foo3.m4a','foo4.mp4']
#方法一
for filename in filenames:
    for extension in extensions:
         if filename.endswith(extension):
             print(filename)
             break

#方法二：endswith接受一个元组,所以很容易：
exts = tuple(extensions)
result = [f for f in filenames if f.endswith(exts)]
print(result)