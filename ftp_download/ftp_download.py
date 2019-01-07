#-*-coding=utf-8-*-
from Tkinter import *
from tkinter import ttk
from DownLoad import a
import time
import subprocess
import shlex

DDD = a()
inputFile = ""
outputFile = ""
reInput = 1

root=Tk()
root.minsize(300,200)

varI = StringVar()
varO = StringVar()



def quit1(a):
    quit = 1
    if quit == True:
        root.destroy()


def go(*args):  # 处理事件，*args表示可变参数
    chosen = numberChosen.get()  # 打印选中的值
    DDD.setHost(chosen)

def PrintIn():
    global inputFile
    inputFile = varI.get()
    global outputFile
    outputFile = varO.get()
    go()


def download(a):
    Label(root, text="                         ").place(x=1, y=150)

    PrintIn()
    global inputFile
    global outputFile
    # print "iiiii",inputFile
    # print "OOOOO",outputFile
    import os
    if os.path.exists(outputFile) == False:
        t = time.time()

        Label(root, text="本地路径错误！"+str((t))).place(x=100, y=150)

        return
    if len(inputFile) > 0:# and len(outputFile) > 0:
        #root.update()
        # print ".///////"
        Label(root, text="下载中..." ).place(x=1, y=150)
        status = DDD.DownLoad(inputFile,outputFile)
        # print "status",status
        Label(root, text="         ").place(x=1, y=150)
        if status == 0:
            t = time.time()
            Label(root, text="完成！"+str((t))).place(x=100,y=150)
        else:
            Label(root, text="失败！"+str((t))).place(x=100,y=150)

        root.update()
    else:
        Label(root, text="请输入！" ).place(x=1, y=150)
        root.update()

number = StringVar()
numberChosen = ttk.Combobox(root, width=13, textvariable="1")
numberChosen['values'] = ("10.24.10.6","10.24.10.103","10.24.171.42")     # 设置下拉列表的值
numberChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
numberChosen.current(0)    # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
# numberChosen.bind("<<ComboboxSelected>>", go)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
# go()
numberChosen.place(x=60,y=10)
Label(root,text = 'ftp').place(x=10,y=10)
Label(root,text = '下载文件').place(x=5,y=55)
Label(root,text = '本地目录').place(x=5,y=75)
# Label(root, text="下载耗时：" + "s").place(x=1, y=150)

Entry(root,width=30,textvariable=varI).place(x=60,y=55)
Entry(root,width=30,textvariable=varO).place(x=60,y=75)
confirm = Button(root,text="确认",command=PrintIn)
confirm.place(x=80,y=120)



inputFile = varI.get()
outputFile = varO.get()

# print "111111111111111",inputFile
confirm.bind("<ButtonPress>", download)
# print "222222222222222"
confirm2 = Button(root,text="关闭",command="")
confirm2.place(x=170,y=120)
confirm2.bind("<ButtonPress-1>", quit1)
root.mainloop()