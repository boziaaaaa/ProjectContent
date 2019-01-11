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
        self.sftpConnect = None
        self.sftp = None
    # def close(self):
    #     pass
    def sftp_check(self,command):
        picturePath = []
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.Host,self.port,self.user,self.password)
        std_in,std_out,std_err = ssh_client.exec_command(command)
        for line in std_out:
            picturePath.append(line.strip("\n"))
        ssh_client.close()
        return picturePath
    def sftp_down_file_open(self):
        self.sftpConnect = paramiko.Transport((self.Host, self.port))
        self.sftpConnect.connect(username=self.user, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.sftpConnect)

    def sftp_down_file_close(self):
        self.sftpConnect.close()
    def sftp_down_file(self,server_path, local_path):
        try:
            # sftp = paramiko.SFTPClient.from_transport(self.sftpConnect)
            self.sftp.get(server_path,local_path)
        except Exception, e:
            print e

def getEachDay(startDate,endDate):
    eachDay = []
    datestart = datetime.datetime.strptime(startDate,'%Y%m%d')
    dateend = datetime.datetime.strptime(endDate,'%Y%m%d')
    eachDay.append(datestart.strftime('%Y%m%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)

        eachDay.append(datestart.strftime('%Y%m%d'))
    return eachDay

if __name__=="__main__":
    startDate = ""
    endDate = ""
    local_path = ""
    with open("LMI_L1B_Picture_configure.cfg") as f:
        lines = f.readlines()
        for line in lines:
            if "startDate" in line:
                startDate = line.split("=")[-1].strip()
            elif "endDate" in line:
                endDate = line.split("=")[-1].strip()
            elif "outputPath" in line:
                local_path = line.split("=")[-1].strip()
    print "startDate",startDate
    print "endDate",endDate
    print "local_path",local_path
    Host = "10.24.189.195"
    port = 83
    user = "CVSRUN"
    password = "CVSRUN"
    server_path = "/CVSDATA/FY4A/LMI/D1B/IMAGE/"

    if os.path.exists(local_path) == False:
        print "local path do not exist!->",local_path
        exit()
    SFTP = sftp(Host,port,user,password)
    Days = getEachDay(str(startDate),str(endDate))
    for YYYYMMDD in Days:
        command = "ls " + server_path + YYYYMMDD + "/*.jpg"
        picturePath = SFTP.sftp_check(command)
        local_path_new = local_path + YYYYMMDD + "/"
        print local_path_new
        if os.path.exists(local_path_new) == False:
            os.makedirs(local_path_new)
            print "create file : %s"%local_path_new
        SFTP.sftp_down_file_open()
        for server_name in picturePath:
            local_name = local_path_new + server_name.split("/")[-1]
            SFTP.sftp_down_file(server_name, local_name)
        SFTP.sftp_down_file_close()
        print "download %s jpg Success! number: %d "%(YYYYMMDD,len(picturePath))
