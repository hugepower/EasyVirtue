'''
Author: hugepower
Date: 2021-02-05 02:45:31
LastEditors: hugepower
LastEditTime: 2021-02-17 21:01:12
Description: file content
'''

#批量给键赋值

new_seq = {'Google': '', 'Runoob': '', 'Taobao': ''}
a = ['google', 'runoob', 'taobao']

c = dict(zip(new_seq.keys(), a))
print("批量给键赋值:\n{}\n".format(c))

# {'Google': 'google', 'Runoob': 'runoob', 'Taobao': 'taobao'}

#给可迭代对象赋值

a = ['google', 'runoob', 'taobao']
new_dic = dict.fromkeys(a, 1)
print("给可迭代对象赋值:\n{}\n".format(new_dic))

# {'google': 1, 'runoob': 1, 'taobao': 1}

#将俩列表组合字典
seq = ['Google', 'Runoob', 'Taobao']
a = ['google', 'runoob', 'taobao']
print("将俩列表组合字典:\n{}\n".format(list(zip(seq, a))))

# {'Google': 'google', 'Runoob': 'runoob', 'Taobao': 'taobao'}

#更新字典
##方式一：赋值的方法
new_dic = {'Google': 'google', 'Taobao': 'taobao'}
new_dic.update(Tianmao='tianmao', JinDong='jindong')
print("更新字典的方式一：赋值的方法:\n{}\n".format(new_dic))

# {'Google': 'google', 'Taobao': 'taobao', 'Tianmao': 'tianmao', 'JinDong': 'jindong'}

##方式二：列表中套元组
new_dic = {'Google': 'google', 'Taobao': 'taobao'}
new_dic.update([("Jack", "jack"), ("Tom", "tom")])
print("更新字典的方式二：列表中套元组:\n{}\n".format(new_dic))

# {'Google': 'google', 'Taobao': 'taobao', 'Jack': 'jack', 'Tom': 'tom'}

##方式三：zip关联俩列表
new_dic = {'Google': 'google', 'Taobao': 'taobao'}
a = ["Lisa", "Bruce"]
b = ["lisa", "bruce"]
new_dic.update(list(zip(a, b)))
print("更新字典的方式三：zip关联俩列表:\n{}\n".format(new_dic))

# {'Google': 'google', 'Taobao': 'taobao', 'Lisa': 'lisa', 'Bruce': 'bruce'}


