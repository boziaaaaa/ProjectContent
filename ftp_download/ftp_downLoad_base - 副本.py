import paramiko
import os

class ExSFTP():
    def __init__(self, host, acct, passwd, port=22):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print host
        print port
        print acct
        print passwd
        ssh.connect(hostname=host, port=port, username=acct, password=passwd)
        self.sftp = ssh.open_sftp()
        self.open = self.sftp.open
        self.get_transport=ssh.get_transport
        self.exec_command = ssh.exec_command

    def runcmd(self, command, cwd='', bufsize=-1, get_pty=False, environment=None, stdout=None, stderr=None):
        _tsp = self.get_transport()
        chan = _tsp.open_session(timeout=30)

        if environment:
            chan.update_environment(environment)
        if get_pty:
            chan.get_pty()
        if cwd:
            chan.exec_command("cd %s" % cwd)
        chan.exec_command(command)
        return chan

    def xlist(self, path):
        l = []
        with self.runcmd("ls " + path).makefile('r') as f:
            for i in f.readlines():
                i = i.strip()
                if i:
                    l.append(i)
        return l

    def xget(self, path, callback, rest, block_size=32768):
        with self.open(path, "r") as f:
            if rest: f.seek(rest)
            f.set_pipelined(True)
            buf = True
            while buf:
                buf = f.read(block_size)
                callback(buf)

class a(object):
    def __init__(self):
        self.host_final = ""
        self.user_final = ""
        self.password_final = ""
        self.port = ""
    def setHost(self,host):
        # print "---setHost----"
        self.host_final = host
        if "10.24.10.6" in host or "10.24.10.103" in host:
            self.user_final = "fy4"
            self.password_final = "fy4"
        elif "10.24.171.42" in host:
            self.user_final = "cosrun3d"
            self.password_final = "cosrun3d"
        elif "10.24.240.83" in host:
            self.host_final = "10.24.189.195"
            self.port = 83
            self.user_final = "CVSRUN"
            self.password_final = "CVSRUN"
        elif "10.24.34.219" in host:
            self.user_final = "developer"
            self.password_final = "deve123"

    def DownLoad(self,inputFile,outputPath):

        client=ExSFTP(self.host_final,acct=self.user_final,passwd=self.password_final,port=self.port)
        if len(outputPath) < 1:
            outputPath="D:/Data_ftp/"
        OutputName = outputPath+os.path.basename(inputFile)
        inputFile = inputFile.replace(r"\\","\/")
        OutputName = OutputName.replace(r"\\","\/")
        index = 1
        print inputFile
        for i in client.xlist(inputFile):
            print i
            with open(OutputName,'wb') as f:
                client.xget(i,f.write,0)
                index = 0
        if index == 1:
            return 1 #fail
        return 0

# if __name__ == '__main__':
#     import os
#     client=ExSFTP(host="10.24.10.6",acct="fy4",passwd="fy4")
#     for i in client.xlist("/FY4COMM/FY4A/COM/PRJ/test/Himawari8_OBI_20170406_0000_PRJ3.HDF"):
#         print i
#         with open("D:/temp_10.24.10.6/Himawari8_OBI_20170406_0000_PRJ3.HDF",'wb') as f:
#             client.xget(i,f.write,0)