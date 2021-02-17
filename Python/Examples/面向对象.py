'''
Author: hugepower
Date: 2021-01-18 11:44:20
LastEditors: hugepower
LastEditTime: 2021-01-30 06:27:59
Description: file content
'''


class Student(object):

    def __init__(self, name, age):

        self.name = name
        self.age = age
    

    def study(self, course_name):
        print('%s正在学习%s.' % (self.name, course_name))
    
    def SayHello(self,text):
        print('%s正在对你说：%s.' % (self.name, text))
    
if __name__ == "__main__":

    DonaldJohnTrump = Student("Donald John Trump",72)

    DonaldJohnTrump.study("《葵花宝典》")
    DonaldJohnTrump.SayHello("你大爷！")