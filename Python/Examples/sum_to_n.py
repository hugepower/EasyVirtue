'''
Author: hugepower
Date: 2021-03-08 00:36:49
LastEditors: hugepower
LastEditTime: 2021-03-09 17:56:32
Description: file content
'''

from itertools import combinations

def sum_to_n(arr,n):
    """
    返回列表中两个元素的"和"为n的所有组合\n
    combinations(range(4), 3) --> (0,1,2), (0,1,3), (0,2,3), (1,2,3)
    """
    new_arr = [x for x in list(combinations(arr,2)) if sum(x) == n]
    return new_arr

if __name__ == '__main__':
    arr = [1, 2, 5, 6, 3,4]
    new_arr = sum_to_n(arr,7)
    print(new_arr)