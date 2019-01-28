# -*-coding=UTF-8-*-
import h5py
import sys
import numpy as N
import os
import glob
import time
from PIL import Image
import xml.etree.ElementTree as ET
import MySQLdb
import re
from picture_Base import MosaicImage_RGB


def addAttr(inputHDF, resolution, maxLon, minLon, maxLat, minLat):
    print "add global attribute"
    centerLat = ((maxLat + minLat) / 2)
    centerLon = ((maxLon + minLon) / 2)
    str_temp = "+units=m +lon_0=" + str(centerLon) + " +datum=WGS84 +proj=latlong _" + str(minLat) + "-" + str(
        maxLat) + "-" + str(minLon) + "-" + str(maxLon)
    attrs = {u'VResolution': resolution, \
             u'UResolution': resolution, \
             u'SensorName': "VIRR", \
             u'CenterLongitude': centerLon, u'MaxLon': maxLon, u'MinLat': minLat, \
             u'SatelliteName': "FY3C", u'MaxLat': maxLat, \
             u'ProjString': str_temp, \
             u'CenterLatitude': centerLat, u'MinLon': minLon}

    attrs_Data = {u"FillValue": "", \
                  u"Intercept": 0.0, \
                  u"Slope": 0.01, \
                  u"band_name": 0, \
                  u"long_name": "Sea Surface Temperature", \
                  u"units": "Degree", \
                  u"valid_range": [-200, 3500]}

    fileHandle = h5py.File(inputHDF)
    for key in attrs.keys():
        fileHandle.attrs[key] = attrs[key]
    for key in attrs_Data.keys():
        fileHandle["sea_surface_temperature"].attrs[key] = attrs_Data[key]
    fileHandle.close()
    return 0


def addLatLon(HDF, resolution, maxLon, minLon, maxLat, minLat):
    print "add Lat Lon"
    print HDF
    fileHandle = h5py.File(HDF)
    dataset = fileHandle["sea_surface_temperature"].value
    Height, Width = dataset.shape

    longitude = N.linspace(minLon, maxLon, int(Width))
    longitude = N.tile(longitude, int(Height))
    longitude = longitude.reshape(int(Height), int(Width)).astype('f4')
    if maxLon > 180:
        longitude[longitude > 180] -= 360
        longitude[longitude < -180] + 360
    latitude = N.linspace(maxLat, minLat, Height)
    latitude = N.tile(latitude, int(Width))
    latitude = latitude.reshape(int(Width), int(Height)).astype('f4')
    latitude = latitude.T

    fileHandle.create_dataset("latitude", data=latitude)
    fileHandle.create_dataset("longitude", data=longitude)
    fileHandle.close()

    addAttr(HDF, resolution, maxLon, minLon, maxLat, minLat)

    return 0


