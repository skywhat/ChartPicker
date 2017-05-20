#!/usr/bin/python
# coding=utf-8
#从path指定的csv文件中获取数据
import csv
class data(object):
    def __init__(self,path):
        self.f=open(path, 'rb')
        self.reader=csv.reader(self.f)
        self.dates=[]
        self.values=[]
        for row in self.reader:
            if row[1] != '':
                self.dates.append(row[0])
                self.values.append(row[1])
        #删除csv文件第一行字符Date
        del self.dates[0]
        #删除csv文件第一行字符Flow
        del self.values[0]