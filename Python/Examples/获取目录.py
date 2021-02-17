'''
Author: hugepower
Date: 2021-02-17 20:59:26
LastEditors: hugepower
LastEditTime: 2021-02-17 21:02:52
Description: file content
'''
import os
print(os.getcwd()) #获取当前工作目录路径
print(os.path.join(os.getcwd(),"hello.txt"))
print(os.path.abspath('.')) #获取当前工作目录路径
print(os.path.abspath('test.txt')) #获取当前目录文件下的工作目录路径
print(os.path.abspath('..')) #获取当前工作的父目录 ！注意是父目录路径
print(os.path.abspath(os.curdir)) #获取当前工作目录路径 