import matplotlib
matplotlib.use('WXAgg')
import wx
import data_csv
from mpldatacursor import datacursor
import time
import datetime as dt
import matplotlib.dates as md

import process
import numpy as np
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

from matplotlib.figure import Figure

class GraphFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title=u'ChartPicker')
        path = "samples.csv"
        self.create_main_panel(path)

    def create_main_panel(self, path):
        self.panel=wx.Panel(self)
        self.fig=Figure()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.axes=self.fig.add_subplot(111)
        self.axes.cla()

        self.get_data(path)
        self.set_x_axis()

        self.line=self.axes.plot(self.datenums, self.values, '_', marker=r'8',picker=1.5)

        datacursor(self.line)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)

        #wxpython ctrl
        self.toolbar = NavigationToolbar(self.canvas)
        self.m_filePicker = wx.FilePickerCtrl(self.panel, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.m_button_import = wx.Button(self.panel,  -1, "import data now!")
        self.m_button_import.Bind(wx.EVT_BUTTON, self.on_button_import_click_event)

        self.hbox1=wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.m_filePicker,border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.m_button_import,border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.vbox=wx.BoxSizer(wx.VERTICAL)

        self.vbox.Add(self.canvas,1,flag=wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.toolbar,0,wx.EXPAND)
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)

        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def get_data(self, path):
        #CSV file data
        self.data_points=data_csv.data(path)
        self.test_time = self.data_points.dates
        self.test_timeArray = []
        for item in self.test_time:
            self.test_timeArray.append(int(time.mktime(time.strptime(item,"%m/%d/%Y %H:%M"))))
        self.values=self.data_points.values
        self.dates=[dt.datetime.fromtimestamp(ts) for ts in self.test_timeArray]
        self.datenums=md.date2num(self.dates)
        # CSV file data

    def set_x_axis(self):
        #Set the format of x axis
        self.xlabels=['Time %i' % i for i in self.datenums]
        self.axes.set_xticklabels(self.xlabels,rotation=25)
        self.fig.subplots_adjust(bottom=0.2)
        self.xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        self.axes.xaxis.set_major_formatter(self.xfmt)
        # Set the format of x axis

    def init_plot(self):
        self.chart=process.ConstructChart(path='samples.csv')

    def on_pick(self,event):
        self.index = event.ind
        print 'onpick:', self.index, np.take(self.datenums, self.index), np.take(self.values, self.index)

    def on_button_import_click_event(self, event):
        self.path=self.m_filePicker.GetPath()
        self.get_data(self.path)
        self.set_x_axis()

        self.line=self.axes.plot(self.datenums, self.values, '_', marker=r'8',picker=1.5)

        datacursor(self.line)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.Update()

if __name__=='__main__':
    app=wx.PySimpleApp()
    app.frame=GraphFrame()
    app.frame.Show()
    app.MainLoop()