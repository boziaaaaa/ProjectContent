#coding=utf8
import numpy
import time
import re

def analyse_L2_time(txtL1B,txtFile):
    f_txt = open(txtL1B)
    L1Bfiles = f_txt.readlines()
    f_txt.close()
    f_txt = open(txtFile)
    data = f_txt.readlines()
    f_txt.close()
    Time_all = []
    Time_base = time.strptime("2018-08-07 00:00:00","%Y-%m-%d %H:%M:%S")
    Time_base = time.mktime(Time_base)
    num = len(data)
    time_max = 0
    index = 0

    for file in L1Bfiles:
        startTime = file[0:14]
        subTask = file[37:39]
        string_tmp = "_1MIN_0"+subTask+"_R N_REGX_1047E "+startTime
        for i in range(num):
            if string_tmp in data[i]:
                str_tmp = re.split(" |\.",data[i])
                if len(str_tmp) != 11:#某一行异常 则跳过
                    continue
                # print str_tmp
                Time = str_tmp[-2]
                Time = "2018-08-07 "+Time
                Time = time.strptime(Time,"%Y-%m-%d %H:%M:%S")
                Time = time.mktime(Time)
                Time_cost = Time - Time_base
                if time_max < Time_cost:
                    time_max = Time_cost
                index += 1
        Time_all.append(time_max)
        time_max = 0
    # print "index",index
    index = 0

    Time_all = numpy.array(Time_all)
    Time_all = Time_all[Time_all>0]
    # Time_all = Time_all[Time_all<100]
    print numpy.mean(Time_all)
    print numpy.max(Time_all),"\n"
if __name__ == "__main__":

    #---->绘制程序运行时间图 开始
    # txtFile_L1B = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\t.txt"
    txtFile_L1B = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\file_20_50.txt"

    txtFile_mp_15s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_15s.txt"
    analyse_L2_time(txtFile_L1B,txtFile_mp_15s)

    txtFile_mp_10s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_10s.txt"
    analyse_L2_time(txtFile_L1B,txtFile_mp_10s)

    txtFile_mp_5s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_5s.txt"
    analyse_L2_time(txtFile_L1B,txtFile_mp_5s)
    #<----绘制程序运行时间图 结束



