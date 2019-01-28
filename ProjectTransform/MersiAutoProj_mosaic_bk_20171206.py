# -*-coding=UTF-8-*-
import h5py
import sys
import numpy as N
import os
import glob
import time
from PIL import Image
import re

def MosaicImage_gray(InputFilePath):
    hdf_in = h5py.File(InputFilePath)
    BandData = hdf_in['sea_surface_temperature'].value[:, :]

    temp_Disk = BandData.astype('f4')
    temp_Disk[temp_Disk < -800] = N.nan
    max = N.nanmax(temp_Disk)
    min = N.nanmin(temp_Disk)

    temp_Disk[temp_Disk > max] = max
    temp_Disk[temp_Disk < min] = min

    temp_Disk -= min
    temp_Disk *= 255
    temp_Disk /= (max - min)

    img_Disk = Image.fromarray(temp_Disk.astype(N.uint8))
    JPGname = InputFilePath.replace('.HDF', '.jpg')
    img_Disk.save(JPGname)
    return 0


def Trans(inputArray):
    # "single": [[-888.0,[0,0,0],         "无效值" ],
    #             [65530.0,[120,67, 29 ],  "陆地"    ],
    #             [65532.0,[172,172,166],  "卫星天顶角大于70度" ],
    #             [65535.0,[255,255,255 ,  "外太空"    ]  ],
    # "gradient": [[-5.0,[0,0,139]],
    #             [5.0, [48,12,250]],
    #             [15.0,[41, 194, 207]],
    #             [25.0,[69, 191, 51 ]],
    #             [35.0,[215,219, 38 ]],
    #             [45.0,[236,32,  15 ]] ],
    # single = {    -999.0:[0,0,0],65530.0:[120,67, 29 ],65532.0:[172,172,166],65535.0:[255,255,255] }
    single = {-999.0: [150, 150, 150], 65530.0: [120, 67, 29], 65532.0: [172, 172, 166], 65535.0: [255, 255, 255]}

    gradient = {-5.0: [0, 0, 139],
                5.0: [48, 12, 250],
                15.0: [41, 194, 207],
                25.0: [69, 191, 51],
                35.0: [215, 219, 38],
                45.0: [236, 32, 15]}
    inputArray = N.array(inputArray)
    r = N.zeros(inputArray.shape)
    g = N.zeros(inputArray.shape)
    b = N.zeros(inputArray.shape)

    for key in single:
        r[inputArray == key] = single[key][0]
        g[inputArray == key] = single[key][1]
        b[inputArray == key] = single[key][2]
    for key in gradient:
        if key != 45:
            mask = inputArray >= key
            mask &= inputArray < (key + 10)
            r[mask] = (inputArray[mask] - key) / 10 * (gradient[key + 10][0] - gradient[key][0]) + gradient[key][0]
            g[mask] = (inputArray[mask] - key) / 10 * (gradient[key + 10][1] - gradient[key][1]) + gradient[key][1]
            b[mask] = (inputArray[mask] - key) / 10 * (gradient[key + 10][2] - gradient[key][2]) + gradient[key][2]
            print "00000000000000000"
            print (inputArray[mask] - key) / 10 * (gradient[key + 10][0] - gradient[key][0]), (
            gradient[key + 10][0] - gradient[key][0]), gradient[key][0]
            print (inputArray[mask] - key) / 10 * (gradient[key + 10][1] - gradient[key][1]), (
            gradient[key + 10][1] - gradient[key][1]), gradient[key][1]
            print (inputArray[mask] - key) / 10 * (gradient[key + 10][2] - gradient[key][2]), (
            gradient[key + 10][2] - gradient[key][2]), gradient[key][2]

            print "11111111111111111"

            print r[mask]
            print g[mask]
            print b[mask]
        else:
            mask = inputArray >= key
            r[mask] = gradient[key][0]
            g[mask] = gradient[key][1]
            b[mask] = gradient[key][2]
    return r, g, b


