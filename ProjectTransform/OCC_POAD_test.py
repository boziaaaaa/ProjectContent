# -*-coding=UTF-8-*-
import h5py
import sys
import numpy as N
import os
import glob
import time
import xml.etree.ElementTree as ET
import re
from picture_Base_OCC import MosaicImage_RGB
def addAttr(inputHDF,resolution,maxLon,minLon,maxLat,minLat):
    print "add global attribute"
    centerLat = ((maxLat+minLat)/2)
    centerLon = ((maxLon+minLon)/2)
    str_temp = "+units=m +lon_0="+str(centerLon)+" +datum=WGS84 +proj=latlong _"+str(minLat)+"-"+str(maxLat)+"-"+str(minLon)+"-"+str(maxLon)
    attrs ={u'VResolution':resolution,\
            u'UResolution':resolution,\
            u'SensorName':"MERSI", \
            u'CenterLongitude':centerLon, u'MaxLon':maxLon, u'MinLat':minLat,\
            u'SatelliteName':"FY3B", u'MaxLat':maxLat, \
            u'ProjString':str_temp, \
            u'CenterLatitude':centerLat, u'MinLon':minLon}
    attrs_Data  = {'Kd490':0.0001,
                   'POC':0.01,
                   'Zsd':0.0001,
                   'a490':0.0001,
                   'acdom443':0.0001,
                   'bbp_531':0.0001,
                   'chl':0.0001,
                   'salinity':0.0001,
                   'tsm':0.0001,
                   'tur':1,
                   'Ocean_Flag':1}

    fileHandle = h5py.File(inputHDF)
    for key in attrs.keys():
        fileHandle.attrs[key] = attrs[key]
    for key in attrs_Data:
        fileHandle[key].attrs["Slope"] = attrs_Data[key]
    fileHandle.close()
    return 0

def GetLatlon(xmlfile):
    print xmlfile
    MaxLon = 0
    MinLon = 0
    MaxLat = 0
    MinLat = 0
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    for projrange in root.iter('ProjRange'):
        MaxLon = projrange.find('MaxLon').text
        MinLon = projrange.find('MinLon').text
        MaxLat = projrange.find('MaxLat').text
        MinLat = projrange.find('MinLat').text
    return int(MaxLon),int(MinLon),int(MaxLat),int(MinLat)

