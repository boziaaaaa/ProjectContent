#-*-coding=utf-8-*-
from Tkinter import *
from tkinter import ttk
from ftp_downLoad_base import a
import time
import subprocess
import shlex

downLoad_base = a()
inputFile = ""
outputFile = ""
# reInput = 1
root=Tk()
root.minsize(300,200)
PrintIn_varI = StringVar()
PrintIn_varO = StringVar()

def Quit(a):
    root.destroy()

def ftp_init(*args):  # 处理事件，*args表示可变参数
    chosen = interfaceChosen.get()  # 打印选中的值
    downLoad_base.setHost(chosen)

def PrintIn():
    global inputFile
    inputFile = PrintIn_varI.get()
    global outputFile
    outputFile = PrintIn_varO.get()
    ftp_init()

def download(a):
    Label(root, text="                         ").place(x=1, y=150)
    PrintIn()
    global inputFile
    global outputFile
    import os
    if os.path.exists(outputFile) == False:
        t = time.time()
        Label(root, text="本地路径错误！"+str((t))).place(x=100, y=150)
        return
    if len(inputFile) > 0:# and len(outputFile) > 0:
        Label(root, text="下载中..." ).place(x=1, y=150)
        status = downLoad_base.DownLoad(inputFile,outputFile)
        Label(root, text="         ").place(x=1, y=150)
        t = time.time()
        if status == 0:
            Label(root, text="完成！"+str((t))).place(x=100,y=150)
        else:
            Label(root, text="失败！"+str((t))).place(x=100,y=150)
        root.update()
    else:
        Label(root, text="请输入！" ).place(x=1, y=150)
        root.update()

if __name__=="__main__":
    interfaceChosen = ttk.Combobox(root, width=13, textvariable="1")
    interfaceChosen['values'] = ("10.24.240.83",
                                 "10.24.10.6",
                              "10.24.10.103",
                              "10.24.171.42",

                              "10.24.34.219")     # 设置下拉列表的值
    interfaceChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
    interfaceChosen.current(0)    # 设置下拉列表默认显示的值，0为 interfaceChosen['values'] 的下标值
    interfaceChosen.place(x=60,y=10)
    Label(root,text = 'ftp').place(x=10,y=10)
    Label(root,text = '下载文件').place(x=5,y=55)
    Label(root,text = '本地目录').place(x=5,y=75)
    # Label(root, text="下载耗时：" + "s").place(x=1, y=150)

    Entry(root,width=30,textvariable=PrintIn_varI).place(x=60,y=55)
    Entry(root,width=30,textvariable=PrintIn_varO).place(x=60,y=75)
    confirm = Button(root,text="确认",command=PrintIn)
    confirm.place(x=80,y=120)
    # inputFile = varI.get()
    # outputFile = varO.get()
    confirm.bind("<ButtonPress>", download)

    confirm2 = Button(root,text="关闭",command="")
    confirm2.place(x=170,y=120)
    confirm2.bind("<ButtonPress-1>", Quit)
    root.mainloop()