def MosaicImage_RGB(InputFilePath):
    hdf_in = h5py.File(InputFilePath)
    BandData = hdf_in['tsm'].value[:, :]

    mask_t = N.where(BandData > -800)
    BandData[mask_t] = BandData[mask_t] / 100
    '''temp_Disk = BandData.astype('f4')
    temp_Disk[temp_Disk < -800] = N.nan
    max = N.nanmax(temp_Disk)
    min = N.nanmin(temp_Disk)

    temp_Disk[temp_Disk > max] = max
    temp_Disk[temp_Disk < min] = min

    temp_Disk -= min
    temp_Disk *=255
    temp_Disk /=(max - min)'''

    r, g, b = Trans(BandData)  # bb bigger Image Redder
    # print r[r>0]
    # print g[g>0]
    # print b[b>0]
    Height, Width = BandData.shape
    rgbArray = N.zeros((Height, Width, 3), 'uint8')
    rgbArray[..., 0] = r
    rgbArray[..., 1] = g
    rgbArray[..., 2] = b
    OutputImg = Image.fromarray(rgbArray, mode="RGB")
    JPGname = InputFilePath.replace('.HDF', '.jpg')
    OutputImg.save(JPGname)

    return 0

def mosaic(InputFilePath, OutputFilePath, inputTime):
    # print "OutputFile-->", OutputFile
    # print "inputTime",inputTime
    outTime = OutputFilePath[-8:-4]
    print "outTime",outTime

    DatasetsName  = ['Kd490','POC','Zsd','a490','acdom443','bbp_531','chl','salinity','tsm','tur']
    NumOfDatasets = len(DatasetsName)
    hdf_in_temp = h5py.File(InputFilePath)#获取数据维度大小--->
    Band_in_temp = hdf_in_temp[DatasetsName[0]].value[:, :]
    hdf_in_temp.close()
    Height = Band_in_temp.shape[0]
    Width = Band_in_temp.shape[1]  #获取数据维度大小<---
    del Band_in_temp
    print "------------------",NumOfDatasets,Height,Width
    Band_in = N.zeros([NumOfDatasets,Height,Width])
    Band_out = N.zeros([NumOfDatasets,Height,Width])
    Band_mosaic = N.zeros([NumOfDatasets,Height,Width])
    # 读取输入文件
    hdf_in = h5py.File(InputFilePath)
    for i in range(0,NumOfDatasets):
        print "))))))))))))",i,DatasetsName[i]
        Band_in[i] = hdf_in[DatasetsName[i]].value[:, :]
    #创建临时文件
    if (os.path.exists(OutputFilePath) == False):#如果第一次进行图像拼接，则创建被拼接图像，该图像与输入数据一样
        print("create temp HDF file-->")
        print(OutputFilePath)
        OutputHDF = h5py.File(OutputFilePath, 'w')
        for i in range(0,NumOfDatasets):
            OutputHDF.create_dataset(DatasetsName[i], data=Band_in[i])
        OutputHDF.close()
    #打开输出文件 并 对各个数据集进行拼接处理
    hdf_out = h5py.File(OutputFilePath)
    for i in range(0,NumOfDatasets):
        Band_out[i] = hdf_out[DatasetsName[i]].value[:, :]

        mask_in = N.array(Band_in[i])
        mask_in[:, :] = 0
        mask_in[Band_in[i] < 65535] = 1 #筛选输入文件有效值
        mask_in[Band_in[i] == 0.0] = 0  #筛选输入文件有效值
        # mask_in[SunZenith_in/100 > 90] = 0  # if SunZenith greater than 90,abandon
        mask_out = N.array(Band_out[i])
        mask_out[:, :] = 0
        mask_out[Band_out[i] < 65535] = 1 #筛选输出文件（被拼接文件）有效值
        mask_out[Band_out[i] == 0.0] = 0  #筛选输出文件（被拼接文件）有效值
        # mask_out[SunZenith_out/100 > 90] = 0
        mask_total = mask_in + mask_out
        Index_repeat = N.where(mask_total == 2) #求出重叠区域
        #如果两幅图像有重叠区域，则选用新时次数据
        timeIn = int(inputTime[10:14])#输入数据的时间
        timeOut = int(outTime)        #已拼接的数据时间
        if (timeOut > timeIn):  # chose the new data of repeat area
            mask_in[Index_repeat] = 0
        else:
            mask_out[Index_repeat] = 0

        Index_in= N.where(mask_in > 0) #输入文件最终参与拼接的部分
        Index_out = N.where(mask_out > 0)#输出（被拼接）文件最终参与拼接的部分

        Band_mosaic[i] = N.array(Band_in[i])  # can not: Band1_mosaic=Band1_in equal Band1_mosaic=&Band1_in!!!
        Band_mosaic[i][:, :] = 0.0  # fill value

        Band_mosaic[i][Index_in] = Band_in[i][Index_in]
        Band_mosaic[i][Index_out] = Band_out[i][Index_out]

    hdf_in.close()
    hdf_out.close()
    print "InputFile-->", OutputFilePath

    StrCmd = "rm -file " + OutputFilePath
    print StrCmd
    os.system(StrCmd)
    print "InputFile-->", OutputFilePath

    OutputFileNew = OutputFilePath[:-17] + inputTime + OutputFilePath[-4:] #拼写文件名称
    print "================"
    print OutputFileNew
    print OutputFilePath[:-17]
    print inputTime
    print OutputFilePath[-4:]
    #time.sleep(3)
    mosaicHDF = h5py.File(OutputFileNew, 'w')
    for i in range(0,NumOfDatasets):
        mosaicHDF.create_dataset(DatasetsName[i], data=Band_mosaic[i])
    mosaicHDF.close()
    return OutputFileNew