def mosaic(InputFilePath, OutputFilePath, inputTime):
    # print "OutputFile-->", OutputFile
    # print "inputTime",inputTime
    outTime = OutputFilePath[-8:-4]
    print "outTime",outTime

    DatasetsName  = ['Ocean_Flag','Kd490','POC','Zsd','a490','acdom443','bbp_531','chl','salinity','tsm','tur']
    NumOfDatasets = len(DatasetsName) #获取数据集个数
    
    hdf_in_temp = h5py.File(InputFilePath)#获取数据维度大小--->
    Band_in_temp = hdf_in_temp[DatasetsName[0]].value[:, :]
    hdf_in_temp.close()
    Height = Band_in_temp.shape[0]
    Width = Band_in_temp.shape[1] 
    del Band_in_temp                      #获取数据维度大小<---
    
    print "------------------",NumOfDatasets,Height,Width
    Band_in = N.zeros([Height,Width]) + 65535  #初始化为无效填充值
    Band_out = N.zeros([Height,Width]) + 65535 #初始化为无效填充值
    Band_mosaic = N.zeros([Height,Width])
    # 读取输入文件
    hdf_in = h5py.File(InputFilePath)

    #创建临时文件 文件数据集均为填充值
    if (os.path.exists(OutputFilePath) == False):#如果第一次进行图像拼接，则创建被拼接图像，该图像与输入数据一样
        print("create temp HDF file-->")
        print(OutputFilePath)
        OutputHDF = h5py.File(OutputFilePath, 'w')
        tempArray = N.zeros([Height,Width])
        tempArray = tempArray + 65535
        #print tempArray
        #print tempArray.shape
        for i in range(0,NumOfDatasets):
            OutputHDF.create_dataset(DatasetsName[i], data=tempArray,dtype=N.int32)
        OutputHDF.close()
        del tempArray
    #打开输出文件 并 对各个数据集进行拼接处理
    hdf_out = h5py.File(OutputFilePath)

    OutputFileNew = OutputFilePath[:-17] + inputTime + OutputFilePath[-4:] #拼写文件名称
    mosaicHDF = h5py.File(OutputFileNew, 'w')

    print "********"
    print InputFilePath
    print OutputFilePath
    print OutputFileNew
    
    for i in range(0,NumOfDatasets):
        print "))))))))))))",i,DatasetsName[i]
        Band_in = hdf_in[DatasetsName[i]].value #[:, :]
          
        Band_out = hdf_out[DatasetsName[i]].value #[:, :]
        print "((((((((((("

        mask_in = N.array(Band_in)
        mask_in[:, :] = 0
        mask_in[Band_in < 65535] = 1 #筛选输入文件有效值
        mask_in[Band_in == 0.0] = 0  #筛选输入文件有效值
        # mask_in[SunZenith_in/100 > 90] = 0  # if SunZenith greater than 90,abandon
        mask_out = N.array(Band_out)
        mask_out[:, :] = 0
        mask_out[Band_out < 65535] = 1 #筛选输出文件（被拼接文件）有效值
        mask_out[Band_out == 0.0] = 0  #筛选输出文件（被拼接文件）有效值
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

        Band_mosaic = N.array(Band_in)  # can not: Band1_mosaic=Band1_in equal Band1_mosaic=&Band1_in!!!
        Band_mosaic[:, :] = 0.0  # fill value

        Band_mosaic[Index_in] = Band_in[Index_in]
        Band_mosaic[Index_out] = Band_out[Index_out]

        mosaicHDF.create_dataset(DatasetsName[i], data=Band_mosaic)
        del Band_in
        del Band_out
    hdf_in.close()
    hdf_out.close()
    mosaicHDF.close()


    StrCmd = "rm -f " + OutputFilePath
    print StrCmd
    os.system(StrCmd)
    print "================"
    print OutputFileNew

    return OutputFileNew

def find_last(string,str):
    last_position=-1
    while True:
        last_position = last_position + 1
        position=string.find(str,last_position)
        if position==-1:
            return last_position
def input_outputPath(configureFile,YYYYMMDD,DayOrNight):
    f_txt = open(configureFile)
    lines = f_txt.readlines()
    inputL1 = ""
    inputGEO = ""
    outputPROJ = ""
    outputMosaic = ""
    outputPicture = ""
    xmlfile = ""
    for line in lines:
        if "inputPath_OCC_L2" in line:
            index_begin = line.find('/')
            index_end = find_last(line,'/')
            inputL1 = line[int(index_begin):int(index_end)] + YYYYMMDD + "/hdf5/"
        elif "inputPath_OCC_GEO" in line:
            index_begin = line.find('/')
            index_end = find_last(line,'/')
            inputGEO = line[int(index_begin):int(index_end)] + YYYYMMDD + "/hdf5/"
        elif "outputPath_OCC_PROJ" in line:
            index_begin = line.find('/')
            index_end = find_last(line,'/')
            outputPROJ = line[int(index_begin):int(index_end)] + YYYYMMDD + "/"#+"hdf5/"
        elif "outputPath_OCC_Mosaic" in line:
            index_begin = line.find('/')
            index_end = find_last(line,'/')
            outputMosaic = line[int(index_begin):int(index_end)]
        # elif "outputPath_OCC_Picture" in line:
        #     index_begin = line.find('/')
        #     index_end = find_last(line,'/')
        #     outputPicture = line[int(index_begin):int(index_end)] + YYYYMMDD + "/" + DayOrNight + "/"
        elif "XML" in line:
            index_begin = line.find('/')
            index_end = line.find('.xml')
            xmlfile = line[int(index_begin):int(index_end)+4]

    return inputL1,inputGEO,outputPROJ,outputMosaic,xmlfile

