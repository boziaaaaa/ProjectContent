#coding=utf8
import numpy
import matplotlib.pyplot as plt
import matplotlib
import time
import re

# def a(flash_time,diff_ratio):
#     print flash_time
#     print diff_ratio
#     fig = plt.figure()
#     myfont = matplotlib.font_manager.FontProperties(fname="C:/Windows/Fonts/simsun.ttc")
#     fig_sub_1 = fig.subplots()
#     fig_sub_1.plot(flash_time,"dodgerblue")
#     fig_sub_1.set_ylabel(u"运\n行\n时\n间",fontproperties=myfont,rotation=0)
#     fig_sub_2 = fig_sub_1.twinx()
#     fig_sub_2.plot(diff_ratio,'lawngreen')
#     fig_sub_2.set_ylabel(u"差\n异\n比\n例",fontproperties=myfont,rotation=0)
#     plt.xticks((0,1,2,3),("5s","10s","15s",   "60s"))
#     plt.title(u"分析图",fontproperties=myfont)
#     plt.show()
#     plt.close()
# def analyse(data):
def analyse(flash_time,diff_ratio,flash_time_0_20,diff_ratio_0_20,
            flash_time_20_30,diff_ratio_20_30,flash_time_30_40,diff_ratio_30_40,
            flash_time_40_50,diff_ratio_40_50,flash_time_50,diff_ratio_50,
            flash_time_20_50,diff_ratio20__50,
            outputPicture):
    # print flash_time
    # print diff_ratio
    fig = plt.figure()
    myfont = matplotlib.font_manager.FontProperties(fname="C:/Windows/Fonts/simsun.ttc")
    fig_sub_1 = fig.subplots()
    fig_sub_1.set_ylabel(u"运\n行\n时\n间",fontproperties=myfont,rotation=0)
    fig_sub_2 = fig_sub_1.twinx()
    fig_sub_2.set_ylabel(u"差\n异\n比\n例",fontproperties=myfont,rotation=0)
    # fig_sub_1.plot(flash_time,"gray")
    # fig_sub_2.plot(diff_ratio,'gray',linestyle=":")
    fig_sub_1.plot(flash_time_0_20,"dodgerblue")
    fig_sub_2.plot(diff_ratio_0_20,'dodgerblue',linestyle=":")
    # fig_sub_1.plot(flash_time_20_30,"lawngreen")
    # fig_sub_2.plot(diff_ratio_20_30,'lawngreen',linestyle=":")
    # fig_sub_1.plot(flash_time_30_40,"yellow")
    # fig_sub_2.plot(diff_ratio_30_40,'yellow',linestyle=":")
    # fig_sub_1.plot(flash_time_40_50,"orangered")
    # fig_sub_2.plot(diff_ratio_40_50,'orangered',linestyle=":")
    fig_sub_1.plot(flash_time_50,"purple")
    fig_sub_2.plot(diff_ratio_50,'purple',linestyle=":")
    fig_sub_1.plot(flash_time_20_50,"yellow")
    fig_sub_2.plot(diff_ratio_20_50,'yellow',linestyle=":")

    # plt.annotate(u"黑色：所有\n蓝色：0~20\n绿色：20~30\n黄色：30~40\n红色：40~50\n紫色：>50",(1,0.26),fontproperties=myfont,fontsize = 8,rotation=0)
    #plt.annotate(u"蓝色： 0~20  实线：运行时间 \n绿色：20~30  虚线：闪电个数差异比例\n黄色：30~40\n红色：40~50\n紫色：>50",(0.8,0.26),fontproperties=myfont,fontsize = 8,rotation=0)
    plt.annotate(u"蓝色： 0~20  实线：运行时间 \n黄色：20~50  虚线：闪电个数差异比例\n紫色：>50",(0.8,0.26),fontproperties=myfont,fontsize = 8,rotation=0)

    plt.xticks((0,1,2,3),("5s","10s","15s",   "60s"))
    plt.title(u"分析图",fontproperties=myfont)
    # plt.show()
    plt.savefig(outputPicture,dpi=200)
    plt.close()
if __name__ == "__main__":
    outputPicture = "D:\\temp_10.24.189.195\LIO_mp\\LIO_mp_analyse\\final_2.png"
    flash_time = [24.6621983914,31.6246648794,34.2064343164,60]
    diff_ratio = [0.207624487769,0.0804355071659,0.048969906159,0]

    flash_time_0_20 = [19.8527607362,23.2883435583,23.3374233129,60]
    diff_ratio_0_20 = [0.330691642651,0.122114216282,0.0701042873696,0]

    flash_time_20_30 = [23.9365079365,40.0317460317,37.2380952381,60]
    diff_ratio_20_30 = [0.223076923077,0.0957960027567,0.046741277156,0]

    flash_time_30_40 = [28.5245901639,35.6721311475,42.2786885246,60]
    diff_ratio_30_40 = [0.177717391304,0.0727722772277,0.0488867376573,0]

    flash_time_40_50 = [32.224137931,38.3620689655,47.3448275862,60]
    diff_ratio_40_50 = [0.169522091975,0.057911908646,0.0413488558812,0]

    flash_time_50 = [30.2142857143,38.4642857143,45.8571428571,60]
    diff_ratio_50 = [0.168324407039,0.0663407821229,0.0394826412526,0]

    flash_time_20_50 = [28.1153846154,38.0384615385,42.1483516484,60]
    diff_ratio_20_50 = [0.185330347144,0.0722606787101,0.0452600394997,0]



    analyse(flash_time,diff_ratio,flash_time_0_20,diff_ratio_0_20,
            flash_time_20_30,diff_ratio_20_30,flash_time_30_40,diff_ratio_30_40,
            flash_time_40_50,diff_ratio_40_50,flash_time_50,diff_ratio_50,
            flash_time_20_50,diff_ratio_20_50,
            outputPicture)