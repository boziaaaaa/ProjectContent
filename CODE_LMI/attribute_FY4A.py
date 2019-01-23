#-*-coding=utf-8-*-
import h5py
import numpy
import sys
import os
import time
import xml.etree.ElementTree as ET

class GlobalAttribute(object):
    def __init__(self):
        pass
    Satellite_Name =  "FY-4A"
    Sensor_Name = "AGRI"
    File_Name =  ""
    Projection_Type =  "LatLon（等经纬度）"
    Resolution =  "1000"
    Numbers_of_Bands = "1"
    Band_names =  "1"
    Center_Wavelength = "1"
    CenterPoint_Latitude =  1
    CenterPoint_Longitude =  "1"
    Latitude_Resolution =  "0.01"
    Longitude_Resolution =  "0.01"
    Maximum_Latitude = "1"
    Maximum_Longitude =  "1"
    Minimum_Latitude = "1"
    Minimum_Longitude =  "1"
    Standard_Latitude1 = "1"
    Standard_Latitude2 = "1"
    Orbit_Point_Latitude = "4 "
    Orbit_Point_Longitude = "4 "
    Data_Creating_Date =  ""
    Data_Creating_Time =  ""
    Data_Pixels = "1"
    Data_Lines =  "1"
    Additional_Annotation =  "None"

    def __parseXML(self,xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        for ProjInfor in root.iter('ProjInfor'):
            # format = ProjInfor.find('ProjFormat').text
            # TaskName = ProjInfor.find('ProjTaskName').text
            self.Projection_Type = ProjInfor.find('ProjMethod').text
            self.Resolution = numpy.int32(ProjInfor.find('Resolution').text)
            self.CenterPoint_Longitude = ProjInfor.find('CentralLon').text
        for projrange in root.iter('ProjRange'):
            self.Maximum_Longitude = numpy.float32(projrange.find('MaxLon').text)
            self.Minimum_Longitude = numpy.float32(projrange.find('MinLon').text)
            self.Maximum_Latitude = numpy.float32(projrange.find('MaxLat').text)
            self.Minimum_Latitude = numpy.float32(projrange.find('MinLat').text)

        for BandsToProj in root.iter('BandsToProj'):
            self.Band_names = BandsToProj.find('BandName').text
            self.Center_Wavelength = BandsToProj.find('BandWaveLength').text

    def setGlobalAttr(self,HDFfile,xmlFile):
        self.__parseXML(xmlFile)
        self.File_Name = HDFfile
        self.CenterPoint_Latitude = (self.Maximum_Latitude - self.Minimum_Latitude)/2
        # self.CenterPoint_Longitude = (self.Maximum_Longitude - self.Minimum_Longitude)/2
        self.Latitude_Resolution = self.Resolution/100000.0
        self.Longitude_Resolution = self.Resolution/100000.0

        f = h5py.File(HDFfile,"r")
        dataset = f["EVB0064"]
        self.Data_Lines = dataset.shape[0]
        self.Data_Pixels = dataset.shape[1]
        f.close()
        timeStruct = time.localtime(time.time())
        self.Data_Creating_Date = str(timeStruct.tm_year) + str(timeStruct.tm_mon).zfill(2) + str(timeStruct.tm_mday).zfill(2)
        self.Data_Creating_Time = str(timeStruct.tm_hour).zfill(2) + str(timeStruct.tm_min).zfill(2) + str(timeStruct.tm_sec).zfill(2)
        tempNames = self.Center_Wavelength.split(",")
        self.Numbers_of_Bands = len(tempNames)

class DatasetAttribute(object):
    EVB0046_attr = 	["earth view band 0046","0046",0.0,0.001,65535,"None",[0,1000]]
    EVB0064_attr = 	["earth view band 0064","0064",0.0,0.001,65535,"None",[0,1000]]
    EVB0086_attr = 	["earth view band 0086","0086",0.0,0.001,65535,"None",[0,1000]]
    EVB0137_attr = 	["earth view band 0137","0137",0.0,0.001,65535,"None",[0,1000]]
    EVB0160_attr = 	["earth view band 0160","0160",0.0,0.001,65535,"None",[0,1000]]
    EVB0230_attr = 	["earth view band 0230","0230",0.0,0.001,65535,"None",[0,1000]]
    EVB0372H_attr = ["earth view band 0372H", "0372H", 0.0, 0.01, 65535, "K", [0, 32760]]
    EVB0390_attr = ["earth view band 0390", "0390", 0.0, 0.01, 65535, "K", [0, 32760]]
    EVB0620_attr = ["earth view band 0620", "0620", 0.0, 0.01, 65535, "K", [0, 32760]]
    EVB0700_attr = ["earth view band 0700", "0700", 0.0, 0.01, 65535, "K", [0, 32760]]
    EVB0860_attr = ["earth view band 0860", "0860", 0.0, 0.01, 65535, "K", [0, 32760]]
    EVB1040_attr = ["earth view band 1040", "1040", 0.0, 0.01, 65535, "K", [0, 32760]]
    EVB1230_attr = ["earth view band 1230", "1230", 0.0, 0.01, 65535, "K", [0, 32760]]
    EVB1330_attr = ["earth view band 1330", "1330", 0.0, 0.01, 65535, "K", [0, 32760]]
    SunAzimuth_attr = ["SunAzimuth", "SunAzimuth", 0.0, 1, 65535, "K", [0, 360]]
    SunZenith_attr = ["SunAzimuth", "SunAzimuth", 0.0, 1, 65535, "K", [-90, 90]]
    def getDatasetAttr(self,bandname):
        if "0046" in bandname:
            return self.EVB0046_attr
        elif "0064" in bandname:
            return self.EVB0064_attr
        elif "0086" in bandname:
            return self.EVB0086_attr
        elif "0137" in bandname:
            return self.EVB0137_attr
        elif "0160" in bandname:
            return self.EVB0160_attr
        elif "0230" in bandname:
            return self.EVB0230_attr
        elif "0372H" in bandname:
            return self.EVB0372H_attr
        elif "0390" in bandname:
            return self.EVB0390_attr
        elif "0620" in bandname:
            return self.EVB0620_attr
        elif "0700" in bandname:
            return self.EVB0700_attr
        elif "0860" in bandname:
            return self.EVB0860_attr
        elif "1040" in bandname:
            return self.EVB1040_attr
        elif "1230" in bandname:
            return self.EVB1230_attr
        elif "1330" in bandname:
            return self.EVB1330_attr
        elif "SunAzimuth" in bandname:
            return self.SunAzimuth_attr
        elif "SunZenith" in bandname:
            return self.SunZenith_attr




#if __name__ == '__main__':
def WriteAttributes_FY4A(HDFfile, xmlFile):

    GlobalAttr = GlobalAttribute()       #全局属性
    GlobalAttr.setGlobalAttr(HDFfile,xmlFile)#设置全局属性
    Datasetattribute = DatasetAttribute()#各数据集私有属性

    f = h5py.File(HDFfile,"a")
    f.attrs.clear()#删除原有属性，重写
    f.attrs["Satellite Name"] =      GlobalAttr.Satellite_Name
    f.attrs["Sensor Name"] =         GlobalAttr.Sensor_Name
    f.attrs["File Name"] =           GlobalAttr.File_Name
    f.attrs["Projection Type"] =    GlobalAttr.Projection_Type
    f.attrs["Resolution"] =          numpy.int32(GlobalAttr.Resolution)
    f.attrs["Numbers of Bands"] =   numpy.int16(GlobalAttr.Numbers_of_Bands)
    f.attrs["Band names"] =          GlobalAttr.Band_names
    f.attrs["Center Wavelength"] =     GlobalAttr.Center_Wavelength
    f.attrs["CenterPoint Latitude"] =  numpy.float32(GlobalAttr.CenterPoint_Latitude)
    f.attrs["CenterPoint Longitude"] = numpy.float32(GlobalAttr.CenterPoint_Longitude)
    f.attrs["Latitude Resolution"] =    numpy.float32(GlobalAttr.Latitude_Resolution)
    f.attrs["Longitude Resolution"] =   numpy.float32(GlobalAttr.Longitude_Resolution)
    f.attrs["Maximum Latitude"] =   numpy.float32(GlobalAttr.Maximum_Latitude)
    f.attrs["Maximum Longitude"] =  numpy.float32(GlobalAttr.Maximum_Longitude)
    f.attrs["Minimum Latitude"] =   numpy.float32(GlobalAttr.Minimum_Latitude)
    f.attrs["Minimum Longitude"] =  numpy.float32(GlobalAttr.Minimum_Longitude)
    # if "at" in GlobalAttr.Projection_Type and "on" in GlobalAttr.Projection_Type: # latlon / LatLon
    f.attrs["Standard Latitude 1"] = "None"
    f.attrs["Standard Latitude 2"] = "None"
    f.attrs["Orbit Point Latitude"] = "None"
    f.attrs["Orbit Point Longitude"] = "None"
    # else:
    #     f.attrs["Standard Latitude 1"] = numpy.float32(GlobalAttr.Standard_Latitude1)
    #     f.attrs["Standard Latitude 2"] = numpy.float32(GlobalAttr.Standard_Latitude2)
    #     f.attrs["Orbit Point Latitude"] = numpy.float32(GlobalAttr.Orbit_Point_Latitude)
    #     f.attrs["Orbit Point Longitude"] = numpy.float32(GlobalAttr.Orbit_Point_Longitude)

    f.attrs["Data Creating Date"] = GlobalAttr.Data_Creating_Date
    f.attrs["Data Creating Time"] = GlobalAttr.Data_Creating_Time
    f.attrs["Data Pixels"] = GlobalAttr.Data_Pixels
    f.attrs["Data Lines"] = GlobalAttr.Data_Lines
    f.attrs["Additional Annotation"] = GlobalAttr.Additional_Annotation
    bandlist = f.keys()
    for k in bandlist:
        dataset = f[k]
        dataset.attrs.clear() #删除原有属性，重写
        dataset.attrs["long_name"] = Datasetattribute.getDatasetAttr(k)[0]
        dataset.attrs["band_name"] = Datasetattribute.getDatasetAttr(k)[1]
        dataset.attrs["Intercept"] = numpy.float32(Datasetattribute.getDatasetAttr(k)[2])
        dataset.attrs["Slope"] = numpy.float32(Datasetattribute.getDatasetAttr(k)[3])
        dataset.attrs["FillValue"] = numpy.int(Datasetattribute.getDatasetAttr(k)[4])
        dataset.attrs["units"] = Datasetattribute.getDatasetAttr(k)[5]
        dataset.attrs["valid_range"] = Datasetattribute.getDatasetAttr(k)[6]
    f.close()
    print "-------"