if __name__ == '__main__':
    startTime = time.time()

    # --------->解析调度令
    inputPath_Proj = sys.argv[1]
    ouputPath_Proj = sys.argv[2] + "proj_temp/"
    inputPath_Mosaic = ouputPath_Proj
    outputPath_Mosaic = sys.argv[2]
    date = sys.argv[3]
    xmlfile = sys.argv[4]
    resolution = sys.argv[5]
    # <---------

    # --------->对在所选区域内的水色L2级数据逐个 投影
    if os.path.exists(ouputPath_Proj) == False:
        command = "mkdir " + ouputPath_Proj
        os.system(command)
        print ouputPath_Proj, "not exist,so create!!"

    command = "python /gds/Run/ProjectTransform/MersiAutoProj_run.py " + inputPath_Proj + " " + ouputPath_Proj + " " + date + " " + xmlfile+" "+resolution

    print command
    #time.sleep(10)
    status = -1
    #status = os.system(command)
    print status
    if status == 0:
        print "proj of MERSI Successful!! \n "
    #<---------

    # --------->对投影后的水色L2级数据 拼接
    print "mosaic of MERSI begin!! \n \n L2 file date is:", date
    OutputFile = outputPath_Mosaic + "MERSI_Mosaic_00000000_0000.HDF"
    print inputPath_Mosaic
    files = os.listdir(inputPath_Mosaic)
    inputTime = ''
    for f in files:
        if (".HDF" in f) and (date in f):
            print f
            #inputTime = file[6:15]
            startIndex = re.search(r"(_\d{8}_)",f).start()
            startIndex = startIndex + 1
            inputTime = f[startIndex:startIndex+13]
            inputFile = inputPath_Mosaic + f
            print "inputFile-->",inputFile
            print "OutputFile  ",OutputFile
            print "inputTime",inputTime
            finalOutputFile = mosaic(inputFile, OutputFile, inputTime)
            OutputFile = finalOutputFile
    command = "mv " + OutputFile + " " + outputPath_Mosaic + "MERSI_MOSAIC_" + date + "_PD.HDF"
    print command
    status = os.system(command)
    print status
    if status == 0:
        print "mosaic of MERSI Successful!! \n "
    command = "rm -rf " + ouputPath_Proj  # delete Project files
    print command
    #status = os.system(command)
    if status == 0:
        print "delete ", ouputPath_Proj, " "
    # <--------------

    # ------------>对拼接后的HDF生成真彩色图片
    # FinalHdfFile = outputPath_Mosaic + "FY3C_VIRR_MOSAIC_" + date + "_PD.HDF"
    # # FinalHdfFile = "/gds/DATA/mosaic/FY3C_VIRR_mosaic_20171120.HDF"
    # status = MosaicImage_RGB(FinalHdfFile)
    # if status == 0:
    #     print "Image Success!!! "
    # <-------------

    # ------------>拼接后HDF文件名称和JPG文件名称入库
    # JPGname = FinalHdfFile.replace("HDF", "jpg")
    # command = "python /gds/Run/ProjectTransform/fileNameToSQL.py " + JPGname + " " + FinalHdfFile
    # status = os.system(command)
    # if status == 0:
    #     print "file name write to SQL Success!!! "
    # <-------------

    endTime = time.time()
    print "time cost ", endTime - startTime, "s"
    #time cost  7425.21379805 s
