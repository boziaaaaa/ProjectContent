#coding:utf-8
import socket
s = socket.socket()
host = socket.gethostbyname(socket.gethostname())
port = 11112
s.connect((host,port))
while True:
    cmd = raw_input('输入:')
    if cmd == 'quit':
        break
    elif cmd == '':
        continue
    s.sendall(cmd)
    data = s.recv(1024)
    print data
s.close()