def mosaic(InputFilePath, OutputFilePath, inputTime):
    outTime = OutputFilePath[-8:-4]  # hour and minute

    # read data
    hdf_in = h5py.File(InputFilePath)
    Band1_in = hdf_in['sea_surface_temperature'].value[:, :]
    Band2_in = hdf_in['quality_flag'].value[:, :]  # yuanbo 20180824

    if (os.path.exists(OutputFilePath) == False):
        print("create temp HDF file-->")
        print(OutputFilePath)
        OutputHDF = h5py.File(OutputFilePath, 'w')
        OutputHDF.create_dataset("sea_surface_temperature", data=Band1_in)
        OutputHDF.create_dataset("quality_flag", data=Band2_in)  # yuanbo 20180824
        OutputHDF.close()
    hdf_out = h5py.File(OutputFilePath)
    Band1_out = hdf_out['sea_surface_temperature'].value[:, :]
    Band2_out = hdf_out['quality_flag'].value[:, :]

    mask_in = N.array(Band1_in)
    mask_in[:, :] = 0
    mask_in[(Band1_in < 32767) & (Band1_in > -900)] = 1


    mask_out = N.array(Band1_out)
    mask_out[:, :] = 0
    mask_out[(Band1_out < 32767) & (Band1_out > -900)] = 1  #

    mask_total = mask_in + mask_out
    Index_repeat = N.where(mask_total == 2)

    # ------>20180914 yuanbo
    try:
        repeat_idx = N.argwhere(Band2_in[Index_repeat] >= Band2_out[Index_repeat])
        mask_in[Index_repeat[0][repeat_idx], Index_repeat[1][repeat_idx]] = 0
        repeat_idx = N.argwhere(Band2_in[Index_repeat] < Band2_out[Index_repeat])
        mask_out[Index_repeat[0][repeat_idx], Index_repeat[1][repeat_idx]] = 0
    except:
        pass
    # <------20180914 yuanbo

    Index_in = N.where(mask_in > 0)
    Index_out = N.where(mask_out > 0)

    Band1_mosaic = N.array(Band1_in)  # can not: Band1_mosaic=Band1_in equal Band1_mosaic=&Band1_in!!!
    Band1_mosaic[:, :] = -999.0  # fill value
    Band1_mosaic[Index_in] = Band1_in[Index_in]
    Band1_mosaic[Index_out] = Band1_out[Index_out]

    Band2_mosaic = N.array(Band2_in)  # yuanbo 20180824
    Band2_mosaic[:, :] = -999.0  # yuanbo 20180824
    Band2_mosaic[Index_in] = Band2_in[Index_in]  # yuanbo 20180824
    Band2_mosaic[Index_out] = Band2_out[Index_out]  # yuanbo 20180824

    hdf_in.close()
    hdf_out.close()
    # print "InputFile-->", OutputFilePath

    StrCmd = "rm -f " + OutputFilePath  # delete the temp mosaic HDF
    print StrCmd
    os.system(StrCmd)

    finalOutputFile = OutputFilePath[:-8] + inputTime + OutputFilePath[-4:]
    mosaicHDF = h5py.File(finalOutputFile, 'w')
    mosaicHDF.create_dataset("sea_surface_temperature", data=Band1_mosaic)
    mosaicHDF.create_dataset("quality_flag", data=Band2_mosaic)
    mosaicHDF.close()
    return finalOutputFile


def OverWriteXML(xmlfile, MaxLon, MinLon, MaxLat, MinLat):
    print xmlfile
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    for ProjInfor in root.iter('ProjInfor'):
        ProjInfor.find('CentralLon').text = str(int(float(MaxLon + MinLon) / 2))

    for projrange in root.iter('ProjRange'):
        projrange.find('MaxLon').text = str(int(MaxLon))
        projrange.find('MinLon').text = str(int(MinLon))
        projrange.find('MaxLat').text = str(int(MaxLat))
        projrange.find('MinLat').text = str(int(MinLat))
    os.system("rm " + xmlfile)
    tree.write(xmlfile)
    return 0


def LoadLatLon():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='gds',
        passwd='gds',
        db='GDS',
    )
    cur = conn.cursor()
    checkSQL = "SELECT * FROM SST_Area_Config WHERE Valid = '1'"  # WHERE JPGfile "#> '%s'" % (1000)
    cur.execute(checkSQL)
    results = cur.fetchall()
    print results
    cur.close()
    conn.close()
    List = []
    for i in range(0, len(results)):
        if results[i][6] != 0:
            List.append(
                [int(results[i][0]), int(results[i][2]), int(results[i][3]), int(results[i][4]), int(results[i][5])])
    return List


def FindLocate(MaxLat, MinLon, maxlon, minlon, maxlat, minlat, resolution):
    # resolution = 1000
    factor = 100000 / resolution
    row_up = (MaxLat - maxlat) * factor + 1
    row_down = (MaxLat - minlat) * factor + 1
    column_left = (minlon - MinLon) * factor + 1
    column_right = (maxlon - MinLon) * factor + 1
    return row_up, row_down, column_left, column_right


