#coding=utf-8
import cv2
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
from PIL import ImageGrab
import os

def Captrue():
    cap = cv2.VideoCapture(0)  # 0 means Camera
    ret, frame = cap.read()  # get a frame
    image = np.array(frame)
    cv2.imwrite("test.png", image)
    cap.release()
    cv2.destroyAllWindows()
def GetScreen():
    I = ImageGrab.grab()
    I.save("test.png")
def Similarity(picture1,picture2):
    data = cv2.imread(picture1)
    hist1 = cv2.calcHist(data, [0], None, [256], [0, 255.0])
    data = cv2.imread(picture2)
    hist2 = cv2.calcHist(data, [0], None, [256], [0, 255.0])
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    try:
        return degree[0]
    except:
        return degree
def Email():
    mail_host = "smtp.163.com"
    mail_user = "boziabozi"
    # mail_pass = raw_input("password:")
    mail_pass = 0
    with open("./key.txt") as f:
        mail_pass = f.readline()
    receiver = "boziabozi@163.com"
    sender = "bozi" + "<" + mail_user + "@163.com" + ">" # 注意发件人格式
    message = MIMEMultipart("mult")

    content = u"检测本机电脑屏幕/摄像头，附件是屏幕截图"
    msg = MIMEText(content,_charset='utf-8')
    msg['Subject'] = u'邮件测试'
    msg['From'] = sender
    msg['To'] = receiver
    #添加照片附件
    with open('test.png',"rb")as fp:
         picture = MIMEImage(fp.read())
    # os.system("rm -rf test.png")
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
        print('send email success')
    except Exception:
        print("send email fail ！")

if __name__ == "__main__":
    pic_old = "test_original.png"
    pic_new = "test.png"
    while(1):
        GetScreen()
        # Captrue()
        if os.path.exists(pic_old) == False:
            GetScreen()
            # Captrue()
            os.system("cp "+pic_new+" "+pic_old)
        degree = Similarity(pic_old,pic_new)
        print time.time()
        print "-->",degree

        if degree < 0.9:
            print "picture changed"
            # Email()
            os.system("mv "+pic_new+" "+pic_old)
        time.sleep(2) #60s

