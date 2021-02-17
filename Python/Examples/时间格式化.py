'''
Author: hugepower
Date: 2021-02-02 01:19:02
LastEditors: hugepower
LastEditTime: 2021-02-04 08:11:58
Description: 时间格式化
'''

import time
my_date = "Sat Nov 28 02:34:29 +0800 2020"

timeArray = time.strptime(my_date, "%a %b %d %H:%M:%S +0800 %Y")
img_Last_Modified = time.strftime('%Y%m%d%H%M%S', timeArray)
print(img_Last_Modified)  # Output: 20201128023429
timeStamp = int(time.mktime(timeArray))
print(timeStamp)  # Output: 1606502069
