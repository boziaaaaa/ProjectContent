#coding=utf8
import h5py
import os
from PIL import Image
import numpy
import matplotlib.pyplot as plt
import xlwt
def readHDF(inputFile,dataset):
    data = []
    with h5py.File(inputFile) as f:
        for i in f[dataset].keys():
            data.append(i)
    return data

def makeImage(data,outputPNG):
    img = Image.fromarray(data,"L")
    img.show()
    img.save(outputPNG)

if __name__=="__main__":

    # file = r"D:\temp_10.24.34.219\useless\S19891991_TOMS.OZONE.h5"
    # file = r"D:\temp_10.24.34.219\useless\S19461993_COADS_GEOS1.MET_noon.h5"
    file = r"D:\temp_10.24.34.219\useless\MYD08_D3.A2019003.061.2019004190509.h5"
    outputPNG = file.replace(".h5",".png")
    data = readHDF(file,"/mod08/Data Fields")
    # print data
    for i in data:
        print i
        if "water" in i:
            print i


    # workbook = xlwt.Workbook(encoding="ascii")
    # worksheet = workbook.add_sheet("0")
    # for i in range(len(data)):
    #     worksheet.write(i,0,data[i])
    # workbook.save("tst.xls")

    # with xlwt.open("tst.txt","w") as f:
    #     for d in data:
    #         f.write(d)
    #         f.write("\n")
    # makeImage(data,outputPNG)


"Total_Ozone_Mean"
"Cloud_Top_Pressure_Mean"