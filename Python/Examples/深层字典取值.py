'''
Author: hugepower
Date: 2021-02-03 15:34:53
LastEditors: hugepower
LastEditTime: 2021-02-15 23:10:58
Description: file content
'''
from functools import reduce
""" 
python3 多层/深层字典取值，不存在时返回默认值

用到了reduce 函数实现
reduce函数的定义：
reduce(function, sequence [, initial] ) -> value
function参数是一个有两个参数的函数，reduce依次从sequence中取一个元素，和上一次调用function的结果做参数再次调用function。
第一次调用function时，如果提供initial参数，会以sequence中的第一个元素和initial作为参数调用function，否则会以序列sequence中的前两个元素做参数调用function。
"""
def get_from_dict(data_dict, map_list, defalut=None):
    def getitem(source, key):
        try:
            if isinstance(source, list):
                return source[int(key)]
            if isinstance(source, dict) and key not in source.keys():
                return defalut
        except IndexError:
            return defalut

        return source[key]

    if isinstance(map_list, str):
        map_list = map_list.split('.')

    return reduce(getitem, map_list, data_dict)


a = {
    'entry_data': {
        'hhh': 'hahah',
        'ProfilePage': [{
            'graphql': 'hhhh'
        }, {
            'graphql2': 'hhhh2'
        }]
    }
}
data_dict = 'entry_data.ProfilePage.0.graphql'  # or data_dict = ['entry_data', 'ProfilePage', 0]
res = get_from_dict(a, data_dict, 'hahahaaaa')

print(res)  # output: hhhh
