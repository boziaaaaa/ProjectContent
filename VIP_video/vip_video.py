#!/usr/bin/env python
# -*- coding: utf-8 -*-
# url解析 vip视频播放地址的模块 做url加密的
from urllib import parse
# 控制浏览器的
import webbrowser
import wx
import wx.xrc
import re
import os
class MyFrame1(wx.Frame):

    def __init__(self, parent):
        self.url = ""

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="这个软件可以看vip视频，不用掏钱-作者yb", pos=wx.DefaultPosition,
                          size=wx.Size(500, 150), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        # 背景图

        image_file = 'backGround.jpeg'
        if os.path.exists(image_file) == True:
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))
            #输入验证码
            self.m_textCtrl1 = wx.TextCtrl(self.bitmap, wx.ID_ANY, "", wx.DefaultPosition, (480,25), 0)
            bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)
            #输入验证码
            self.m_button1 = wx.Button(self.bitmap, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0)
            self.m_button1.SetPosition((100,100))
            bSizer1.Add(self.m_button1, 0, wx.ALL, 5)
            self.Bind(wx.EVT_BUTTON, self.playVideo, self.m_button1)

            self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"把视频网址复制粘贴到框里，点确认就可以看了", wx.DefaultPosition, wx.DefaultSize,0)
            self.m_staticText1.SetBackgroundColour((255,255,255))
            bSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)
        else:
            self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, "", wx.DefaultPosition, (480,25), 0)
            bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)

            self.m_button1 = wx.Button(self, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0)
            self.m_button1.SetPosition((3,3))
            bSizer1.Add(self.m_button1, 0, wx.ALL, 5)
            self.Bind(wx.EVT_BUTTON, self.playVideo, self.m_button1)

            self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"和我一起的backGround.jpeg文件是我的背景，换图片可以换背景，没有图片就没有背景", wx.DefaultPosition, wx.DefaultSize,0)
            bSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

    def playVideo(self,event):
        self.url = self.m_textCtrl1.GetValue()
        # 视频解析网站地址
        port = 'http://www.wmxz.wang/video.php?url='
        # 正则表达式判定是否为合法连接
        if re.match(r'^https?:/{2}\w.+$', self.url):
            # 拿到用户输入的视频网址
            ip = self.url
            # 视频连接加密
            ip = parse.quote_plus(ip)
            # 用浏览器打开网址
            webbrowser.open(port + ip)
        else:
            dlg = wx.MessageDialog(None, "网址无效，看看输对了没有！", u"要说的是", wx.YES_NO | wx.ICON_QUESTION)
            dlg.ShowModal()
    def __del__(self):
        pass

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame1(None)
    frame.Show(True)
    app.MainLoop()







#
# class APP:
#     # 魔术方法
#     # 初始化用的
#     def __init__(self, width=500, height=300):
#         self.w = width
#         self.h = height
#         self.title = 'vip视频破解助手'
#         # 软件名
#         self.root = tk.Tk(className=self.title)
#         # vip视频播放地址 StringVar() 定义字符串变量
#         self.url = tk.StringVar()
#         # 定义选择哪个播放源
#         self.v = tk.IntVar()
#         # 默认为1
#         self.v.set(1)
#         # Frame空间
#         frame_1 = tk.Frame(self.root)
#         frame_2 = tk.Frame(self.root)
#
#         # 控件内容设置
#         group = tk.Label(frame_1, text='暂时只有一个视频播放通道：', padx=10, pady=10)
#         tb = tk.Radiobutton(frame_1, text='唯一通道', variable=self.v, value=1, width=10, height=3)
#         lable = tk.Label(frame_2, text='请输入视频连接：')
#
#         # 输入框声明
#         entry = tk.Entry(frame_2, textvariable=self.url, highlightcolor='Fuchsia', highlightthickness=1, width=35)
#         play = tk.Button(frame_2, text='播放', font=('楷体', 12), fg='Purple', width=2, height=1, command=self.video_play)
#
#         # 控件布局 显示控件在你的软件上
#         frame_1.pack()
#         frame_2.pack()
#
#         # 确定控件的位置 wow 行 column 列
#         group.grid(row=0, column=0)
#         tb.grid(row=0, column=1)
#         lable.grid(row=0, column=0)
#         entry.grid(row=0, column=1)
#
#         # ipadx x方向的外部填充 ipady y方向的内部填充
#         play.grid(row=0, column=3, ipadx=10, ipady=10)
#
#     def video_play(self):
#             # 视频解析网站地址
#             port = 'http://www.wmxz.wang/video.php?url='
#             # 正则表达式判定是否为合法连接
#             if re.match(r'^https?:/{2}\w.+$', self.url.get()):
#                 # 拿到用户输入的视频网址
#                 ip = self.url.get()
#                 # 视频连接加密
#                 ip = parse.quote_plus(ip)
#                 # 用浏览器打开网址
#                 webbrowser.open(port + ip)
#             else:
#                 msgbox.showerror(title='错误', message='视频链接地址无效，请重新输入！')
#
#     # 启动GUI程序的函数
#     def loop(self):
#             self.root.resizable(True, True)
#             self.root.mainloop()
#
# if __name__ == "__main__":
#     app = APP()
#     app.loop()