def CreateSmallRangeFile(FinalHdfFile, MaxLat, MinLon, latlon, resolution):
    temp_string = str(latlon[0])
    temp_string = temp_string.zfill(5)
    newHDFfile = FinalHdfFile.replace("00000", temp_string)
    import h5py
    filehandle = h5py.File(FinalHdfFile, "r")
    dataset = filehandle["sea_surface_temperature"][:, :]
    dataset_QA = filehandle["quality_flag"][:, :]  # yuanbo 20180824

    filehandle.close()
    maxlon = latlon[4]
    minlon = latlon[2]
    maxlat = latlon[1]
    minlat = latlon[3]
    print MaxLat, MinLon, maxlon, minlon, maxlat, minlat
    row_up, row_down, column_left, column_right = FindLocate(MaxLat, MinLon, maxlon, minlon, maxlat, minlat, resolution)
    print row_up, row_down, column_left, column_right
    newDataset = dataset[row_up:row_down, column_left:column_right]
    newDataset_QA = dataset_QA[row_up:row_down, column_left:column_right]

    index_temp = re.search("FY3C_", newHDFfile)
    newHDFpath = newHDFfile[:index_temp.start()]

    if os.path.exists(newHDFpath) == False:
        os.system("mkdir -p " + newHDFpath)

    filehandle = h5py.File(newHDFfile, "w")
    filehandle.create_dataset("sea_surface_temperature", data=newDataset)
    filehandle.create_dataset("quality_flag", data=newDataset_QA)
    filehandle.close()
    return newHDFfile


def find_last(string, str):
    last_position = -1
    while True:
        last_position = last_position + 1
        position = string.find(str, last_position)
        if position == -1:
            return last_position


def input_outputPath(configureFile, YYYYMMDD, DayOrNight):
    f_txt = open(configureFile)
    lines = f_txt.readlines()
    inputL1 = ""
    inputGEO = ""
    outputPROJ = ""
    outputMosaic = ""
    outputPicture = ""
    xmlfile = ""
    for line in lines:
        if "inputPath_SST_L1" in line:
            index_begin = line.find('/')
            index_end = find_last(line, '/')
            inputL1 = line[int(index_begin):int(index_end)] + YYYYMMDD + "/" + DayOrNight + "/"
        elif "inputPath_SST_GEO" in line:
            index_begin = line.find('/')
            index_end = find_last(line, '/')
            inputGEO = line[int(index_begin):int(index_end)]
        elif "outputPath_SST_PROJ" in line:
            index_begin = line.find('/')
            index_end = find_last(line, '/')
            outputPROJ = line[int(index_begin):int(index_end)] + YYYYMMDD + "/" + DayOrNight + "/"
        elif "outputPath_SST_Mosaic" in line:
            index_begin = line.find('/')
            index_end = find_last(line, '/')
            outputMosaic = line[int(index_begin):int(index_end)]
            # elif "outputPath_SST_Picture" in line:
        # index_begin = line.find('/')
        #     index_end = find_last(line,'/')
        #     outputPicture = line[int(index_begin):int(index_end)] + YYYYMMDD + "/" + DayOrNight + "/"
        elif "XML" in line:
            index_begin = line.find('/')
            index_end = line.find('.xml')

            xmlfile = line[int(index_begin):int(index_end) + 4]

    return inputL1, inputGEO, outputPROJ, outputMosaic, xmlfile


