#coding=utf8
import numpy
import matplotlib.pyplot as plt
import time
import re
# def Curve_L2_time_test(txtFile,outputPNG):
#     f_txt = open(txtFile)
#     data = f_txt.readlines()
#     f_txt.close()
#     Time_all = []
#     Time_base = time.strptime("2018-08-07 00:00:00","%Y-%m-%d %H:%M:%S")
#     Time_base = time.mktime(Time_base)
#     num = len(data)
#     for i in range(num):
#         str_tmp = re.split(" |\.",data[i])
#         if len(str_tmp) != 11:#某一行异常 则跳过
#             continue
#         Time = str_tmp[-2]
#         Time = "2018-08-07 "+Time
#         Time = time.strptime(Time,"%Y-%m-%d %H:%M:%S")
#         Time = time.mktime(Time)
#         Time_cost = Time - Time_base
#         Time_all.append(Time_cost)
#     plt.figure(figsize=(20,6))
#     plt.plot(Time_all)
#     plt.xlabel(u"task",size=20)
#     plt.ylabel(u"second",size=20)
#     plt.savefig(outputPNG)
#     plt.close()

# def Curve_flashNum_SERVE():
#     txtFile = ("D:\\temp_10.24.189.195\\20180822\\Flash_number_1min_servise.txt")
#     outputPath = "D:\\temp_10.24.189.195\\20180822\\"
#     outputPNG = outputPath + "Curve_FlashNum_service.png"
#     f_txt = open(txtFile)
#     data = f_txt.readlines()
#     f_txt.close()
#     flashNum_all = []
#     num = len(data)
#     for i in range(num):
#         str_tmp = re.split(" ", data[i])
#         flashNum = int(str_tmp[-1])
#         flashNum_all.append(flashNum)
#     plt.plot(flashNum_all)
#     x = numpy.linspace(0, 100, 10)
#     plt.xlabel(u"each parallel task")
#     plt.ylabel(u"flash number")
#     plt.savefig(outputPNG)
#     plt.close()
#
def Curve_flashNum(inputTxt_60s,inputTxt2,outputPNG):
    f_txt = open(inputTxt_60s)
    data = f_txt.readlines()
    f_txt.close()
    flashNum_all = []
    num = len(data)
    for i in range(num):
        str_tmp = re.split(" ", data[i])
        flashNum = int(str_tmp[-1])
        flashNum_all.append(flashNum)
    f_txt_mp = open(inputTxt2)
    data_mp = f_txt_mp.readlines()
    f_txt_mp.close()
    flashNum_all_mp = []
    num_mp = len(data_mp)
    for i in range(num_mp):
        str_tmp_mp = re.split(" ", data_mp[i])
        flashNum_mp = int(str_tmp_mp[-1])
        flashNum_all_mp.append(flashNum_mp)
    # plt.plot(flashNum_all,color="r")
    # plt.plot(flashNum_all_mp,color="g")
    flashNum_all = numpy.array(flashNum_all)
    flashNum_all_mp = numpy.array(flashNum_all_mp)
    print len(flashNum_all)
    print len(flashNum_all_mp)
    mask = (flashNum_all == 0)
    mask |= (flashNum_all_mp == 0)
    flashNum_all[mask] = flashNum_all[mask] + 1
    flashNum_all_mp[mask] = flashNum_all_mp[mask] + 1
    flashNumber_diff = (flashNum_all_mp - flashNum_all)/numpy.array(flashNum_all,dtype = "f4")
    mash_tmp = flashNumber_diff == -1
    print flashNum_all[mash_tmp]
    print flashNum_all_mp[mash_tmp]
    zero_line = flashNum_all * 0
    plt.figure(figsize=(20,6))
    # plt.subplot(211)
    index = re.search("_2018",outputPNG)
    Title = outputPNG[index.start()+1:-4]
    plt.plot(flashNum_all_mp,color="blue")
    plt.plot(flashNum_all,color="lime")
    plt.xlabel(u"task")
    plt.ylabel(u"flash number")
    plt.axis([0,373,0,80])
    plt.title(Title)
    plt.savefig(outputPNG)
    plt.close()
    outputPNG = outputPNG.replace(".png","_diffRatio.png")
    # plt.subplot(212)
    plt.figure(figsize=(20,6))
    plt.plot(zero_line,color="gray",linestyle = "dashed")
    plt.plot(flashNumber_diff,color="lightseagreen")
    plt.axis([0,373,-1,1])
    plt.xlabel(u"task")
    plt.ylabel(u"diff ratio")
    plt.title(Title)

    plt.savefig(outputPNG)
    plt.close()