if __name__ == '__main__':
    startTime = time.time()
    configureFile = "/GDS/SSTWORK/ProjectTransform/PARAM/OCC_proj_mosiac_picture.txt"

    # --------->解析调度令
    date = sys.argv[1]
    dnflag = ""
    resolution = 4000
    inputPath_Proj, geopath, ouputPath_Proj, outputPath_Mosaic, xmlfile \
        = input_outputPath(configureFile, date, dnflag)
    inputPath_Mosaic = ouputPath_Proj
    # <---------
    if os.path.exists(inputPath_Proj) == False:
        print "Wrong!!!inputPath do not exits ",inputPath_Proj
        exit(0)

    # --------->对在所选区域内的水色L2级数据逐个 投影
    if os.path.exists(ouputPath_Proj) == False:
        command = "mkdir " + ouputPath_Proj
        os.system(command)
        print ouputPath_Proj, "not exist,so create!!"

    command = "python /GDS/SSTWORK/ProjectTransform/MersiAutoProj_run.py " + inputPath_Proj + " " + ouputPath_Proj + " " + date + " " + xmlfile+" "+str(resolution)
    print command
    status = -1
    status = os.system(command)
    print status
    if status == 0:
        print "proj of MERSI Successful!! \n "
    #<---------

    # --------->对投影后的水色L2级数据 拼接
    print "mosaic of MERSI begin!! \n \n L2 file date is:", date
    #OutputFile = outputPath_Mosaic + "MERSI_Mosaic_00000000_0000.HDF"
    OutputFile = outputPath_Mosaic + "MERSI_Mosaic_"+str(date)+"_0000.HDF"
    print inputPath_Mosaic
    files = os.listdir(inputPath_Mosaic)
    if len(files) == 0:
        print "Wrong!!!no suitable mosaic inputFile"
        exit(0)
    inputTime = ''
    whichOne = 1
    for f in files:
        if (".HDF" in f) and (date in f):
            print f
            #inputTime = file[6:15]
            startIndex = re.search(r"(_\d{8}_)",f).start()
            startIndex = startIndex + 1
            inputTime = f[startIndex:startIndex+13]
            inputFile = inputPath_Mosaic + f
            print "inputFile-->",inputFile
            print "OutputFile->",OutputFile
            print "inputTime-->",inputTime
            print "whichOne",whichOne
            whichOne = whichOne + 1
            finalOutputFile = mosaic(inputFile, OutputFile, inputTime)
            OutputFile = finalOutputFile
    #outputFile_mosiac = "MERSI_MOSAIC_" + date + "_PD.HDF"
    outputFile_mosiac = "FY3B_MERSI_GBAL_L2_OCC_MLT_GLL_"+date+"_POAD_"+str(resolution)+"M.HDF"
    # command = "mv " + OutputFile + " " + outputPath_Mosaic + "MERSI_MOSAIC_" + date + "_PD.HDF"
    command = "mv " + OutputFile + " " + outputPath_Mosaic +outputFile_mosiac

    print command
    status = os.system(command)
    print status
    if status == 0:
        print "mosaic of MERSI Successful!! \n "
    command = "rm -rf " + ouputPath_Proj  # delete Project files
    print command
    status = os.system(command)
    if status == 0:
        print "delete ", ouputPath_Proj, " "
    # <--------------
    FinalHdfFile = outputPath_Mosaic + outputFile_mosiac

    maxLon, minLon, maxLat, minLat = GetLatlon(xmlfile)
    print "7777777777777777777777777"
    print maxLon, minLon, maxLat, minLat
    addAttr(FinalHdfFile, resolution, maxLon, minLon, maxLat, minLat)


    #------------>对拼接后的HDF生成真彩色图片
    FinalPNGFile = FinalHdfFile.replace(".HDF",".png")
    status = MosaicImage_RGB(FinalHdfFile,FinalPNGFile)
    if status == 0:
        print "Image Success!!! "
    #<-------------

    # ------------>拼接后HDF文件名称和JPG文件名称入库
    # JPGname = FinalHdfFile.replace("HDF", "jpg")
    # command = "python /gds/Run/ProjectTransform/fileNameToSQL.py " + JPGname + " " + FinalHdfFile
    # status = os.system(command)
    # if status == 0:
    #     print "file name write to SQL Success!!! "
    # <-------------

    endTime = time.time()
    print "time cost ", endTime - startTime, "s"