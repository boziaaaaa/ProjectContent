import os
import re
import numpy

if __name__ == "__main__":
    HDFpath = "D:\\temp_10.24.189.195\\fuse\\"
    Path_FalseNumber = "D:\\temp_10.24.189.195\\false_number"

    files = os.listdir(HDFpath)
    date_last = 0
    FalseNum = 0
    TrueNum = 0

    Index_temp = 0
    result_F = []
    result_T = []

    for file in files:
        if ".txt" in file and "_False" in file:

            if ".txt" in file and "_False" in file:
                with open(HDFpath + file, 'r') as f:
                    for line in f:
                        result_F.append(numpy.int16(line))
                FalseNum = sum(result_F)
            if ".txt" in file and "True" in file:
                with open(HDFpath + file, 'r') as f:
                    for line in f:
                        result_T.append(numpy.int16(line))
                TrueNum = sum(result_T)
            print file

            f = open(Path_FalseNumber + ".txt", "a")
            index = re.search(r"NUL_(\d+)",file)
            date = file[index.start()+4:index.start()+12]
            if Index_temp == 0:
                date_last = date
                Index_temp = 1
            if date_last != date:
                print date_last, date
                f.write(date_last + " " + str(FalseNum) + " "+str(float(FalseNum)/(FalseNum+TrueNum))+ "\n")
                date_last = date
            f.close()
