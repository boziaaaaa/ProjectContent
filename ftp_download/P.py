#-*-coding=utf-8-*-
from Tkinter import *
import os
import getpass

root = Tk()
root.minsize(300,50)
label = Label(root,text="label",width=30,height=2)
listbx = Listbox(root,width=80,height=5)
listbx.pack()
def Print():
    listbx.insert(0, "99999")
    #label.pack()
def inputFTP():
    command = "scp fy4@10.24.10.6:/FY4COMM/FY4A/COM/PRJ/test/Himawari8_OBI_20170406_0000_PRJ3.HDF D:/temp_10.24.10.6/"
    txt = "Downloading File,Please Wait!!"
    listbx.insert(0, txt)
    os.system(command)
    #listbx.insert(0, command)
    FileName = "/FY4COMM/FY4A/COM/PRJ/test/Himawari8_OBI_20170406_0000_PRJ3.HDF"
    txt = "Get "+FileName+" Sucess!!"
    listbx.insert(0, txt)

b2 = Button(root, text="button2", command=inputFTP)
b2.pack()
#b1 = Button(root,text="button1",command=Print)
#b1.pack()
def quit():
    quit = 1
    if quit == True:
        root.destroy()
b_quit = Button(root,text="Q",command=root.quit())
b_quit.pack()







root.mainloop()
