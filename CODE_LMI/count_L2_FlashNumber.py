#coding=utf-8
from netCDF4 import Dataset
import os
import numpy

def readNC(NCfile):
    fileHandle = Dataset(NCfile)
    X =  fileHandle.variables["FR"]
    # Y =  fileHandle["EYP"][:]
    X = numpy.array(X)
    fileHandle.close()
    length = X.shape[0]
    return  length

def count_L2_FlashNumber(txtFile_L1B,inputPath,outputFile):
    f_txt = open(outputFile,"w")
    files = os.listdir(inputPath)
    f_txt_L1B = open(txtFile_L1B)
    L1Bfiles = f_txt_L1B.readlines()
    f_txt_L1B.close()
    flash_num = 0
    for file_L1B in L1Bfiles:
        startTime = file_L1B.split("_")[9]
        subTask = file_L1B.split("_")[12][1:3]
        string_tmp1 = "FY4A-_LMI---_N_REGX_1047E_L2-_LMIF_SING_NUL_"+startTime+"_"
        string_tmp2 = "_7800M_N"+subTask+"V1"
        for f in files:
            if "LMIF" in f and ".NC" in f:
                if string_tmp1 in f and string_tmp2 in f:
                    # print f

                    file = inputPath + f
                    try:
                        flash_num =  flash_num + readNC(file)
                        # print flash_num
                    except:
                        print "Wrong!-->",f
                        continue
        # print file_L1B[:-1]
        # input("")
        f_txt.write(file_L1B[:-1])
        f_txt.write("%6d\n" % (flash_num))
        flash_num = 0

    f_txt.close()
if __name__ == "__main__":

    txtFile_L1B = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\t.txt"

    inputPath = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_20180807_5s\\"
    outputFile = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_5s.txt"
    count_L2_FlashNumber(txtFile_L1B,inputPath,outputFile)

    inputPath = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_20180807_10s\\"
    outputFile = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_10s.txt"
    count_L2_FlashNumber(txtFile_L1B,inputPath,outputFile)

    inputPath = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_20180807_15s\\"
    outputFile = "D:\\temp_10.24.189.195\\LIO_mp\\LIO_mp_analyse\\countFlashNumber_20180807_15s.txt"
    count_L2_FlashNumber(txtFile_L1B,inputPath,outputFile)