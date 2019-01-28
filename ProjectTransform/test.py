#coding = utf-8
import os

import datetime

def getEveryDay(startT,endT):
    result = []
    startTime = datetime.datetime.strptime(startT,"%Y%m%d")
    endTime = datetime.datetime.strptime(endT,"%Y%m%d")
    while startTime <= endTime:
        temp = datetime.datetime.strftime(startTime,"%Y%m%d")
        result.append(temp)

        startTime = startTime + datetime.timedelta(1)

    return result
if __name__ == "__main__":

    startT = "20180601"
    endT =   "20180629"
    result = getEveryDay(startT,endT)
    print result

    for d in result:
        cmd = "cp -r /mnt/FY3D/SSTDATA/FY3C/VIRR/L1/"+d +" /SSTDATA/SSTDATA/FY3C/VIRR/L1/"
        print cmd
        status = os.system(cmd)
        print "status == ",status

