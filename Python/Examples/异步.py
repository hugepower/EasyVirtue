'''
Author: hugepower
Date: 2021-02-06 12:14:06
LastEditors: hugepower
LastEditTime: 2021-02-06 12:14:16
Description: file content
'''
#https://www.cnblogs.com/shenh/p/9090586.html
#python异步编程之asyncio（百万并发）
#https://docs.python.org/zh-cn/3/library/asyncio.html
#asyncio --- 异步 I/O
import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

# Python 3.7+
asyncio.run(main())