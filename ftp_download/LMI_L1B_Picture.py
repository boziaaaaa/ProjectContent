#coding=utf8
import time
import datetime
import ftp_downLoad_base
def getEachDay(startDate,endDate):
    eachDay = []
    datestart = datetime.datetime.strptime(startDate,'%Y%m%d')
    dateend = datetime.datetime.strptime(endDate,'%Y%m%d')
    eachDay.append(datestart.strftime('%Y%m%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        eachDay.append(datestart.strftime('%Y%m%d'))
    return eachDay

def ParseConfig(configFile):
    config = {"Host":None,"port":None,"user":None,"passward":None,"server_path":None, \
              "startDate":None,"endDate":None,"local_path":None}
    with open(configFile) as f:
        lines = f.readlines()
        for line in lines:
            if "Host" in line:
                config["Host"] = line.split("=")[-1].strip()
            elif "port" in line:
                config["port"] = int( line.split("=")[-1].strip() )
            elif "user" in line:
                config["user"] = line.split("=")[-1].strip()
            elif "password" in line:
                config["passward"] = line.split("=")[-1].strip()
            elif "server_path" in line:
                config["server_path"] = line.split("=")[-1].strip()
            if "startDate" in line:
                config["startDate"] = line.split("=")[-1].strip()
            elif "endDate" in line:
                config["endDate"] = line.split("=")[-1].strip()
            elif "local_path" in line:
                config["local_path"] = line.split("=")[-1].strip()
    return config
if __name__=="__main__":
    configFile = "LMI_L1B_Picture_configure.cfg"
    config = ParseConfig(configFile)
    Days = getEachDay(str(config["startDate"]),str(config["endDate"]))
    for YYYYMMDD in Days:
        print YYYYMMDD
        serverPath =  config["server_path"]+YYYYMMDD
        localPath = config["local_path"]
        sftp = ftp_downLoad_base.sftp(config["Host"], config["port"], config["user"], config["passward"])
        sftp.DownLoad(serverPath,localPath)

if __name__=="__main22__": #每天自动下载一次
    day_flag = ""
    while(1):
        date_now = (datetime.datetime.now()-datetime.timedelta(1)).strftime("%Y%m%d")
        print date_now,day_flag
        if day_flag != date_now:
            configFile = "./ftp_download/LMI_L1B_Picture_configure.cfg"
            config = ParseConfig(configFile)
            Days = getEachDay(str(config["startDate"]),str(config["endDate"]))
            YYYYMMDD = date_now
            serverPath =  config["server_path"]+YYYYMMDD
            localPath = config["local_path"]
            print serverPath
            print localPath
            day_flag = date_now
        time.sleep(60*60*6)