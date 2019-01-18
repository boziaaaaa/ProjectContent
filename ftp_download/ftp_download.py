#-*-coding=utf-8-*-
from Tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ftp_downLoad_base import sftp
import time
import os

inputFile = ""
outputFile = ""
host_final = ""
port = 0
user_final = ""
password_final = ""


def Quit(a=0):
    print "Quit()"
    root.destroy()

def ftp_init(a=0):  # 处理事件，*args表示可变参数
    print "ftp_init()"
    global host_final
    global port
    global password_final
    global user_final
    chosen = interfaceChosen.get()  # 打印选中的值
    host_final = chosen
    port = 22
    if "10.24.10.6" in chosen or "10.24.10.103" in chosen:
        user_final = "fy4"
        password_final = "fy4"
    elif "10.24.171.42" in chosen:
        user_final = "cosrun3d"
        password_final = "cosrun3d"
    elif "10.24.240.83" in chosen:
        host_final = "10.24.189.195"
        port = 83
        user_final = "CVSRUN"
        password_final = "CVSRUN"
    elif "10.24.34.219" in chosen:
        user_final = "developer"
        password_final = "deve123"

def PrintIn(a=0):
    print "PrintIn()"
    global inputFile
    global outputFile
    if inputFile:
        pass
    else:
        inputFile = PrintIn_varI.get()
    if outputFile:
        pass
    else:
        outputFile = PrintIn_varO.get()
    outputFile = outputFile.strip()
    ftp_init()

def download(a=0):
    print "download()"
    global inputFile
    global outputFile
    global host_final
    global port
    global password_final
    global user_final
    Label(root, text="                         ").place(x=1, y=150)
    if os.path.exists(outputFile) == False:
        t = time.time()
        Label(root, text="本地路径错误！"+str((t))).place(x=100, y=150)
        return
    print "inputFile",inputFile
    inputFile = str(inputFile).split(";")
    if len(inputFile) > 0:# and len(outputFile) > 0:
        Label(root, text="下载中..." ).place(x=1, y=700)
        for inputFile_each in inputFile:
            downLoad_base = sftp(host_final,port,user_final,password_final)
            print "inputFile_each",inputFile_each
            print "outputFile",outputFile
            status = downLoad_base.DownLoad(inputFile_each,outputFile)
        Label(root, text="         ").place(x=1, y=150)
        t = time.time()
        if status == 0:
            Label(root, text="完成！"+str((t))).place(x=100,y=150)
        else:
            Label(root, text="失败 输入文件不存在！"+str((t))).place(x=100,y=150)
        root.update()
    else:
        Label(root, text="请输入！" ).place(x=1, y=150)
        root.update()
    inputFile = ""
    outputFile = ""
    host_final = ""
    port = 0
    user_final = ""
    password_final = ""

def browse(a=0):
    print "browse()"
    global outputFile
    outputFile = filedialog.askdirectory()
    Label(root,text = '                                                       ').place(x=100, y=150)
    Label(root,text = '本地目录:'+str(inputFile)).place(x=100, y=150)

if __name__=="__main__":
    root = Tk()
    root.title("download from sftp -version1.0(test)")
    root.iconbitmap("ftp_download.ico")
    root.minsize(800, 200)
    PrintIn_varI = StringVar()
    PrintIn_varO = StringVar()
    # ftp = ftp_tk()
    interfaceChosen = ttk.Combobox(root, width=13, textvariable="1")
    interfaceChosen['values'] = ("10.24.34.219",
                                 "10.24.240.83",
                                 "10.24.10.6",
                              "10.24.10.103",
                              "10.24.171.42"
                              )     # 设置下拉列表的值
    interfaceChosen.grid(column=1, row=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
    interfaceChosen.current(0)    # 设置下拉列表默认显示的值，0为 interfaceChosen['values'] 的下标值
    interfaceChosen.place(x=60,y=10)
    Label(root,text = 'ftp').place(x=10,y=10)
    Label(root,text = '下载文件').place(x=5,y=55)
    Label(root,text = '本地目录').place(x=5,y=75)

    Entry(root,width=100,textvariable=PrintIn_varI).place(x=60,y=55)
    Entry(root,width=100,textvariable=PrintIn_varO).place(x=60,y=75)

    confirm_brose = Button(root,text="浏览",command=browse)
    confirm_brose.place(x=30,y=120)
    # confirm = Button(root,text="确认",command=PrintIn)
    # confirm.place(x=80,y=120)
    # confirm.bind("<ButtonPress>", download)
    confirm = Button(root,text="确认",command=download)
    confirm.place(x=80,y=120)
    confirm.bind("<ButtonPress>", PrintIn)
    confirm2 = Button(root,text="关闭",command="")
    confirm2.place(x=170,y=120)
    confirm2.bind("<ButtonPress-1>", Quit)
    root.mainloop()
