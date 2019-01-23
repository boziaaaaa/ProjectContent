#coding=utf8
import numpy
import re

def Curve_flashNum(inputTxt_60s,inputTxt2,txtFile_L1B=''):
    # f_L1B = open(txtFile_L1B,"w")
    f_txt = open(inputTxt_60s)
    data = f_txt.readlines()
    f_txt.close()
    f_txt_mp = open(inputTxt2)
    data_mp = f_txt_mp.readlines()
    f_txt_mp.close()
    flashNum_all = []
    flashNum_all_mp = []
    num = len(data)
    num_mp = len(data_mp)
    if num != num_mp:
        print "Wrong!->",num, num_mp
        exit(0)
    index = 0
    for i in range(num):
        str_tmp = re.split(" ", data[i])
        str_tmp_mp = re.split(" ", data_mp[i])
        flashNum = int(str_tmp[-1])
        flashNum_mp = int(str_tmp_mp[-1])
        if flashNum <= 20 or flashNum >50:
            continue
        flashNum_all.append(flashNum)
        flashNum_all_mp.append(flashNum_mp)
        index += 1
        # print data[i],index,"00000000000000000"

        # f_L1B.write(data[i])
        # f_L1B.write('\n')
    # plt.plot(flashNum_all,color="r")
    # plt.plot(flashNum_all_mp,color="g")
    flashNum_all = numpy.array(flashNum_all)
    flashNum_all_mp = numpy.array(flashNum_all_mp)
    mask = (flashNum_all == 0)
    mask |= (flashNum_all_mp == 0)
    flashNum_all[mask] = flashNum_all[mask] + 1
    flashNum_all_mp[mask] = flashNum_all_mp[mask] + 1
    len_all = numpy.sum(flashNum_all)
    len_mp = numpy.sum(flashNum_all_mp)
    print len_all
    print len_mp
    print float(len_mp - len_all)/len_mp
    # f_L1B.close()

if __name__ == "__main__":
    txtFile_L1B = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\file_20_50.txt"

    #----->绘制闪电个数图 开始
    txtFile1 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_1min_servise.txt")
    txtFile2 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_15s.txt")
    Curve_flashNum(txtFile1,txtFile2)

    txtFile2 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_10s.txt")
    Curve_flashNum(txtFile1,txtFile2)

    txtFile2 = ("D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_5s.txt")
    Curve_flashNum(txtFile1,txtFile2)
    #----->绘制闪电个数图 结束
