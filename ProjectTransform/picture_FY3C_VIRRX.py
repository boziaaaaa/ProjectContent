#-*-coding=UTF-8-*-
import h5py
import sys
import numpy as N
import os
import glob
import time
from PIL import Image
from InsertDB import InsertDB
from picture_Base import Trans

def MosaicImage_RGB(InputFilePath,outputJPG):
    startLat = float(sys.argv[3])
    startLon = float(sys.argv[4])
    endLat   = float(sys.argv[5])
    endLon   = float(sys.argv[6])
    areaid   = int(sys.argv[7])

    print startLat ,startLon ,endLat ,endLon
    #定义类
    database = InsertDB()
    #计算区域起始行、列号
    sLat,sLon,eLat,eLon = database.get_Lat_Lon_Extend(areaid = areaid)
    database.closeall()
    if sLat < startLat :
        print "The Latitude error, fallen outside! The region top Latitude is ",sLat,", but input is ",startLat
        return

    if startLon < sLon :
        print "The Longitude error, fallen outside! The region left Longitude is ",sLon,", but input is ",startLon
        return

    if sLat < endLat :
        print "The Latitude error, fallen outside! The region right Latitude is ",sLat,", but input is ",endLat
        return

    if endLon < sLon :
        print "The Longitude error, fallen outside! The region low Longitude is ",sLon,", but input is ",endLon
        return

    beginLine = N.int((sLat - startLat) / 0.05)
    beginColumn = N.int((startLon - sLon) / 0.05)
    endLine = N.int((sLat - endLat) / 0.05)
    endColumn = N.int((endLon - sLon) / 0.05)

    print "beginLine,beginColumn,endLine,endColumn",beginLine,beginColumn,endLine,endColumn

    print InputFilePath
    if not os.path.isfile(InputFilePath):
        print InputFilePath ,' not exsit!'
        return
    hdf_in = h5py.File(InputFilePath)
    BandData1 = hdf_in['sea_surface_temperature'].value[:, :]
    BandData=BandData1[beginLine:endLine,beginColumn:endColumn]
    mask_t = N.where(BandData>-800)
    BandData[mask_t] = BandData[mask_t]/100
    #picture_SSTtt = picture_SST()
    r,g,b=Trans(BandData) # bb bigger Image Redder

    f=150 #fill value 150 is useless
    Height,Width = BandData.shape
    rgbArray = N.zeros(( Height,Width, 4), 'uint8')
    rgbArray[..., 0] = r
    rgbArray[..., 1] = g
    rgbArray[..., 2] = b
    rgbArray[..., 3] = ((r!=f) | (g!=f) | (b!=f)).astype('u1')*255
    OutputImg = Image.fromarray(rgbArray,mode="RGBA")
    print OutputImg
    print rgbArray[...,3]
    JPGname = outputJPG
    OutputImg.save(JPGname)

    return 0


if __name__ == '__main__':
    startTime = time.time()

    #--------->����������
    inputHDF = sys.argv[1]
    outputJPG = sys.argv[2]
    #<---------
    
    #------------>��ƴ�Ӻ��HDF�������ɫͼƬ
    #FinalHdfFile = outputPath_Mosaic+"FY3C_VIRR_MOSAIC_"+date+"_PD.HDF"
    status = MosaicImage_RGB(inputHDF,outputJPG)
    if status == 0:
      print "Image " + outputJPG +" Success!!! "
    #<-------------
    
    #------------>ƴ�Ӻ�HDF�ļ����ƺ�JPG�ļ��������
    #JPGname = FinalHdfFile.replace("HDF","jpg")
    #command = "python /gds/Run/ProjectTransform/fileNameToSQL.py "+JPGname+" "+FinalHdfFile
    #status = os.system(command)
    #if status == 0:
    #  print "file name write to SQL Success!!! "
    #<-------------
    
    endTime = time.time()
    print "time cost ",endTime - startTime,"s"
