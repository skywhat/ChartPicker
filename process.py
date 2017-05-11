#!/usr/bin/python
# coding=utf-8
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import time
import datetime as dt
import data_csv
from mpldatacursor import datacursor

#根据path指定的文件构造图标
class ConstructChart(object):
    def __init__(self,path):
        self.data_points=data_csv.data(path)
        self.test_time = self.data_points.dates
        self.test_timeArray = []
        for item in self.test_time:
            self.test_timeArray.append(int(time.mktime(time.strptime(item,"%m/%d/%Y %H:%M"))))
        self.values=self.data_points.values
        self.dates=[dt.datetime.fromtimestamp(ts) for ts in self.test_timeArray]
        self.datenums=md.date2num(self.dates)
        #self.dpi=100
        #self.fig=plt.Figure((3.0, 3.0), dpi=self.dpi)
        self.fig=plt.figure(figsize=(8,4))
        self.ax =self.fig.add_subplot(111)
        #self.fig,self.ax=plt.subplots()
        #self.ax=plt.subplot()
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        plt.gca()
        self.xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        self.ax.xaxis.set_major_formatter(self.xfmt)


        #There are a variety of meanings of the picker property https://matplotlib.org/examples/event_handling/pick_event_demo.html
        # markers example https://matplotlib.org/examples/lines_bars_and_markers/marker_reference.html
        self.line = plt.plot(self.datenums, self.values, '_', marker=r'8',picker=2)
        #点击其中的point显示x,y info
        datacursor(self.line)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        #plt.show()

    def on_pick(self,event):
        self.index = event.ind
        print 'onpick:', self.index, np.take(self.datenums, self.index), np.take(self.values, self.index)

if __name__=='__main__':
    path = "samples.csv"
    ConstructChart(path)
