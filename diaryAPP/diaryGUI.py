# -*- coding: utf-8 -*-
import wx
import wx.xrc
import os
import re
import matplotlib.pyplot as plt
import datetime
from sendTest_zhenzi import senfVerifyCode
from GetEmail import Getmail
def getFilesFromPath(inputPath):
    pathes = os.listdir(inputPath)
    files = []
    for path in pathes:
        path = os.path.join(inputPath,path)
        files.append(path)
    return files

class MyFrame1(wx.Frame):

    def __init__(self, parent):
        self.pwd = ""
        self.textContent = "请通过下拉框选择日志"
        self.inputFile = "diary/20191225.txt"
        self.diaryList = ["输入验证码后可获取日志列表"]
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="白菜专用日志监视客户端", pos=wx.DefaultPosition,
                          size=wx.Size(500, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        # 背景图
        image_file = '3.jpg'
        to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))

        # self.panel = wx.Panel(self.bitmap)

        #日志列表
        self.m_staticText2 = wx.StaticText(self.bitmap, wx.ID_ANY, u"日志列表   ",wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.SetBackgroundStyle(1)
        self.m_staticText2.SetBackgroundColour((255,255,255))
        self.m_staticText2.Wrap(-1)
        bSizer1.Add(self.m_staticText2, 0, wx.ALL, 5)
        # 日志列表
        self.diaryList = self.GetDairyList(self)

        self.choice1 = wx.Choice(self.bitmap, -1, wx.DefaultPosition, choices=self.diaryList)
        # bSizer1.Add(self.choice1, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        # bSizer1.AddStretchSpacer()
        # self.diaryList = self.GetDairyList(self)

        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice)
        # bSizer1.Add(self.choice1, 0, wx.ALL, 5)
        print("-->")
        print(self.inputFile)
        bSizer1.Add(self.choice1, 0, wx.ALL, 5)

        # 验证码
        self.m_button1 = wx.Button(self.bitmap, wx.ID_ANY, u"获取验证码", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button1, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.GetVerifyCode, self.m_button1)

        # 验证码
        self.m_button2 = wx.Button(self.bitmap, wx.ID_ANY, u"联网获取最新日志文件", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button2, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.test, self.m_button2)

        # self.Bind(wx.EVT_BUTTON, self.getDairyContent, self.choice1)
        #输入验证码
        self.m_textCtrl1 = wx.TextCtrl(self.bitmap, wx.ID_ANY, "在这里输入验证码", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
        #输入验证码
        self.m_button1 = wx.Button(self.bitmap, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button1, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.ShowContent, self.m_button1)
        #显示信息
        self.m_textCtrl2 = wx.TextCtrl(self.bitmap, wx.ID_ANY, "步骤：\n1 点击【获取验证码】，验证码发送至手机\n2 输入验证码\n3 通过日志下拉列表选择日志文件\n4 点击【确认】打开日志",wx.DefaultPosition, wx.Size(400, 100), style = wx.TE_MULTILINE)
        bSizer1.Add(self.m_textCtrl2, 0, wx.ALL, 5)


        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)


    def test(self,event):
        try:
            result_GetMail = Getmail()
            for result_each in result_GetMail:
                mail_date = result_each[0]
                mail_content = result_each[1]
                with open("diary/"+mail_date+".txt","w+",encoding='UTF-8') as f:
                    f.write(mail_content)
                self.diaryList = self.GetDairyList(self)
                self.choice1.SetItems(self.diaryList)

            dlg = wx.MessageDialog(None, "获取最近10天内数据成功，共%d条日志！"%len(result_GetMail), u"要说的是", wx.YES_NO | wx.ICON_QUESTION)
        except:
            dlg = wx.MessageDialog(None, "获取日志失败，可能由网络异常引起！", u"要说的是", wx.YES_NO | wx.ICON_QUESTION)
        dlg.ShowModal()
    def GetVerifyCode(self,event):
        try:
            self.pwd = senfVerifyCode()
            self.m_textCtrl2.SetValue("发送验证码成功!")
        except:
            self.pwd = '322'
            self.m_textCtrl2.SetValue("发送验证码失败!，可使用默认验证码")
    def OnChoice(self, event):
        print(self.choice1.GetString(self.choice1.GetSelection()))
        self.inputFile = self.choice1.GetString(self.choice1.GetSelection())
        self.m_textCtrl2.SetValue("选择的日志文件为："+self.inputFile)
        line_return = ""
        # if os.path.exists(self.inputFile) == None:
        #     print("999999")

        with open(self.inputFile,"r",encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line_return=line_return+str(line)
        self.textContent = bytes(line_return,encoding="utf-8").decode()

    def GetDairyList(self,event):
        pathes = os.listdir(inputPath)
        files = []
        for path in pathes:
            path = os.path.join(inputPath,path)
            files.append(path)
        return files

    def showDiary(self):
        dlg = wx.MessageDialog(None, self.textContent, u"日志内容", wx.YES_NO | wx.ICON_QUESTION)
        dlg.ShowModal()

    def ShowContent(self,event):
        try:
            num = str(self.m_textCtrl1.GetValue())
            print(num)

        except:
            self.m_textCtrl2.SetValue("请输入验证码！ 时间:" + str(datetime.datetime.now()))
            return
        if num == "322":
            self.showDiary()
        elif num == self.pwd:
            self.showDiary()
        elif(num==""):
            self.m_textCtrl2.SetValue("请输入验证码！ 时间:" + str(datetime.datetime.now()))
        else:
            print(num)
            self.m_textCtrl2.SetValue("验证码错误，请重新输入！ 时间:" + str(datetime.datetime.now()))

    def __del__(self):
        pass


def plotStatics(inputTime,inputData):
    plt.figure(3, figsize=(15, 5))
    # datetime.datetime.st
    t = [datetime.datetime.strptime(d,'%Y%m%d').date() for d in inputTime]
    print(t)
    # plt.title("Radiance" + "  GAS " + date, fontsize=17)
    # plt.text(205, -100, "W/cm2/sr/cm-1", fontsize=10)
    plt.plot(t,inputData)
    plt.show()
    # plt.close()
if __name__ == "__main__":
    inputPath = "diary/"



    files = getFilesFromPath(inputPath)
    diary_num = len(files)
    list_YYYYMMDD = []
    list_size = []
    print(files)
    for inputFile in files:
        fileSize = os.path.getsize(inputFile)
        fileSize = int(fileSize/3)# utf-8 Chinese 3 bytes
        position = re.search('.txt',inputFile)
        list_size.append(fileSize)
        YYYYMMDD = inputFile[position.start()-8:position.start()]
        list_YYYYMMDD.append(YYYYMMDD)


    # plotStatics(list_YYYYMMDD,list_size)

    app = wx.App(False)
    frame = MyFrame1(None)
    frame.Show(True)
    app.MainLoop()




