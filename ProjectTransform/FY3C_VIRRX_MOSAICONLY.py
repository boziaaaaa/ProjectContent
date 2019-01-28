#-*-coding=utf-8-*-
import os
import sys
import h5py
import math
import numpy as N
def CalProjectWidthAndHeight(minU,minV,maxU,maxV,resolution):
    latlonResRate = float(0.01) / float(1000)
    res = latlonResRate*resolution
    Height = round((maxV- minV) / res+ 0.5)
    Width = round((maxU- minU) / res+ 0.5)
    return Height,Width
def GetlateLatLon(MinU, MinV, MaxU, MaxV,res):

    Height, Width = CalProjectWidthAndHeight(MinU, MinV, MaxU, MaxV,res)
    #计算经度
    longitude = N.linspace(MinU,MaxU,int(Width))
    longitude = N.tile(longitude,int(Height))
    longitude = longitude.reshape(int(Height),int(Width)).astype('f4')
    if MaxU > 180:
      longitude[longitude > 180] -= 360
      longitude[longitude < -180] += 360
    #计算纬度
    latitude = N.linspace(MaxV,MinV,Height)
    latitude = N.tile(latitude,int(Width))
    latitude = latitude.reshape(int(Width),int(Height)).astype('f4')
    latitude = latitude.T
    return longitude,latitude

def FindLocate(maxlon, minlon, maxlat, minlat,resolution):
    #resolution = 1000
    MaxLat = 90
    MinLon = -180 
    factor = 100000 / resolution
    row_up = (MaxLat - maxlat) * factor + 1
    row_down = (MaxLat - minlat) * factor + 1
    column_left = (minlon - MinLon) * factor + 1
    column_right = (maxlon - MinLon) * factor + 1
    return row_up, row_down, column_left, column_right
    
def GlobalHDF_to_AreaHDF(inputFile,outputFile,maxlon, minlon, maxlat, minlat,resolution):
    fileHandle_in = h5py.File(inputFile,"r")
    dataset = fileHandle_in["sea_surface_temperature"]
    #maxY,minX,minY,maxX = findPosition(maxLatitude,minLongitude,minLatitude,maxLongitude)
    print maxlon, minlon, maxlat, minlat
    row_up, row_down, column_left, column_right = FindLocate(maxlon, minlon, maxlat, minlat,int(resolution))
    print row_up, row_down, column_left, column_right 
    dataset_area = dataset[row_up:row_down, column_left:column_right]
    fileHandle_in.close()
    print outputFile
    findHandle_out = h5py.File(outputFile,"w")
    findHandle_out.create_dataset("sea_surface_temperature",data = dataset_area)
    Longitude,Latitude = GetlateLatLon(minlon,minlat,maxlon,maxlat,resolution)
    
    findHandle_out.create_dataset("latitude",data = Latitude)
    findHandle_out.create_dataset("longitude",data = Longitude)
    findHandle_out.close()

if __name__=="__main__":
  inputFile = sys.argv[1]
  maxlat = int(math.ceil(float(sys.argv[2])))
  minlon = int(math.ceil(float(sys.argv[3])))
  minlat = int(math.ceil(float(sys.argv[4])))
  maxlon = int(math.ceil(float(sys.argv[5])))
  resolution = 5000
  outputFile = inputFile.replace("_MS","")
  if os.path.exists(inputFile) == False:
    print "input file lost!! -->"
    print inputFile
  else:
    GlobalHDF_to_AreaHDF(inputFile,outputFile,maxlon, minlon, maxlat, minlat,resolution)
    print "get little area Sucess!!"
  