 # -*- coding:utf-8 -*-
import socket
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def get_computer(info):
    key = '186cccedc79549ecac4dcc8a56fc9fb4'
    api = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+info
          # "http://www.tuling123.com/member/robot/1562625/center/frame.jhtml?page=0&child=0"
    response =urllib.urlopen(api).read()
    dic_json = json.loads(response)
    return '图灵机器人:'.decode('utf-8')+dic_json['text']
host = socket.gethostbyname(socket.gethostname())
print host
port =11112
s = socket.socket()
s.bind((host,port))
s.listen(1)
while True:
    clnt,addr = s.accept()
    print 'client address:',addr
    while True:
        data = clnt.recv(1024)
        if not data:sys.exit()
        print 'going to :',data
        result = get_computer(data)
        if len(result) == 0:
            result = "EXD"
        clnt.sendall(result)
clnt.close()