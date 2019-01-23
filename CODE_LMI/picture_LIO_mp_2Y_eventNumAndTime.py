#coding=utf8
import numpy
import matplotlib.pyplot as plt
import matplotlib
import time
import re

# def Curve_flashNum(inputTxt_60s,inputTxt2,outputPNG):
#     f_txt = open(inputTxt_60s)
#     data = f_txt.readlines()
#     f_txt.close()
#     flashNum_all = []
#     num = len(data)
#     for i in range(num):
#         str_tmp = re.split(" ", data[i])
#         flashNum = int(str_tmp[-1])
#         flashNum_all.append(flashNum)
#     f_txt_mp = open(inputTxt2)
#     data_mp = f_txt_mp.readlines()
#     f_txt_mp.close()
#     flashNum_all_mp = []
#     num_mp = len(data_mp)
#     for i in range(num_mp):
#         str_tmp_mp = re.split(" ", data_mp[i])
#         flashNum_mp = int(str_tmp_mp[-1])
#         flashNum_all_mp.append(flashNum_mp)
#     # plt.plot(flashNum_all,color="r")
#     # plt.plot(flashNum_all_mp,color="g")
#     flashNum_all = numpy.array(flashNum_all)
#     flashNum_all_mp = numpy.array(flashNum_all_mp)
#     print len(flashNum_all)
#     print len(flashNum_all_mp)
#     mask = (flashNum_all == 0)
#     mask |= (flashNum_all_mp == 0)
#     flashNum_all[mask] = flashNum_all[mask] + 1
#     flashNum_all_mp[mask] = flashNum_all_mp[mask] + 1
#     flashNumber_diff = (flashNum_all_mp - flashNum_all)/numpy.array(flashNum_all,dtype = "f4")
#     mash_tmp = flashNumber_diff == -1
#     print flashNum_all[mash_tmp]
#     print flashNum_all_mp[mash_tmp]
#     zero_line = flashNum_all * 0
#     plt.figure(figsize=(20,6))
#     # plt.subplot(211)
#     index = re.search("_2018",outputPNG)
#     Title = outputPNG[index.start()+1:-4]
#     plt.plot(flashNum_all_mp,color="blue")
#     plt.plot(flashNum_all,color="lime")
#     plt.xlabel(u"task")
#     plt.ylabel(u"flash number")
#     plt.axis([0,373,0,80])
#     plt.title(Title)
#     plt.savefig(outputPNG)
#     plt.close()
#     outputPNG = outputPNG.replace(".png","_diffRatio.png")
#     # plt.subplot(212)
#     plt.figure(figsize=(20,6))
#     plt.plot(zero_line,color="gray",linestyle = "dashed")
#     plt.plot(flashNumber_diff,color="lightseagreen")
#     plt.axis([0,373,-1,1])
#     plt.xlabel(u"task")
#     plt.ylabel(u"diff ratio")
#     plt.title(Title)
#
#     plt.savefig(outputPNG)
#     plt.close()

def Curve_L2_time(txtL1B,txtFile_mp_5s,txtFile_mp_10s,txtFile_mp_15s,txtFile_mp_60s,txtFile_mp_EventNum,outputPath_mp_all):
    time_5s = get_L2_time(txtL1B,txtFile_mp_5s)
    time_10s = get_L2_time(txtL1B,txtFile_mp_10s)
    time_15s = get_L2_time(txtL1B,txtFile_mp_15s)
    # time_60s = get_L2_time_60s(txtL1B,txtFile_mp_60s)
    eventNum = get_L1_eventNum(txtL1B,txtFile_mp_EventNum)
    eventNum = numpy.array(eventNum)
    myfont = matplotlib.font_manager.FontProperties(fname="C:/Windows/Fonts/simsun.ttc")

    fig = plt.figure(figsize=(20,6))
    fig_sub1 = fig.subplots()
    fig_sub1.set_ylabel(u"运\n行\n时\n间",fontproperties=myfont,rotation=0,size=15)
    fig_sub1.axis([0,373,0,200])
    fig_sub1.set_xlabel(u"子任务",fontproperties=myfont,rotation=0,size=15)
    fig_sub1.plot(time_5s,color = "lime")
    plt.plot(time_10s,color = "blue")
    plt.plot(time_15s,color = "orange")
    # plt.plot(time_60s,color = "black")
    fig_sub2 = fig_sub1.twinx()
    fig_sub2.plot(eventNum,color = "black") # fuchsia
    fig_sub2.set_ylabel(u"事\n件\n个\n数",fontproperties=myfont,rotation=0,size=15)
    fig_sub2.axis([0,373,0,5000])

    # plt.annotate('green   : 5s\nblue     : 10s\norange : 15s',(10,170))
    plt.annotate(u'绿色 : 5秒拆分并行程序运行时间\n蓝色 : 10秒拆分并行程序运行时间\n橙色 : 15秒拆分并行程序运行时间\n黑色 : L1B闪电事件个数',(10,4000),fontproperties=myfont,size=15)
    plt.title(u"并行程序运行时间和L1B闪电事件个数对比图",fontproperties=myfont,size=15)
    plt.savefig(outputPath_mp_all)
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
# def get_L2_time_60s(txtL1B, txtFile):
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
#                 if len(str_tmp) != 10:#某一行异常 则跳过
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
#     return Time_all
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
                eventNum = str_tmp[-1]
                eventNum_all.append(int(eventNum))
    return eventNum_all

if __name__ == "__main__":
    #---->绘制程序运行时间图 开始
    txtFile_L1B = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\t.txt"
    txtFile_mp_5s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_5s.txt"
    txtFile_mp_10s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_10s.txt"
    txtFile_mp_15s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_15s.txt"
    txtFile_mp_60s = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\time_60s.txt"
    txtFile_mp_EventNum = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\EventFlashNumber_L1B_8_ranges_20180807.txt"
    # outputPath_mp_all = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\Curve_timeCost_5s_EventNumber.png"
    # outputPath_mp_all = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\Curve_timeCost_5s_10s_15s_EventNumber.png"
    outputPath_mp_all = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\qqqqqqqqq.png"

    Curve_L2_time(txtFile_L1B,txtFile_mp_5s,txtFile_mp_10s,txtFile_mp_15s,txtFile_mp_60s,txtFile_mp_EventNum,outputPath_mp_all)
    #<----绘制程序运行时间图 结束

