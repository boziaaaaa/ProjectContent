#coding=utf-8
import time
import datetime
import random
import zhenzismsclient as smsclient
import requests
from bs4 import BeautifulSoup


def get_content(url):
    outputString = []
    r = requests.get(url,headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0',})
    html = r.content
    soup =BeautifulSoup(html, "lxml")
    juzilist = soup.find_all('div',class_="entry-content")
    for x in juzilist:
        lines = x.get_text()
        lines = lines.split('\n')
        for l in  lines:
            if '、' in l:
                if '肥' in l or '胖' in l:
                    continue
                outputString.append(l)
    return outputString
def get_sentence():
    url = 'https://www.haoyulu.cn/juzi/jingdian/2618.html'
    outputString = get_content(url)
    line = outputString[31].split('、')
    line = line[1]
    return outputString
def sendText(message):
    client = smsclient.ZhenziSmsClient('http://sms_developer.zhenzikj.com', '102699','a31c39d9-28c6-4d23-bbb2-69dd2f5eb610' )
    result = client.send('15292189666', message)
    # result = client.send('18810939414', message)
    print(result)
    return 0

if __name__ == '__main__':
    status = 0
    try:
        sentenceS = get_sentence()

        # for i in range(len(sentenceS)):
        #     print(sentenceS[i])

        number = random.randint(0,len(sentenceS)-1)
        sentence = sentenceS[number].split('、')
        sentence = sentence[1]
    except:
        sentence = '塑造自己，过程很疼，但你最终你能收获一个更好的自己'
    message = sentence+'\n'+'    备注：我是bozi的分身，任务是在每天定时发送爱心提示短信！不接收信息，切勿回复！'

    time_now = datetime.datetime.now()
    time_now_str = str(time_now.year)+"年"+str(time_now.month)+'月'+str(time_now.day)+'日'+str(time_now.hour)+'时'+str(time_now.minute)+'分'+str(time_now.second)+'秒'
    message_send = message + '\n' + str(time_now_str)
    status = sendText(message_send)
    if status == 0:
        print('test send message success!! :\n',message_send)

