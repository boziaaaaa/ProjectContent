#coding=utf8
from Tkinter import *
import time
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#图灵网站账号是手机或boziaaaaa邮箱，key is tuling123
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyttsx
def tuling_speak(inputString):
    engine = pyttsx.init()
    engine.say(inputString)
    engine.runAndWait()

def tuling(inputString):
    while True:
        cmd = inputString
        if cmd == 'quit':
            break
        elif cmd == '':
            return '你什么也没有输入'
        key = '186cccedc79549ecac4dcc8a56fc9fb4' #别人的
        # key = 'e21c928c2a9e414e9c8eff6615d0ad51'
        api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info=' + cmd
        print api
        response = urllib.urlopen(api).read()
        dic_json = json.loads(response)
        # return '图灵机器人:'.decode('utf-8') + dic_json['text']
        return dic_json['text']

# 发送按钮事件
def sendmessage():
    # 在聊天内容上方加一行 显示发送人及发送时间
    msgcontent = unicode('我输入的  :', 'utf8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
    text_me = text_msg.get('0.0', END)
    text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, text_me)

    text_me = text_me.strip()
    text_me = text_me.encode('utf8')
    text_tuling = tuling(text_me)
    msgcontent = unicode('图灵机器人:', 'utf8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
    text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, text_tuling+"\n")
    text_msg.delete(0.0,END)
    text_msglist.see(END)
    text_msglist.update()
    tuling_speak(text_tuling)

if __name__=="__main__":
    root = Tk()
    root.title(unicode('与图灵机器人聊天中', 'utf8'))
    # 创建几个frame作为容器
    frame_left_top = Frame(width=564, height=316, bg='green')
    frame_left_center = Frame(width=500, height=100, bg='red')
    frame_left_bottom = Frame(width=50, height=30)
    ##创建需要的几个元素
    text_msglist = Text(frame_left_top)
    text_msg = Text(frame_left_center);
    button_sendmsg = Button(frame_left_bottom, text=unicode('发送', 'utf8'), command=sendmessage)
    # 创建一个绿色的tag
    text_msglist.tag_config('green', foreground='#008B00')
    # 使用grid设置各个容器位置
    frame_left_top.grid(row=0, column=0, padx=2, pady=5)
    frame_left_center.grid(row=1, column=0, padx=2, pady=5)
    frame_left_bottom.grid(row=2, column=0)
    frame_left_top.grid_propagate(0)
    frame_left_center.grid_propagate(0)
    frame_left_bottom.grid_propagate(0)
    # 把元素填充进frame
    text_msglist.grid()

    text_msg.grid()
    button_sendmsg.grid(sticky=E)
    text_msglist.see(END)
    # 主事件循环
    root.mainloop()


