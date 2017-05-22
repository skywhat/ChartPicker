import matplotlib
matplotlib.use('WXAgg')
import wx
import data_csv
from mpldatacursor import datacursor
import time
import datetime as dt
import matplotlib.dates as md

import numpy as np
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

from matplotlib.figure import Figure
import csv

class GraphFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title=u'ChartPicker')
        #if you import the csvfile for the first time.
        #we would check it in function. on_button_import_click_event
        self.FIRST_TIME=True
        self.create_main_panel()

    def create_main_panel(self):
        self.panel=wx.Panel(self)
        self.fig=Figure()
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.axes=self.fig.add_subplot(111)
        self.axes.cla()

        #wxpython controls
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.vbox.Add(self.canvas,1,flag=wx.LEFT | wx.TOP | wx.GROW)

        #All figure windows come with a navigation toolbar, which can be used to navigate through the data set.
        #https://matplotlib.org/users/navigation_toolbar.html
        self.toolbar = NavigationToolbar(self.canvas)
        self.vbox.Add(self.toolbar,0,wx.EXPAND)

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_filePicker = wx.FilePickerCtrl(self.panel, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.m_button_import = wx.Button(self.panel,  -1, "import data now!")
        self.m_button_import.Bind(wx.EVT_BUTTON, self.on_button_import_click_event)

        self.hbox1.AddSpacer(100)
        self.hbox1.Add(self.m_filePicker,border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(145)
        self.hbox1.Add(self.m_button_import,border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)

        self.hbox2=wx.BoxSizer(wx.HORIZONTAL)

        #A list control presents lists in a number of formats
        #https://wxpython.org/Phoenix/docs/html/wx.ListCtrl.html
        self.list_ctrl = wx.ListCtrl(self.panel, size=(-1, 100),
                                     style=wx.LC_REPORT
                                           | wx.BORDER_SUNKEN
                                     )
        self.list_ctrl.InsertColumn(0, 'Num',width=50)
        self.num=0
        self.list_ctrl.InsertColumn(1, 'Date',width=130)
        self.list_ctrl.InsertColumn(2, 'Flow',width=130)

        self.vbox_inner=wx.BoxSizer(wx.VERTICAL)

        self.m_button_delete=wx.Button(self.panel, -1, "delete selected one")
        self.m_button_clear=wx.Button(self.panel,-1,"clear all")
        self.m_button_export = wx.Button(self.panel, -1, "export data now!")
        self.vbox_inner.Add(self.m_button_delete)
        self.vbox_inner.Add(self.m_button_clear)
        self.vbox_inner.Add(self.m_button_export)
        self.m_button_delete.Bind(wx.EVT_BUTTON,self.on_button_delete_click_event)
        self.m_button_export.Bind(wx.EVT_BUTTON, self.on_button_export_click_event)
        self.m_button_clear.Bind(wx.EVT_BUTTON, self.on_button_clear_click_event)

        self.hbox2.AddSpacer(100)
        self.hbox2.Add(self.list_ctrl)
        self.hbox2.AddSpacer(50)
        self.hbox2.Add(self.vbox_inner)


        self.vbox.Add(self.hbox2,0,flag=wx.ALIGN_LEFT|wx.TOP)

        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    #get the datasets from csvfile you have picked
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

    #set how to present x axis
    def set_x_axis(self):
        #Set the format of x axis
        self.xlabels=['Time... %i' % i for i in self.datenums]
        self.axes.set_xticklabels(self.xlabels,rotation=25)
        self.fig.subplots_adjust(bottom=0.2)
        self.xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        self.axes.xaxis.set_major_formatter(self.xfmt)
        # Set the format of x axis

    #how to deal with the point you have clicked
    def on_pick(self,event):
        #get the index of this point
        self.index = event.ind
        self.pick_data.append([self.data_points.dates[self.index[0]],self.values[self.index[0]]])

        #print 'onpick:', self.index, np.take(self.data_points.dates, self.index), np.take(self.values, self.index)
        point_item="Point %s" % self.num
        new_index=self.list_ctrl.InsertItem(self.num, point_item)

        self.list_ctrl.SetItem(new_index, 1,self.pick_data[-1][0])
        self.list_ctrl.SetItem(new_index, 2, self.pick_data[-1][1])
        #count the point you have clicked
        self.num += 1

    #how to deal with the file you have picked
    def on_button_import_click_event(self, event):
        if self.FIRST_TIME==True:
            self.FIRST_TIME=False
        else:
            # clear the figure
            self.axes.lines.pop(0)
            self.axes.clear()
        self.path = self.m_filePicker.GetPath()
        self.get_data(self.path)
        self.set_x_axis()

        # There are a variety of meanings of the picker property
        # https://matplotlib.org/examples/event_handling/pick_event_demo.html
        # markers example
        # https://matplotlib.org/examples/lines_bars_and_markers/marker_reference.html
        self.line=self.axes.plot(self.datenums, self.values, '_', marker=r'8',picker=1.5)
        #https://github.com/joferkington/mpldatacursor
        #mpldatacursor provides interactive "data cursors" (clickable annotation boxes) for matplotlib.
        datacursor(self.line)
        #collect the data you have clicked
        self.pick_data=[]
        self.get_data(self.path)
        self.set_x_axis()

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas.draw()
        self.Update()

    def on_button_delete_click_event(self,event):
        index=self.list_ctrl.GetFocusedItem()
        self.list_ctrl.DeleteItem(index)
        del self.pick_data[index]

    def on_button_clear_click_event(self,event):
        self.list_ctrl.DeleteAllItems()
        self.pick_data=[]
        self.num=0

    def on_button_export_click_event(self, event):
        f=file("export.csv","wb")
        writer=csv.writer(f)
        writer.writerow(['Date','Flow'])
        for row in self.pick_data:
            writer.writerow(row)
        f.close()

if __name__=='__main__':
    app=wx.App()
    app.frame=GraphFrame()
    app.frame.Show()
    app.MainLoop()