# def Curve_L2_time(txtL1B,txtFile,outputPNG):
#     f_txt = open(txtL1B)
#     L1Bfiles = f_txt.readlines()
#     f_txt.close()
#     f_txt = open(txtFile)
#     data = f_txt.readlines()
#     f_txt.close()
#     Time_all = []
#     Time_base = time.strptime("2018-08-07 00:00:00","%Y-%m-%d %H:%M:%S")
#     Time_base = time.mktime(Time_base)
#     num = len(data)
#     time_max = 0
#     for file in L1Bfiles:
#         startTime = file.split("_")[9]
#         subTask = file.split("_")[12][1:3]
#
#         string_tmp = "_1MIN_0"+subTask+"_R N_REGX_1047E "+startTime
#
#         for i in range(num):
#             if string_tmp in data[i]:
#                 str_tmp = re.split(" |\.",data[i])
#                 if len(str_tmp) != 11:#某一行异常 则跳过
#                     continue
#                 Time = str_tmp[-2]
#                 Time = "2018-08-07 "+Time
#                 Time = time.strptime(Time,"%Y-%m-%d %H:%M:%S")
#                 Time = time.mktime(Time)
#                 Time_cost = Time - Time_base
#                 if time_max < Time_cost:
#                     time_max = Time_cost
#         Time_all.append(time_max)
#         time_max = 0
#     plt.figure(figsize=(20,6))
#     plt.plot(Time_all)
#     plt.xlabel(u"task",size=20)
#     plt.ylabel(u"second",size=20)
#     plt.savefig(outputPNG)
#     plt.close()

def Curve_L2_time(txtL1B,txtFile_mp_5s,txtFile_mp_10s,txtFile_mp_15s,txtFile_mp_60s,txtFile_mp_EventNum,outputPath_mp_all):
    time_5s = get_L2_time(txtL1B,txtFile_mp_5s)
    time_10s = get_L2_time(txtL1B,txtFile_mp_10s)
    time_15s = get_L2_time(txtL1B,txtFile_mp_15s)
    time_60s = get_L2_time_60s(txtL1B,txtFile_mp_60s)
    eventNum = get_L1_eventNum(txtL1B,txtFile_mp_EventNum)
    eventNum = numpy.array(eventNum)/50
    print len(time_5s)
    print len(time_10s)
    print len(time_15s)
    print len(eventNum)
    plt.figure(figsize=(20,6))
    plt.plot(time_5s,color = "lime")
    plt.plot(time_10s,color = "b")
    plt.plot(time_15s,color = "orange")
    # plt.plot(time_60s,color = "black")
    # plt.plot(eventNum,color = "gray") # fuchsia

    plt.annotate('green   : 5s\nblue     : 10s\norange : 15s',(10,170))
    plt.xlabel(u"task",size=20)
    plt.ylabel(u"second",size=20)
    plt.axis([0,373,0,200])
    plt.savefig(outputPath_mp_all)
    plt.show()
    plt.close()
def get_L2_time(txtL1B, txtFile):
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
    for file in L1Bfiles:
        startTime = file.split("_")[9]
        subTask = file.split("_")[12][1:3]

        string_tmp = "_1MIN_0"+subTask+"_R N_REGX_1047E "+startTime

        for i in range(num):
            if string_tmp in data[i]:
                str_tmp = re.split(" |\.",data[i])
                if len(str_tmp) != 11:#某一行异常 则跳过
                    continue
                Time = str_tmp[-2]
                Time = "2018-08-07 "+Time
                Time = time.strptime(Time,"%Y-%m-%d %H:%M:%S")
                Time = time.mktime(Time)
                Time_cost = Time - Time_base
                if time_max < Time_cost:
                    time_max = Time_cost
        Time_all.append(time_max)
        time_max = 0
    return Time_all
