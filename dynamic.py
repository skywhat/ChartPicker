import wx
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)

        self.panel = FigCanvas(self, -1, Figure())
        axes = self.panel.figure.gca()
        axes.cla()
        axes.plot([1, 2, 3], [1, 2, 3])

        self.panel.draw()


app = wx.App()
f = TestFrame()
f.Show(True)
app.MainLoop()