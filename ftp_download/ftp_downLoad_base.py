#coding=utf8
import paramiko
import os
import datetime
import sys
class sftp(object):
    def __init__(self,Host,port,user,password):
        self.Host = Host
        self.port = port
        self.user = user
        self.password = password
        self.sftpConnect = paramiko.Transport((self.Host, self.port))
        self.sftpConnect.connect(username=self.user, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.sftpConnect)
    # def sftp_do_command(self,command):
    #     result = []
    #     ssh_client = paramiko.SSHClient()
    #     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     ssh_client.connect(self.Host,self.port,self.user,self.password)
    #     std_in,std_out,std_err = ssh_client.exec_command(command)
    #     for line in std_out:
    #         result.append(line)
    #     ssh_client.close()
    #     return result
    def __sftp_getFileList(self,command):
        picturePath = []
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.Host,self.port,self.user,self.password)
        std_in,std_out,std_err = ssh_client.exec_command(command)
        for line in std_out:
            picturePath.append(line.strip("\n"))
        ssh_client.close()
        return picturePath
    def __sftp_download_file(self,server_path, local_path):
        try:
            self.sftp.get(server_path,local_path)
        except Exception, e:
            print e
    def __sftp_close(self):
        self.sftpConnect.close()

    def DownLoad(self,server_path,local_path):
        print "server_path",server_path
        print "local_path",local_path
        flag = 0
        command = "ls " + server_path
        print command
        picturePath = self.__sftp_getFileList(command)
        print picturePath
        if len(picturePath) < 1:
            self.__sftp_close()
            return 1
        for file in picturePath:
            remote_path = os.path.dirname(file)
            basename = os.path.basename(file)
            if remote_path:
                pass
            else:
                remote_path = server_path
            file_romote = remote_path + '/' + basename
            YYYYMMDD = remote_path[-8:]
            print "YYYYMMDD",YYYYMMDD
            try:
                if int(YYYYMMDD) > 20000000 and int(YYYYMMDD) < 40000000 and flag == 0:
                    local_path = local_path + "\\" + YYYYMMDD #if date in path ,make subfile
                    flag = 1
            except:
                pass
            if os.path.exists(local_path) == False:
                os.mkdir(local_path)
            file_local = os.path.join(local_path, basename)
            print file_romote
            try:
                self.__sftp_download_file(file_romote, file_local)
            except Exception,e:
                print e
                continue
        self.__sftp_close()
        return 0
if __name__=="__main__":
        Host = "10.24.189.195"
        port = 83
        user = "CVSRUN"
        password = "CVSRUN"
        server_path = "/CVSDATA/FY4A/LMI/D1B/IMAGE/*/*L1B_EVT-_SING_NUL_20190109235510_20190109235959_7800M_3.jpg"
        local_path = "D:/Data_ftp/"
        local_path = "C:/Users/bozi/Desktop/test"


        Host = "10.24.34.219"
        port = 22
        user = "developer"
        password = "deve123"
        server_path = "/dpps01/COMDATA/AOD/AEROD/MYD/2018/MYD08_D3.A2018357.061.2018358202652.h5"
        local_path = "D:/Data_ftp/"
        local_path = "C:/Users/bozi/Desktop/test"


        SFTP = sftp(Host,port,user,password)
        SFTP.DownLoad(server_path,local_path)



