#coding=utf-8
from netCDF4 import Dataset
import h5py
import os
import numpy
import datetime
def read_L1B_HDF(HDFfile):
    X = []
    Y = []
    fileHandle = h5py.File(HDFfile)
    VData = fileHandle["VData"]
    # VData_len = len(VData)
    VData_keys = VData.keys()
    for i in VData_keys:
        X_temp = VData[i]["X_pixel"][:]
        X.extend(X_temp)
        Y_temp = VData[i]["Y_pixel"][:]
        Y.extend(Y_temp)
    fileHandle.close()
    X = numpy.array(X)
    Y = numpy.array(Y)

    length = X.shape[0]
    num1, num2, num3, num4, num5, num6, num7, num8 = 0,0,0,0,0,0,0,0
    # 0---------------------------------600
    #    5        6       7       8
    # ----------------------------------
    #    1        2       3       4
    # 400-------------------------------
    for i in range(length):
        print Y[i]
        if Y[i] >= 0 and Y[i] < 150 and X[i] >= 0 and X[i] <200:
            num5 = num5 + 1
        elif Y[i] >= 150 and Y[i] < 300 and X[i] >= 0 and X[i] < 200:
            num6 = num6 + 1
        elif Y[i] >= 300 and Y[i] < 450 and X[i] >= 0 and X[i] < 200:
            num7 = num7 + 1
        elif Y[i] >= 450 and Y[i] < 600 and X[i] >= 0 and X[i] < 200:
            num8 = num8 + 1
        elif Y[i] >= 0 and Y[i] < 150 and X[i] >= 200 and X[i] < 400:
            num1 = num1 + 1
        elif Y[i] >= 150 and Y[i] < 300 and X[i] >= 200 and X[i] < 400:
            num2 = num2 + 1
        elif Y[i] >= 300 and Y[i] < 450 and X[i] >= 200 and X[i] < 400:
            num3 = num3 + 1
        elif Y[i] >= 450 and Y[i] <= 600 and X[i] >= 200 and X[i] <= 400:
            num4 = num4 + 1
    return  num1, num2, num3, num4, num5, num6, num7, num8

def readNC(NCfile):
    fileHandle = Dataset(NCfile)
    X =  fileHandle.variables["EXP"]
    Y =  fileHandle["EYP"][:]
    X = numpy.array(X)
    fileHandle.close()
    length = X.shape[0]
    num1, num2, num3, num4, num5, num6, num7, num8 = 0,0,0,0,0,0,0,0
    # 0---------------------------------600
    #    5        6       7       8
    # ----------------------------------
    #    1        2       3       4
    # 400-------------------------------
    for i in range(length):
        print Y[i]
        if Y[i] >= 0 and Y[i] < 150 and X[i] >= 0 and X[i] <200:
            num5 = num5 + 1
        elif Y[i] >= 150 and Y[i] < 300 and X[i] >= 0 and X[i] < 200:
            num6 = num6 + 1
        elif Y[i] >= 300 and Y[i] < 450 and X[i] >= 0 and X[i] < 200:
            num7 = num7 + 1
        elif Y[i] >= 450 and Y[i] < 600 and X[i] >= 0 and X[i] < 200:
            num8 = num8 + 1
        elif Y[i] >= 0 and Y[i] < 150 and X[i] >= 200 and X[i] < 400:
            num1 = num1 + 1
        elif Y[i] >= 150 and Y[i] < 300 and X[i] >= 200 and X[i] < 400:
            num2 = num2 + 1
        elif Y[i] >= 300 and Y[i] < 450 and X[i] >= 200 and X[i] < 400:
            num3 = num3 + 1
        elif Y[i] >= 450 and Y[i] <= 600 and X[i] >= 200 and X[i] <= 400:
            num4 = num4 + 1
    return  num1, num2, num3, num4, num5, num6, num7, num8
def getEveryDay(begin_date, end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list
if __name__ == "__main__":
    # inputPath = "D:\\temp_10.24.189.195\\20180726\\"
    # outputFile = "D:\\temp_10.24.189.195\\EventFlashNumber.txt"
    # startTime = "2018-06-26"
    # endTime = "2018-06-27"
    startTime = "2018-08-07"
    endTime = "2018-08-07"
    dates = getEveryDay(startTime, endTime)
    # print dates
    for date_tmp in dates:
        print date_tmp

        # inputPath = "F:\\LMI\\"+date_tmp+"\\"
        inputPath = "D:/temp_10.24.189.195/LIO_mp/L1B_event_20180807/"
        outputFile = "D:\\temp_10.24.189.195\\EventFlashNumber_L1B_8_ranges_"+date_tmp+".txt"

        f_txt = open(outputFile,"w")
        title = u"                                     文件名称                   " \
                u"                            1      2     3     4     5     6     7     8   总计\n"
        f_txt.write(title.encode("utf-8"))
        files = os.listdir(inputPath)
        index = 0
        # for f in files:
        #     if "LMIE" in f and ".NC" in f:
        #         file = inputPath + f
        #         print "file",file
        #         try:
        #             # num1, num2, num3, num4, num5, num6, num7, num8 = readNC(file)
        #             num1, num2, num3, num4, num5, num6, num7, num8 = read_L1B_HDF(file)
        #             all =  num1 + num2 + num3 + num4 + num5 + num6 + num7 + num8
        #             f_txt.write(f)
        #             f_txt.write("%6d%6d%6d%6d%6d%6d%6d%6d%6d\n"%(num1,num2,num3,num4,num5,num6,num7,num8,all))
        #         except:
        #             print "Wrong!-->",f
        #             continue
        for f in files:
            print f
            if "L1B_EVT" in f and ".HDF" in f:
                file = inputPath + f
                try:
                    num1, num2, num3, num4, num5, num6, num7, num8 = read_L1B_HDF(file)
                    all =  num1 + num2 + num3 + num4 + num5 + num6 + num7 + num8
                    f_txt.write(f)
                    f_txt.write("%6d%6d%6d%6d%6d%6d%6d%6d%6d\n"%(num1,num2,num3,num4,num5,num6,num7,num8,all))
                except:
                    print "Wrong!-->",f
                    continue
        f_txt.close()
