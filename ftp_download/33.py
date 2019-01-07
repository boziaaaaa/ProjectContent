#coding:utf-8
"""
  ssh操作例子 实现了服务器日志下载
  2012-08-24
  yywolf
"""
import paramiko
import time
hostname="????"
port=22
username="app"
password="????"
if __name__=="__main__":
#  paramiko.util.log.log_to_file('paramiko.log')
  s = paramiko.SSHClient()
  s.load_system_host_keys()
  s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
  s.connect(hostname,port,username,password,timeout=4)
  stdin,stdout,stderr = s.exec_command("sh ~/log/check")
  print stdout.read()
  s.close()
  #sftp
  t = paramiko.Transport((hostname,port))
  t.connect(username=username,password=password)
  sftp = paramiko.SFTPClient.from_transport(t)
  files = sftp.listdir("/home/app/log/")
  for f in files:
    print f
  filetime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
  #需要下载的文件 和下载后的文件名
  sftp.get("/home/app/log/server.txt","C:\\Users\\Administrator\\Desktop\\server.txt")   
  sftp.get("/home/app/log/"+filetime+".log.zip","C:\Users\Administrator\Desktop\\"+filetime+".log.zip")
  #RASkey
  pkey_file = "E:\\yy\\tools\\key\\rsa.txt"
  key = paramiko.RSAKey.from_private_key_file(pkey_file)
  s = paramiko.SSHClient()
  s.load_system_host_keys()
  s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
  s.connect(hostname,port,username,pkey=key)
  stdin, stdout, stderr = s.exec_command("ls -l /home/app/log")
  print stdout.read()
  s.close()
  raw_input()