if __name__ == '__main__':
    configureFile = "/GDS/SSTWORK/ProjectTransform/PARAM/SST_proj_mosiac_picture.txt"
    resolution = 5000
    startTime = time.time()
    # --------->analyse command
    date = sys.argv[1]
    dnflag = sys.argv[2]
    inputPath_Proj, geopath, ouputPath_Proj, outputPath_Mosaic, xmlfile \
        = input_outputPath(configureFile, date, dnflag)
    inputPath_Mosaic = ouputPath_Proj
    print inputPath_Proj, geopath, ouputPath_Proj, outputPath_Mosaic, xmlfile
    if os.path.exists(inputPath_Proj) == False:
        print "Path Not Exists : ", inputPath_Proj
        exit(0)
    # <---------

    # --------->rewrite XML
    print(inputPath_Proj)
    latlon = LoadLatLon()  # get latlon range form SQL
    latlon = N.array(latlon)
    MaxLat = max(latlon[:, 1])
    MinLon = min(latlon[:, 2])
    MinLat = min(latlon[:, 3])
    Maxlon = max(latlon[:, 4])
    # print "XML Maxlon, MinLon, MaxLat, MinLat :",Maxlon, MinLon, MaxLat, MinLat
    OverWriteXML(xmlfile, Maxlon, MinLon, MaxLat, MinLat)  # make XML file(according to the new latlon of SQL)
    # <---------

    # --------->begin to Project
    if os.path.exists(ouputPath_Proj) == False:
        command = "mkdir -p " + ouputPath_Proj
        os.system(command)
        print ouputPath_Proj, "not exist,so create!!"
    command = "python /GDS/SSTWORK/ProjectTransform/FY3CAutoProj_run.py " + inputPath_Proj + " " + ouputPath_Proj + " " + date + " " + xmlfile + " " + geopath + " " + dnflag
    print command
    status = -1
    status = os.system(command)  #################
    print status
    if status == 0:
        print "proj of VIRR Successful!!"
    # <---------end Proj

    # --------->begin to Mosaic
    print "mosaic of VIRR begin!! \nL2 file date is:", date
    if os.path.exists(outputPath_Mosaic + '00000/') == False:
        command = "mkdir -p " + outputPath_Mosaic + '00000/'
        os.system(command)
        print outputPath_Mosaic + '00000/', "not exist,so create!!"
    FinalHdfFile = outputPath_Mosaic + '00000/FY3C_VIRR' + dnflag + '_GBAL_L2_SST_MLT_GLL_' + date + '_POAD_' + str(
        resolution) + 'M_PD.HDF'

    # OutputFile = outputPath_Mosaic + "FY3C_Mosaic_0000_0000.HDF"
    OutputFile = outputPath_Mosaic + "FY3C_Mosaic_" + date + "_0000.HDF"

    files = os.listdir(inputPath_Mosaic)
    if len(files) == 0:
        print "Wrong!!!no mosaic HDF file !! -->", inputPath_Mosaic
        print "exit!"
        exit(0)
    inputTime = ''
    for file in files:
        if (".HDF" in file) and (date in file):
            # inputTime = file[14:18]
            inputTime = re.findall(r'\d{8}_\d{4}', file)[0]
            inputTime = inputTime.split("_")[1]
            inputFile = inputPath_Mosaic + file
            print inputFile
            print OutputFile
            print inputTime
            finalOutputFile = mosaic(inputFile, OutputFile, inputTime)
            OutputFile = finalOutputFile
    command = "mv " + OutputFile + " " + FinalHdfFile

    print command
    status = os.system(command)
    print status
    if status == 0:
        print "mosaic of VIRR Successful!!"
    # command = "rm -rf " + ouputPath_Proj  # delete Project files
    # print command
    # status = os.system(command) # delete proj (project result should not be deleted)
    # if status == 0:
    #    print "delete ", ouputPath_Proj, " "
    # <--------------end Mosaic

    # ---------------->begin add lat lon
    addLatLon(FinalHdfFile, resolution, Maxlon, MinLon, MaxLat, MinLat)
    # ---------------->end add lat lon

    # ------------>begin to make PNG
    FinalHdfFile_PNG = FinalHdfFile.replace('.HDF', '.png')
    print FinalHdfFile_PNG
    status = MosaicImage_RGB(FinalHdfFile, Maxlon, MinLon, MaxLat, MinLat)  #######################
    if status == 0:
        print "Image Success!!! "
    # <-------------end PNG

    # # ------------>begin to write into SQl
    JPGname = FinalHdfFile.replace("HDF", "png")
    command = "python /GDS/SSTWORK/ProjectTransform/fileNameToSQL.py " + JPGname + " " + FinalHdfFile + " " + dnflag
    status = os.system(command)
    if status == 0:
        print "file name write to SQL Success!!! "
    # # <-------------

    # ------------------> begin to make small range HDF file
    print len(latlon)
    for i in range(0, len(latlon)):
        if latlon[i, 0] == 0:  # the biggest range is already producted ,so skip
            print latlon[i]
            continue
        print latlon[i]
        print MaxLat, MinLon
        SmallRangeHDFfile = CreateSmallRangeFile(FinalHdfFile, MaxLat, MinLon, latlon[i], resolution)
        Maxlon_small = latlon[i][4]
        MinLon_small = latlon[i][2]
        MaxLat_small = latlon[i][1]
        MinLat_small = latlon[i][3]
        MosaicImage_RGB(SmallRangeHDFfile, Maxlon_small, MinLon_small, MaxLat_small, MinLat_small)
        addLatLon(SmallRangeHDFfile, resolution, Maxlon_small, MinLon_small, MaxLat_small, MinLat_small)
        print "SmallRangeHDFfile", SmallRangeHDFfile
    print "Create small range HDF Success!!!"
    # <-----------------

    endTime = time.time()
    print "time cost ", endTime - startTime, "s"
