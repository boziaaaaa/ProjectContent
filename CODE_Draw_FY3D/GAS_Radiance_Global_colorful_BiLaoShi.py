# coding=utf-8
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
import matplotlib.pyplot as plt
import h5py
import numpy
import time
import os
# from matplotlib.ticker import FormatStrFormatter


class GAS_position(object):
    # def GlobalPosition(self,lat,lon,radiance,date,mode):
    def GlobalPosition(self, data,Time,outputFile):
        lat = data.latitude
        lon = data.longitude
        radiance = data.radiance
        date = Time #文件时间
        mode = data.mode #观测模式
        frame = 0 #帧数

        #plt.figure(3,figsize=(30,10))  ###############################################
        plt.figure(3,figsize=(15,5))

        #plt.title("Radiance"+"  GAS "+date,fontsize=17)
        plt.title("GAS Global Measurements(770nm) 2017.12.05",fontsize=15)

        plt.text(205,-100,"$W/cm^2/sr/cm^{-1}$",fontsize=10)
        m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')
        #m.bluemarble(scale=1)
        #m.bluemarble(color = "gray")
        m.drawcoastlines(color="gray")

        #m.fillcontinents(color='#CCCCCC', lake_color='#CCCCCC')  # ,alpha=0.0        print a
        #m.drawstates(color="r")          #国家界限
        #m.drawmapboundary(color="white") #去除边框
        #m.drawlsmask()                      #陆地范围 默认灰色
        #m.drawrivers()

        x, y = m(lon, lat)
        radiance = numpy.array(radiance)
        color = radiance
        #mm=m.scatter(x, y, c=color,s=0.35,cmap=cm.jet)#,vmin=0,vmax=10)
        mm=m.scatter(x, y, c=color,s=0.5,cmap=cm.jet)#,vmin=0,vmax=10)

        cb=plt.colorbar(mm,format="%.3e") #colorbar标注改为科学计数法
        #cb=plt.colorbar(mm,format="%.3e",orientation='horizontal', shrink=0.45) #colorbar数值改为科学计数法


        plt.savefig(outputFile,dpi = 350)
        outputFile = outputFile.replace(".pdf",".eps")
        plt.savefig(outputFile,dpi = 350)
        outputFile = outputFile.replace(".eps",".png")
        plt.savefig(outputFile,dpi = 350)

        plt.show()
        plt.close()

class Data(object): #结构体 需要绘图的数据
    latitude = []
    longitude = []
    radiance = []
    mode = []
if __name__=="__main__":

    #Time = "20171206"
    Time = "20171205"

    Time = str(Time)
    inputPath = "D:/temp_10.24.171.20/"
    outputPath = "D:/Data_GAS/picture/"
    outputFile = outputPath + Time + "_color.pdf"
    files = os.listdir(inputPath)

    data = Data()
    index = 0

    for f in files:
        #if (date in f) and ("SC" not in f) and ("DC" not in f) and ("GL" not in f):
        #if (date in f) and ("SC" not in f) and ("DC" not in f) and ("ND" not in f):
        if (Time in f) and ("SC" not in f) and ("DC" not in f) and ("1B" in f) and (".HDF" in f):

        #if (date in f) and ("SC" not in f) and ("DC" not in fGAS_position.py):
            # acc = os.access(f,os.R_OK)
            # print acc
            print f
            L1b = inputPath+f
            fileHandle = h5py.File(L1b, 'r')
            #print fileHandle.keys()
            try:
                DataNames = fileHandle["Data"].keys()
            except:
                print "Data is empty",f
                continue
            #print DataNames
            if "Radiance_B1" not in DataNames:
                print "Radiance_B1 lost",f
                continue
            lon = fileHandle['Geolocation/CenterLon'].value
            lat = fileHandle['Geolocation/CenterLat'].value
            radiance = fileHandle['Data/Radiance_B1'].value
            radiance = numpy.transpose(radiance)
            radiance = radiance[0]

            attr = fileHandle['Data/Radiance_B2'].attrs  #Radiance_B2 validRange = Radiance_B1 validRange
            minValue = attr["valid_range"][0]
            maxValue = attr["valid_range"][1]
            #print minValue,maxValue  #print radiance
            #mask = (radiance > minValue)  & (radiance < maxValue)
            radiance[radiance < minValue] = minValue
            radiance[radiance > maxValue] = maxValue
            if (Time in f) and ("SC" not in f) and ("DC" not in f) :
                radiance[radiance > 0.000002] = 0.000002
            data.longitude.extend(lon)
            data.latitude.extend(lat)
            data.radiance.extend(radiance)
            for i in range(0,len(lat)):
              data.mode.append(str(f[8:10]))
            index = index +1

    print "=-=-Files Number=-=", index
    GAS_position = GAS_position()

    GAS_position.GlobalPosition(data,Time,outputFile) # 纬度数组 经度数组 辐射亮度 时间 观测模式数组
