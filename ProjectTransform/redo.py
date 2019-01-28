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
    startT = "20180501"
    endT =   "20180601"
    result = getEveryDay(startT,endT)
    for d in result:
        print d
        # cmd = "python ./OCC_POAD.py "+d+" D"

        # cmd = "python /GDS/SSTWORK/Picture_SST_Mean/Picture_SSTMean.py "+d+" AD D"
        # cmd = "python /GDS/SSTWORK/Picture_SST_Mean/Picture_SSTMean.py "+d+" AD N"
        cmd = "python ./FY3C_VIRRX_mosic.py "+d+" D"
        os.system(cmd)
        cmd = "python ./FY3C_VIRRX_mosic.py "+d+" N"
        os.system(cmd)