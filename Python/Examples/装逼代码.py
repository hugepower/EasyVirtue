'''
Author: hugepower
Date: 2021-02-17 21:13:44
LastEditors: hugepower
LastEditTime: 2021-02-17 21:13:46
Description: file content
'''

#由于代码过于简单，让人容易看懂，体现不出自己多年的 Python 功力。
age = 40
if age > 18:
    print("已成年")
else:
    print("未成年")

# 于是有了以下代码
msg1 = ((age > 18) and ("已成年", ) or ("未成年", ))[0]
print(msg1)
msg2 = (lambda: "未成年", lambda: "已成年")[age > 18]()
print(msg2)