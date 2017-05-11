import wx
import matplotlib.pyplot as plt
import process
import numpy as np
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

class BoundControlBox(wx.Panel):

    title='ChartPicker'

    def __init__(self,parent,ID,label,initval):
        wx.Panel.__init__(self,None, -1, self.title)
        self.value = initval

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.radio_auto = wx.RadioButton(self, -1,
                                         label="Auto", style=wx.RB_GROUP)
        self.radio_manual = wx.RadioButton(self, -1,
                                           label="Manual")
        self.manual_text = wx.TextCtrl(self, -1,
                                       size=(35, -1),
                                       value=str(initval),
                                       style=wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_UPDATE_UI, self.on_update_manual_text, self.manual_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)

        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.radio_manual, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(self.radio_auto, 0, wx.ALL, 10)
        sizer.Add(manual_box, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def on_update_manual_text(self, event):
        self.manual_text.Enable(self.radio_manual.GetValue())

    def on_text_enter(self, event):
        self.value = self.manual_text.GetValue()

    def is_auto(self):
        return self.radio_auto.GetValue()

    def manual_value(self):
        return self.value

class GraphFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title=u'ChartPicker')
        self.create_main_panel()

    def create_main_panel(self):
        self.panel=wx.Panel(self)
        self.init_plot()
        self.canvas=FigCanvas(self.panel,-1,self.chart.fig)

        self.toolbar = NavigationToolbar(self.canvas)

        self.m_filePicker = wx.FilePickerCtrl(self.panel, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)

        self.m_button = wx.Button(self.panel,  -1, "Pause")

        self.hbox1=wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.m_filePicker,border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.m_button,border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.vbox=wx.BoxSizer(wx.VERTICAL)

        self.vbox.Add(self.canvas,1,flag=wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.toolbar,0,wx.EXPAND)
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)

        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def init_plot(self):
        self.chart=process.ConstructChart(path='samples.csv')


class MyApp(wx.App):
    def OnInit(self):
        self.frame=GraphFrame()
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True

if __name__=='__main__':
    app=wx.PySimpleApp()
    app.frame=GraphFrame()
    app.frame.Show()
    app.MainLoop()