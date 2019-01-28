#-*-coding=UTF-8-*-
import h5py
import sys
import numpy as N
import os
import glob
import time
import struct
from PIL import Image
from InsertDB import InsertDB

def getRowColumn(MaxLon,MinLon,MaxLat,MinLat) :
    rows = 21600    #fixed row value of .dat
    columns = 43200 #fixed column value of .dat
    column_right = (MaxLon - (-180))/360.0*columns
    row_up = (90 - MaxLat)/180.0*rows
    column_left = (MinLon - (-180))/360.0*columns
    row_down = (90 - MinLat)/180.0*rows
    return int(row_up),int(row_down),int(column_left),int(column_right)

def getLandSeaMask(MaxLon,MinLon,MaxLat,MinLat,height,width):
    row_up, row_down, column_left, column_right = getRowColumn(MaxLon, MinLon, MaxLat, MinLat)
    print row_up - row_down, column_left - column_right
    print row_up, row_down, column_left, column_right

    LandSea = []
    file = "/GDS/SSTWORK/ProjectTransform/PARAM/LAND_SGI.new" # land sea mask file
    arsc_file = open(file, "rb")
    rows = 21600
    columns = 43200
    skip_num = (row_up - 1) * columns + (column_left - 1)
    arsc_file.seek(skip_num, 0)
    for i in range(0, row_down - row_up + 1):
        data = arsc_file.read(column_right - column_left + 1)
        temp = struct.unpack("%dB" % (column_right - column_left + 1), data)
        LandSea.append(temp)
        skip_num = columns - column_right + column_left - 1
        arsc_file.seek(skip_num, 1)

    LandSea = N.array(LandSea)
    img = Image.fromarray(N.uint8(LandSea))
    img = img.resize((width, height))  # width , height
    result = N.zeros((height, width))
    print width, height
    for h in range(0, height):
        for w in range(0, width):
            pixel = img.getpixel((w, h))
            result[h, w] = pixel
    return result

def Trans(inputArray,MaxLon,MinLon,MaxLat,MinLat):
      print inputArray.shape
      if MaxLon==0 and MinLon==0 and MaxLat==0 and MinLat==0: # means do not need LandSeaMask
          pass
      else:
          print "did i come here"
          height,width = inputArray.shape
          LandSeaMask = getLandSeaMask(MaxLon,MinLon,MaxLat,MinLat,height,width)
          inputArray[LandSeaMask == 1] = -999 # LandSeaMask ：land == 1


      inputArray = N.array(inputArray)
      inputArray[inputArray>-888] =  inputArray[inputArray>-888]/10.0


      r = N.zeros(inputArray.shape)
      g = N.zeros(inputArray.shape)
      b = N.zeros(inputArray.shape)

      colorbar = N.loadtxt("/GDS/SSTWORK/ProjectTransform/PARAM/colorbar_sst.txt")

      # a = min(colorbar[:,0:2].any())
      # minSST = a.any()
      # a = max(colorbar[:, 0:2])
      # maxSST = a.any()
      # print minSST,maxSST
      # print "   KKKKKKKKKKKKKKKKKK"
      inputArray[inputArray < -1000] = -1000
      inputArray[inputArray >= 350] = 350

      for line in colorbar:
          minValue = line[0]
          maxValue = line[1]
          mask = inputArray >= minValue
          mask &= inputArray < maxValue
          r[mask] = line[2]
          g[mask] = line[3]
          b[mask] = line[4]
      return r,g,b

#                                 MaxLon,MinLon,MaxLat,MinLat --> passed to Trans()
def MosaicImage_RGB(InputFilePath,MaxLon=0,MinLon=0,MaxLat=0,MinLat=0):
    hdf_in = h5py.File(InputFilePath)
    BandData = hdf_in['sea_surface_temperature'].value[:, :]

    r, g, b = Trans(BandData,MaxLon,MinLon,MaxLat,MinLat)  # bb bigger Image Redder
    Height, Width = BandData.shape
    f = 0
    rgbArray = N.zeros((Height, Width, 4), 'uint8')
    rgbArray[..., 0] = r
    rgbArray[..., 1] = g
    rgbArray[..., 2] = b
    rgbArray[..., 3] = ((r!=f) | (g!=f) | (b!=f)).astype('u1')*255
    OutputImg = Image.fromarray(rgbArray,mode="RGBA")
    JPGname = InputFilePath.replace('.HDF', '.png')
    OutputImg.save(JPGname)
    hdf_in.close()
    return 0

