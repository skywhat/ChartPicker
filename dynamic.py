import wx

DATA = [("0", "Zero"), ("1", "One"), ("2", "Two")]
class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self)

        self.list = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
        self.list.InsertColumn(0, "Index")
        self.list.InsertColumn(1, "Number")
        for data in DATA:
            self.list.Append((data[0], data[1]))

        self.button = wx.Button(self.panel, label="Delete")
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.list, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.button, 0, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizerAndFit(self.sizer)

        self.Show()

    def OnButton(self, e):
        current_items = self.list.GetItemCount() - 1

        '''
        while ((current_items) >= 0) :
            if (self.list.GetItemText(current_items) == "1" or self.list.GetItemText(current_items) == "2"):
                self.list.DeleteItem(current_items)
                wx.MessageBox("Delete item ", 'Delete Information',wx.OK)
            else:
                break
            current_items-=1
        '''
        self.list.DeleteItem(current_items)

if __name__ == "__main__":
    app = wx.App(False)
    win = MainWindow(None)
    win.Centre()
    app.MainLoop()