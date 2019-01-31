#coding=utf8
from Tkinter import *
import time
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def tuling(inputString):
    while True:
        cmd = inputString
        if cmd == 'quit':
            break
        elif cmd == '':
            continue
        key = 'e21c928c2a9e414e9c8eff6615d0ad51'
        api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info=' + cmd
        print api
        response = urllib.urlopen(api).read()
        dic_json = json.loads(response)
        return '图灵机器人:'.decode('utf-8') + dic_json['text']

root = Tk()
root.title(unicode('与图灵机器人聊天中', 'utf8'))
# 发送按钮事件
def sendmessage():
    # 在聊天内容上方加一行 显示发送人及发送时间
    msgcontent = unicode('我输入的  :', 'utf8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
    text_me = text_msg.get('0.0', END)
    text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, text_me)
    text_msg.delete('0.0', END)

    text_me = text_me.strip()
    text_me = text_me.encode('utf8')
    text_tuling = tuling(text_me)
    msgcontent = unicode('图灵机器人:', 'utf8') + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '
    text_msglist.insert(END, msgcontent, 'green')
    text_msglist.insert(END, text_tuling+"\n")
    text_msg.delete('0.0', END)

# 创建几个frame作为容器
frame_left_top = Frame(width=380, height=270, bg='white')
frame_left_center = Frame(width=380, height=100, bg='white')
frame_left_bottom = Frame(width=100, height=30)
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
# 主事件循环
root.mainloop()


