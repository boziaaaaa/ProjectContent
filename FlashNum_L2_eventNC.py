#coding=utf-8
from netCDF4 import Dataset
import os
import numpy
# def readNC_bk(NCfile):
#     fileHandle = Dataset(NCfile)
#     dataset =  fileHandle["ER"][:]
#     fileHandle.close()
#     return str(dataset.shape[0])
# if __name__ == "__main__":
#     inputPath = "D:\\temp_10.24.189.195\\20180726\\"
#     outputFile = "D:\\temp_10.24.189.195\\EventFlashNumber.txt"
#     f_txt = open(outputFile,"w")
#     title = u"                                     文件名称                   " \
#             u"                          闪电个数  \n"
#     f_txt.write(title.encode("utf-8"))
#     files = os.listdir(inputPath)
#     index = 0
#     for f in files:
#         if "LMIE" in f and ".NC" in f:
#             file = inputPath + f
#             try:
#                 length = readNC(file)
#                 f_txt.write(f)
#                 f_txt.write("    ")
#                 f_txt.write(length)
#                 f_txt.write("\n")
#             except:
#                 print "Wrong!-->",f
#                 continue
#         index = index + 1
#         if index == 2:
#             break
#     f_txt.close()
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
        # for i_x in range(0,4):
        #     for i_y in range(0,2):
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
    return  num1, num2, num3, num4, num5, num6, num7, num8
if __name__ == "__main__":
    inputPath = "D:\\temp_10.24.189.195\\20180726\\"
    outputFile = "D:\\temp_10.24.189.195\\EventFlashNumber.txt"
    f_txt = open(outputFile,"w")
    title = u"                                     文件名称                   " \
            u"                            1      2     3     4     5     6     7     8   总计\n"
    f_txt.write(title.encode("utf-8"))
    files = os.listdir(inputPath)
    index = 0
    for f in files:
        if "LMIE" in f and ".NC" in f:

            # if index == 1:
            #     break
            # index = index + 1

            file = inputPath + f
            try:
                num1, num2, num3, num4, num5, num6, num7, num8 = readNC(file)
                all =  num1 + num2 + num3 + num4 + num5 + num6 + num7 + num8
                f_txt.write(f)
                f_txt.write("%6d%6d%6d%6d%6d%6d%6d%6d%6d\n"%(num1,num2,num3,num4,num5,num6,num7,num8,all))
            except:
                print "Wrong!-->",f
                continue
    f_txt.close()