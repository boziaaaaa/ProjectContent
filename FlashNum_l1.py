#coding=utf-8
import numpy
import h5py
import os

# def XY2number(X,Y):
def XY2number(Y, X):

    length = X.shape[0]
    print length
    num1, num2, num3, num4, num5, num6, num7, num8 = 0,0,0,0,0,0,0,0
    # 0---------------------------------600
    #    5        6       7       8
    # ----------------------------------
    #    1        2       3       4
    # 400-------------------------------
    for i in range(length):
        if X[i] >= 0 and X[i] < 150 and Y[i] >= 0 and Y[i] <200:
            num5 = num5 + 1
        elif X[i] >= 150 and X[i] < 300 and Y[i] >= 0 and Y[i] < 200:
            num6 = num6 + 1
        elif X[i] >= 300 and X[i] < 450 and Y[i] >= 0 and Y[i] < 200:
            num7 = num7 + 1
        elif X[i] >= 450 and X[i] < 600 and Y[i] >= 0 and Y[i] < 200:
            num8 = num8 + 1
        elif X[i] >= 0 and X[i] < 150 and Y[i] >= 200 and Y[i] < 400:
            num1 = num1 + 1
        elif X[i] >= 150 and X[i] < 300 and Y[i] >= 200 and Y[i] < 400:
            num2 = num2 + 1
        elif X[i] >= 300 and X[i] < 450 and Y[i] >= 200 and Y[i] < 400:
            num3 = num3 + 1
        elif X[i] >= 450 and X[i] <= 600 and Y[i] >= 200 and Y[i] <= 400:
            num4 = num4 + 1
        else:
            print X[i],Y[i]
    return  num1, num2, num3, num4, num5, num6, num7, num8
def ReadHDF(path):
    Xlist = []
    Ylist = []
    datas = {}
    fp = h5py.File(path, 'r')
    vdata_times = fp['VData'].keys()
    for times in vdata_times:
        datas[times] = fp['VData'][times].value
    fp.close()
    for times in datas:
        for line in datas[times]:
            X_temp = line[0]
            Y_temp = line[1]
            Xlist.append(X_temp)
            Ylist.append(Y_temp)
    return Xlist, Ylist

if __name__ == "__main__":
    f_txt = open("D:\\temp_10.24.189.195\\EventFlashNumber_L1.txt","w")
    title = u"                                     文件名称                   " \
            u"                             1      2     3     4     5     6     7     8   总计\n"
    f_txt.write(title.encode("utf-8"))

    HDFpath = "D:\\temp_10.24.189.195\\20180726_2\\"
    # HDFfile = "FY4A-_LMI---_N_REGX_1047E_L1B_EVT-_SING_NUL_20180726001510_20180726002449_7800M_N07V1.HDF"
    # f = HDFfile
    files = os.listdir(HDFpath)
    for f in files:
        X, Y = ReadHDF(HDFpath + f)
        X = numpy.array(X)
        Y = numpy.array(Y)
        num1, num2, num3, num4, num5, num6, num7, num8 = XY2number(X, Y)
        all =  num1 + num2 + num3 + num4 + num5 + num6 + num7 + num8
        f_txt.write(f)
        f_txt.write("%6d%6d%6d%6d%6d%6d%6d%6d%6d\n"%(num1,num2,num3,num4,num5,num6,num7,num8,all))
    f_txt.close()
