#coding:utf-8
import urllib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def get_computer(info):
    key = 'e21c928c2a9e414e9c8eff6615d0ad51'
    api = 'http://www.tuling123.com/openapi/api?key='+key+'&info='+info
    response =urllib.urlopen(api).read()
    dic_json = json.loads(response)
    return '图灵机器人:'.decode('utf-8')+dic_json['text']
while True:
    cmd = raw_input('输入:')
    if cmd == 'quit':
        break
    elif cmd == '':
        continue
    data = get_computer(cmd)
    print data