def get_L2_time_60s(txtL1B, txtFile):
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
    for file in L1Bfiles:
        startTime = file.split("_")[9]
        subTask = file.split("_")[12][1:3]

        string_tmp = "_1MIN_0"+subTask+"_R N_REGX_1047E "+startTime

        for i in range(num):
            if string_tmp in data[i]:
                str_tmp = re.split(" |\.",data[i])
                if len(str_tmp) != 10:#某一行异常 则跳过
                    continue
                Time = str_tmp[-2]
                Time = "2018-08-07 "+Time
                Time = time.strptime(Time,"%Y-%m-%d %H:%M:%S")
                Time = time.mktime(Time)
                Time_cost = Time - Time_base
                if time_max < Time_cost:
                    time_max = Time_cost
        Time_all.append(time_max)
        time_max = 0
    return Time_all
def get_L1_eventNum(txtL1B,txtFile_mp_EventNum):
    f_txt = open(txtL1B)
    L1Bfiles = f_txt.readlines()
    f_txt.close()
    f_txt = open(txtFile_mp_EventNum)
    data = f_txt.readlines()
    f_txt.close()
    eventNum_all = []
    num = len(data)
    for file in L1Bfiles:
        startTime = file.split("_")[9]
        subTask = file.split("_")[12][1:3]

        string_tmp = "FY4A-_LMI---_N_REGX_1047E_L1B_EVT-_SING_NUL_"+startTime
        string_tmp2 = "_N"+subTask+"V1"
        for i in range(num):
            if string_tmp in data[i] and string_tmp2 in data[i]:
                str_tmp = re.split(" ",data[i])
                # if len(str_tmp) != 28 or "EVT" not in data[i]:#某一行异常 则跳过
                #
                #     continue
                # print str_tmp
                eventNum = str_tmp[-1]
                eventNum_all.append(int(eventNum))
    return eventNum_all

if __name__ == "__main__":
    #---->绘制程序运行时间图 开始
    # txtFile_L1B = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\t.txt"

    # txtFile_mp_15s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_15s.txt"
    # outputPath_mp_15s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\Curve_timeCost_15s.png"
    # Curve_L2_time(txtFile_L1B,txtFile_mp_15s,outputPath_mp_15s)
    #
    # txtFile_mp_10s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_10s.txt"
    # outputPath_mp_10s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\Curve_timeCost_10s.png"
    # Curve_L2_time(txtFile_L1B,txtFile_mp_10s,outputPath_mp_10s)
    #
    # txtFile_mp_5s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_5s.txt"
    # outputPath_mp_5s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\Curve_timeCost_5s.png"
    # Curve_L2_time(txtFile_L1B,txtFile_mp_5s,outputPath_mp_5s)
    #<----绘制程序运行时间图 结束


    #---->绘制程序运行时间图 开始
    txtFile_L1B = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\t.txt"
    txtFile_mp_5s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_5s.txt"
    txtFile_mp_10s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_10s.txt"
    txtFile_mp_15s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_15s.txt"
    txtFile_mp_60s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_60s.txt"
    txtFile_mp_EventNum = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\EventFlashNumber_L1B_8_ranges_20180807.txt"
    outputPath_mp_all = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\Curve_timeCost_5s_10s_15s.png"
    Curve_L2_time(txtFile_L1B,txtFile_mp_5s,txtFile_mp_10s,txtFile_mp_15s,txtFile_mp_60s,txtFile_mp_EventNum,outputPath_mp_all)
    #<----绘制程序运行时间图 结束

    #----->绘制闪电个数图 开始
    # txtFile1 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_1min_servise.txt")
    # txtFile2 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_5s.txt")
    # outputPath = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_5s_and_60s.png"
    # Curve_flashNum(txtFile1,txtFile2,outputPath)
    # #
    # txtFile2 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_10s.txt")
    # outputPath = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_10s_and_60s.png"
    # Curve_flashNum(txtFile1,txtFile2,outputPath)
    # #
    # txtFile2 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_15s.txt")
    # outputPath = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_15s_and_60s.png"
    # Curve_flashNum(txtFile1,txtFile2,outputPath)
    #----->绘制闪电个数图 结束
