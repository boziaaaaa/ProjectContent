# -*- coding: utf-8 -*-
from DataProvider import *
import h5py
import time
import math as Math
import numpy as N
from netCDF4 import Dataset
import numpy.ctypeslib as npct
from ctypes import c_int
from ctypes import c_float
import os

class MSGProvider(DataProvider):

    def __init__(self):
        super(MSGProvider,self).__init__()
        self.__AuxiliaryDataNamesList =dict()
        self.__HdfFileHandleList =dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        #self.__BandWaveLenthList = None # temporary changed as below
        self.__BandWaveLenthList = ['0060','1100','1200','0700','0380']

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataWidthAndHeight = 0
        self.__ZenithStartLine = 0
        self.__ZenithEndLine = 0
        self.SolarZenith = None
        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList=None

        self.__HdfFileHandleList.clear()
        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(MSGProvider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'MSG2'
        self.OrbitInfo.Sensor = 'SEVI'
        self.OrbitInfo.OrbitDirection= ''

        self.OrbitInfo.Width = self.__dataWidth
        self.OrbitInfo.Height = self.__dataHeight

        #solarzenith = self.GetSolarZenith()
        # if solarzenith[int(self.__dataWidthAndHeight/2),int(self.__dataWidthAndHeight/2)] <=85:
        #     self.OrbitInfo.DNFlag = 'D'
        # else:
        #     self.OrbitInfo.DNFlag = 'N'

        self.OrbitInfo.Date = ''
        self.OrbitInfo.Time = ''
        #self.OrbitInfo.Date=self.GetDate()
        #self.OrbitInfo.Time=self.GetTime()
        #self.SolarZenith = self.GetSolarZenith()
    def GetFullScanTime(self):
        #nc_fid = Dataset(self.__HdfFileHandleList['L1'], 'r')
        nc_fid = None
        if self.__HdfFileHandleList.has_key('L1'):# condition when process Channel band data
            nc_fid = Dataset(self.__HdfFileHandleList['L1'], 'r')
        elif self.__HdfFileHandleList.has_key('SolarZenith'):#condition when process Auxiliary data(SolarZenith)
            nc_fid = Dataset(self.__HdfFileHandleList['SolarZenith'], 'r')
        g_attdict = nc_fid.__dict__
        for k, v in g_attdict.iteritems():
            if k == 'fullScanTime':
                Length = len(v)
                FullScanTime = v[0:Length - 8]
                FullScanTime = float(FullScanTime)
        nc_fid.close()
      	return FullScanTime
    def GetDaysOfYear(self):
        Year,Month,Day,Hour,Minute,Second = self.GetTime()
        now_time = time.gmtime(time.mktime((Year,Month,Day,Hour,Minute,Second, 0, 0, 0)))
        DaysOfYear = now_time.tm_yday
        return DaysOfYear
    def GetTime(self):
        #nc_fid = Dataset(self.__HdfFileHandleList['L1'], 'r')
        nc_fid = None
        if self.__HdfFileHandleList.has_key('L1'):# a condition when Channel band data is processed
            nc_fid = Dataset(self.__HdfFileHandleList['L1'], 'r')
        elif self.__HdfFileHandleList.has_key('SolarZenith'):# condition when process Auxiliary data(SolarZenith)
            nc_fid = Dataset(self.__HdfFileHandleList['SolarZenith'], 'r')

        g_attdict = nc_fid.__dict__
        for k, v in g_attdict.iteritems():
            if k == 'time_coverage_start':
                v = str(v)
                Year = v[0:4]
                Year = int(Year)
                Month = v[5:7]
                Month = int(Month)
                Day = v[8:10]
                Day = int(Day)
                Hour = v[11:13]
                Hour = int(Hour)
                Minute = v[14:16]
                Minute = int(Minute)
                Second = v[17:19]
                Second = int(Second)
      	return Year,Month,Day,Hour,Minute,Second

    def OnParametersUpdate(self):
        super(MSGProvider, self).OnParametersUpdate()
        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList
        self.__obsDataCount =len(self.__BandWaveLenthList)
        self.CreateBandsInfo()
        return

    def SetLonLatFile(self,latfile,lonfile):
        self.__HdfFileHandleList['Latitude'] = latfile
        self.__HdfFileHandleList['Longitude'] = lonfile

    def SetL1File(self, file):
        self.__HdfFileHandleList['L1'] = file
        self.__dataRes = 5000
        #self.__dataWidthAndHeight = 3712  
        self.__dataWidth = 3712
        self.__dataHeight = 3712
        self.__InitOrbitInfo()       

    def SetAuxiliaryDataFile(self, AuxiliaryNameDict, AuxiliaryDataDict):
      	for key in AuxiliaryDataDict:
            #self.__HdfFileHandleList[key] = self.__HdfOperator.Open(AuxiliaryDataDict[key])
            self.__HdfFileHandleList[key] = AuxiliaryDataDict[key]
            self.__AuxiliaryDataNamesList[key] = AuxiliaryNameDict[key]
        return

    def CreateBandsInfo(self):
        index  = 1
        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB'+str(wavelength)] = wavelength
            #print("////////////////////////////////////")
            #print(self.OrbitInfo.BandsWavelength['EVB'+str(wavelength)])

            if int(wavelength)>230:
                self.OrbitInfo.BandsType['EVB'+str(wavelength)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB'+str(wavelength)] = 'REF'
            index = index+1

    def GetLongitude(self):        
        Lons = self.GetDataSet(self.__HdfFileHandleList['Longitude'], 'lon')

        # because lat/lon range is bigger than Ref/Emiss(channel) data range,
        #        so mask lat/lon data range by channel data range
        ch6 = self.GetDataSet(self.__HdfFileHandleList['Longitude'], 'ch6')
        #Mask = N.where(ch6 == 0)
        #Lons[Mask] = Lons[1,1]
        # file = h5py.File("/home/bozi/Downloads/TestData/MSG_Lons.HDF")
        # file.create_dataset("Lons_before",data = Lons)

        # use ch6(valid value) to be a mask, ch6[0,0] is filled value
        #the range of fill value of channel6 is used to be the range of fill value of lat/lon data
        Lons[ch6 == ch6[0,0]] = Lons[1, 1]

        # file.create_dataset("Lons_after",data = Lons)
        # file.close()
        return Lons

    def GetLatitude(self):
        Lats = self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'lat')

        ch6 = self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'ch6')
        # Mask = N.where(ch6 == 0)
        # Lats[Mask] = Lats[1,1]
        Lats[ch6 == ch6[0,0]] = Lats[1, 1]

        return Lats

    def GetResolution(self):
        return self.__dataRes

    def GetSolarZenith(self):
        Lats = self.GetLatitude()#.reshape[self.__dataWidth*self.__dataHeight]
        Lons = self.GetLongitude()#.reshape[self.__dataWidth*self.__dataHeight]
        Lats_Width,Lats_Height = Lats.shape
        Lats = N.array(Lats).reshape(Lats_Width * Lats_Height)
        Lons = N.array(Lons).reshape(Lats_Width * Lats_Height)
        SolarZenithData = [0]*(Lats_Width*Lats_Height)

        array_1d_double = npct.ndpointer(dtype=N.double, ndim=1, flags='CONTIGUOUS')
        execpath = os.path.dirname(os.path.realpath(__file__))
        StringLength = len(execpath)
        #print(StringLength)
        #print(execpath)
        SOPath = execpath[0:StringLength-13]
        #print(SOPath)
        libcd = npct.load_library(SOPath + "/SUNAziElv", ".")

        libcd.GetSunAziElvCPP.restype = c_int
        libcd.GetSunAziElvCPP.argtypes=[c_int, c_int, c_int, c_int, c_int, c_int, array_1d_double, array_1d_double, array_1d_double,array_1d_double, c_int, c_int,c_float]

        Azimuth_temp = [0.0]*(Lats_Width * Lats_Height)
        Azimuth_temp = N.array(Azimuth_temp)
        Zenith_temp = [0.0] * (Lats_Width * Lats_Height)
        Zenith_temp = N.array(Zenith_temp)
        Year,Month,Day,Hour,Minute,Second = self.GetTime()
        FullScanTime = self.GetFullScanTime()
        Lats = Lats.astype(N.float64)
        Lons = Lons.astype(N.float64)
        #print(Lats)
        #print(Lats.shape)
        #print(Lons)
        #print(Lons.shape)
        libcd.GetSunAziElvCPP(Year, Month, Day, Hour, Minute, Second, Lats, Lons, Azimuth_temp, Zenith_temp,Lats_Width,Lats_Height,FullScanTime)
        SolarZenithData = Zenith_temp

        SolarZenithData = N.array(SolarZenithData).reshape(Lats_Width,Lats_Height)
        return SolarZenithData


    def GetOBSData(self, band):    
        ret = None        
        #if band!='':
         #   bandname= band.replace("EVB", "ch")
        #     ret = self.GetDataSet(self.__HdfFileHandleList['L1'], bandname)

        if band == 'EVB0060':
            ret=self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch1')
        elif band == 'EVB0080':
            ret = self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch2')
        elif band == 'EVB0160':
            ret=self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch3')
        #elif band == 'EVB0390': # changed according to FY2E,2017_2_9
        elif band == 'EVB0380':
            ret = self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch4')
        elif band == 'EVB0620':
            ret=self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch5')
        #elif band == 'EVB0730': # changed according to FY2E,2017_2_9
        elif band == 'EVB0700':
            ret = self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch6')
        elif band == 'EVB0870':
            ret=self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch7')
        elif band == 'EVB0970':
            ret = self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch8')
        #elif band == 'EVB1080': # changed according to FY2E,2017_2_9
        elif band == 'EVB1100':
            ret=self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch9')
        elif band == 'EVB1200':
            ret = self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch10')
        elif band == 'EVB1340':
            ret = self.GetDataSet(self.__HdfFileHandleList['L1'], 'ch11')
        if self.OrbitInfo.BandsType[band] == 'REF':

            self.SolarZenith = self.GetSolarZenith()#.reshape(self.__dataWidth,self.__dataHeight)
            #print(self.SolarZenith.shape)

            #########################
            # file = h5py.File('/home/bozi/Downloads/TestData/MSGSolarZenith20100101_1145.HDF.h5', 'w')
            # file.create_dataset('NOMSunZenith', data=self.SolarZenith)
            # file.close

            Pi = 3.1415926
            #SunEarthDis = 1

            DaysOfYear = self.GetDaysOfYear()
            SunEarthDis = 1+0.0167*Math.sin(2*Pi*(DaysOfYear-93.5)/360)
            #print("=-=-=-=-=-=-=-==================")
            #print(SunEarthDis)
            #ESUN = 1367.0 
            if band == 'EVB0060':
              ESUN = 1840.0              
            elif band == 'EVB0080':
              ESUN = 1044.0              
            elif band == 'EVB0160':
              ESUN = 225.70

            BandLength = self.OrbitInfo.BandsWavelength[band]
            BandLength_um = float(BandLength)/100 ###change to um
            BandLength_cm = float(BandLength_um)/10000
            ret = ret/(BandLength_cm**2)* (10**(-7))##
            #ret = Radiance * (10**(-7)) / BandLength_cm / BandLength_cm  ####################cm-1 change to um
            #ret = ret * 10/BandLength/BandLength ####################cm-1 change to um
            cos_SolarZenith = N.cos(self.SolarZenith[:, :]) #self.SolarZenith is radian
            Mask_cos = N.where(self.SolarZenith >=90)
            ret_NotCaculate = ret[Mask_cos]

            #cos_SolarZenith[Mask_cos] = 0
            # file = h5py.File('/home/bozi/Downloads/TestData/'+bandname+'.HDF.h5', 'w')
            # temppp = self.SolarZenith*180/Pi
            # file.create_dataset('SolarZenith'+bandname, data=temppp)

            REF_Mask0 = N.where(ret<=0)
            # data will multiply 1000 behind,and 65.335 become 65535,this is the fill value of finnal output data
            ret[REF_Mask0] = 65.535

            ret = Pi*SunEarthDis*SunEarthDis*ret/(ESUN*cos_SolarZenith) #���������۷�����
            # file.create_dataset('Ref11_' + bandname, data=ret)
            Lats_temp = self.GetLatitude()
            #lt = Lats_temp <-90
            #lt|= Lats_temp >90
            ret[Mask_cos] = ret_NotCaculate
            #REF_Mask1 = N.where(Lats_temp<=-90)
            #REF_Mask2 = N.where(Lats_temp >= 90)
            REF_Mask_TooGig = N.where(ret > 1)
            REF_Mask_TooSmall = N.where(ret <= 0)
            ret[REF_Mask_TooSmall] = 65.535
            #ret[Mask_cos] = ret_NotCaculate
            ret[REF_Mask_TooGig] = 65.535
            #ret[REF_Mask1] = 65535
            #ret[REF_Mask2] = 65535
            #ret[lt] = 65535
            # file.create_dataset('Ref22_' + bandname, data=ret)
            # file.close()
            ret = 1000 * ret
            #print("--=======================-------")
            #print(type(ret))
        else:
            h = 6.62606876e-34 # Planck constant(Joule second)
            c = 2.99792458e+8 # Speed of light in vacuum(meters per second)
            k = 1.3806503e-23 # Boltzmann constant(Joules per
            BandLength = self.OrbitInfo.BandsWavelength[band]
            BandLength_um = float(BandLength)/100 # convert to um
            #print(BandLength_um)
            BandLength_cm = BandLength_um/10000 # convert to cm
            r = ret
            EMIS_Mask = N.where(ret <= 0)
            r[EMIS_Mask] = 1
            BandLength_m = BandLength_um/1000000  # convert to meter
            C1 = 2*h*c*c
            C2 = (h*c)/k
            vs = 1/BandLength_m #Wavenumber inverse meters
            ret =  C2 * vs / N.log(C1 * (vs**3) / (1.0e-5 * r) + 1.0);

            #EMIS_Mask = N.where(ret <= 0)
            #ret[EMIS_Mask] = 65535
            ret[EMIS_Mask] = 655.35 #2017_2_9 65535 changed to 655.35 otherwise the fillvalue will be 6553500
            ret = 100 * ret
        ret = ret.astype(N.int32)

        #################
        #print("OBS   <><><><<><")
        #print ret

        return ret
 
    def GetOBSDataCount(self):
        return self.__obsDataCount

    def GetDataSet(self,filehandle,ds):
        #nc_fid = Dataset(self.__HdfFileHandleList['L1'], 'r')
        nc_fid = Dataset(filehandle, 'r')
        data = nc_fid.variables[ds][:]
        '''
        g_attdict = nc_fid.__dict__
        for k, v in g_attdict.iteritems():
            if k == 'fullScanTime':
                Length = len(v)
                FullScanTime = v[0:Length-8]
                FullScanTime = float(FullScanTime)
                print(type(FullScanTime))

                print(FullScanTime)
            if k == 'time_coverage_start':
                v = str(v)
                Year = v[0:4]
                Year = int(Year)
                Month = v[5:7]
                Month = int(Month)
                Day = v[8:10]
                Day = int(Day)
                Hour = v[11:13]
                Hour = int(Hour)
                Minute = v[14:16]
                Minute = int(Minute)
                Second = v[17:19]
                Second = int(Second)
                print Year,Month,Day,Hour,Minute,Second
        '''

        data = N.array(data)  # convert to numpy array,otherwise fillvalue not be correct read
        nc_fid.close()
        data = data.astype('float32')

        startLine = self.startLine
        endlLine = self.endLine
        self.__ZenithStartLine = self.startLine
        self.__ZenithEndLine = self.endLine
        ret = None
        if startLine!= -1 & endlLine!= -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:,:]  
       
        return ret

    def GetAuxiliaryData(self,dataname):
        dsname = self.__AuxiliaryDataNamesList[dataname]

        #################
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print dsname

        ret = None
        if dsname =='':
            return  ret

        if dsname == "SolarZenith":
            print("get in elseeeeeeeeeeeeeeeeeeeeeeeeee")
            ret = self.GetSolarZenith()
            print(ret)
        else:
            ret=self.GetDataSet(self.__HdfFileHandleList[dataname], dsname)


        return ret

    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList

    def SetDataDescription(self, value):
        self.__description = value

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription()+'_'+str(self.GetParameter().ProjectResolution)
        return  self.__description


   
