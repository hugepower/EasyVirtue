'''
Author: hugepower
Date: 2021-02-28 22:13:23
LastEditors: hugepower
LastEditTime: 2021-02-28 22:51:43
Description: file content
'''
import httpx

print(
    httpx.get(
        "http://www.baidu.com",
        verify=False,
    ).text
)