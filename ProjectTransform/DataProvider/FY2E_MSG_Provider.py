from DataProvider import *
from HdfOperator import *
from FY2EProvider import *
from MSGProvider import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD
import h5py


class FY2E_MSG_Provider(DataProvider):
    def __init__(self):
        super(FY2E_MSG_Provider, self).__init__()
        self.__AuxiliaryDataNamesList = dict()
        self.__HdfFileHandleList = dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        self.__BandWaveLenthList = None # temporary changed as below
        #self.__BandWaveLenthList = ['0060', '1100', '1200', '0700', '0380']
        self.__HdfOperator = HdfOperator()
        self.__FY2EProvider = FY2EProvider()
        #self.__FY2EProvider.__init__()
        self.__MSGProvider = MSGProvider()
        #self.__MSGProvider.__init__()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataWidthAndHeight = 0

        self.__minLonFY2E = 0
        self.__maxLonMSG = 0
        self.__FY2ESubarrayIndex = 0
        self.__MSGSubarrayIndex = 0
        return

    def Dispose(self):
        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(FY2E_MSG_Provider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = ''
        self.OrbitInfo.Sensor = ''
        self.OrbitInfo.OrbitDirection = ''

        self.OrbitInfo.Width = self.__dataWidthAndHeight
        self.OrbitInfo.Height = self.__dataWidthAndHeight

        self.OrbitInfo.Date = self.GetDate()
        self.OrbitInfo.Time = self.GetTime()

    def GetDate(self):

        return

    def GetTime(self):

        return

    def OnParametersUpdate(self):
        super(FY2E_MSG_Provider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList
        self.__FY2EProvider.__obsDataCount = 5#len(self.__FY2EProvider.__BandWaveLenthLis)
        self.__MSGProvider.__obsDataCount = 5#len(self.__MSGProvider.__BandWaveLenthList)
        self.__FY2EProvider.CreateBandsInfo()
        self.__MSGProvider.CreateBandsInfo()
        self.CreateBandsInfo()
        self.CaculateSubarrayIndex()
        #self.__FY2EProvider.OnParametersUpdate()
        #self.__MSGProvider.OnParametersUpdate()
        return

    #@staticmethod
    def SetFile(self,latfileFY2E, lonfileFY2E,fileFY2E, latfileMSG, lonfileMSG,fileMSG):
        self.__FY2EProvider.SetLonLatFile(latfileFY2E, lonfileFY2E)
        self.__MSGProvider.SetLonLatFile(latfileMSG, lonfileMSG)
        self.__FY2EProvider.SetL1File(fileFY2E)
        self.__MSGProvider.SetL1File(fileMSG)
        self.__InitOrbitInfo()
        return

    def SetLonLatFile(self,latfileFY2E, lonfileFY2E, latfileMSG, lonfileMSG):#used only by Auxiliary data process
        self.__FY2EProvider.SetLonLatFile(latfileFY2E, lonfileFY2E)
        self.__MSGProvider.SetLonLatFile(latfileMSG, lonfileMSG)

    #def SetAuxiliaryDataFile(self, AuxiliaryNameDict, AuxiliaryDataDict):
    def SetAuxiliaryDataFile(self, AuxiliaryNameDict_FY2E, AuxiliaryDataDict_FY2E, AuxiliaryNameDict_MSG,AuxiliaryDataDict_MSG):
        self.__FY2EProvider.SetAuxiliaryDataFile(AuxiliaryNameDict_FY2E, AuxiliaryDataDict_FY2E)
        self.__MSGProvider.SetAuxiliaryDataFile(AuxiliaryNameDict_MSG,AuxiliaryDataDict_MSG)
        for key in AuxiliaryNameDict_FY2E:
            self.__AuxiliaryDataNamesList[key] = AuxiliaryNameDict_FY2E[key]
        return

    def CreateBandsInfo(self):
        # index  = 1
        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB' + str(wavelength)] = wavelength
            if int(wavelength) > 230:
                self.OrbitInfo.BandsType['EVB' + str(wavelength)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB' + str(wavelength)] = 'REF'
                # index = index+1

    def GetLongitude(self):
        print("----->Begin GetLongitude")
        FY2ELonData = self.__FY2EProvider.GetLongitude()

        FY2ELonData[self.__FY2ESubarrayIndex] = FY2ELonData[0,0]

        MSGLonData = self.__MSGProvider.GetLongitude()
        #MSGLonData = MSGLonData[:,:self.__MSGSubarrayIndex]
        MSGLonData[self.__MSGSubarrayIndex] = MSGLonData[0,0]

        #self.__minLonFY2E = N.min(FY2ELonData)
        #self.__maxLonMSG = N.max(MSGLonData)
        RowNumFY2E,ColumnNumFY2E = FY2ELonData.shape #RowNum is not equal to ColumnNum
        RowNumMSG, ColumnNumMSG = MSGLonData.shape #RowNum is not equal to ColumnNum

        #zoomRate = 5000/1250
        #MSGLonData_Interp = SD.BilinearInterPolateData(int(RowNumMSG), int(ColumnNumMSG), int(zoomRate), MSGLonData)
        #RowNumMSG_Interp, ColumnNumMSG_Interp = MSGLonData_Interp.shape
        LonMasaic = N.tile(MSGLonData,2) # to define a big array to store masaicked data

        LonMasaic[:,ColumnNumMSG:] = LonMasaic[0,0] #left half side is MSG data,set right half side of the big array as filled vaule of MSG
        RowStart = (RowNumMSG - RowNumFY2E)/2 
        RowEnd = RowNumMSG - (RowNumMSG - RowNumFY2E) / 2
        #ColumnStart = (ColumnNumMSG - ColumnNumFY2E)/2 + ColumnNumMSG
        #ColumnEnd = ColumnNumMSG - (ColumnNumMSG - ColumnNumFY2E) / 2 + ColumnNumMSG
        ColumnStart = ColumnNumMSG
        ColumnEnd = ColumnNumFY2E + ColumnNumMSG
        FillValuePosition = N.where(FY2ELonData == FY2ELonData[0,0])
        #FY2ELonData[FillValuePosition] = 65535
        FY2ELonData[FillValuePosition] = MSGLonData[0,0]
        LonMasaic[RowStart:RowEnd, ColumnStart:ColumnEnd] = FY2ELonData #add FY2E data to the big mosaicked array

        print("----->End GetLongitude")
        return LonMasaic

    def CaculateSubarrayIndex(self):
        # FY2E and MSG data are repeated at conjunct boundary
        # and this repeated condition can be removed according to Longitude
        FY2ELonData = self.__FY2EProvider.GetLongitude()
        MSGLonData = self.__MSGProvider.GetLongitude()
        print FY2ELonData
        print MSGLonData
        self.__FY2ESubarrayIndex = FY2ELonData.shape[1] # initializing SubarrayIndex(explained below)
        self.__MSGSubarrayIndex = MSGLonData.shape[1] # initializing SubarrayIndex(explained below)

        self.__minLonFY2E = N.min(FY2ELonData)
        self.__maxLonMSG = N.max(MSGLonData)
        if self.__minLonFY2E < self.__maxLonMSG:
            # choose average longitude of the repeated area as the separate line(the boundary)
            BoundaryLon = self.__minLonFY2E + (self.__maxLonMSG - self.__minLonFY2E) / 2.0
            self.__FY2ESubarrayIndex = N.where((FY2ELonData <= BoundaryLon)&(FY2ELonData != FY2ELonData[0,0]))# Dimension of the index is 1
            self.__MSGSubarrayIndex = N.where((MSGLonData > BoundaryLon)&(MSGLonData != MSGLonData[0,0]))

    def GetLatitude(self):
        print("----->Begin GetLatitude")
        self.CaculateSubarrayIndex() #ought to put in __init__() or OnParametersUpdate()
        FY2ELatData = self.__FY2EProvider.GetLatitude() # Dimension is 2

        FY2ELatData[self.__FY2ESubarrayIndex] = FY2ELatData[0,0] #now the Dimension is 1

        MSGLatData = self.__MSGProvider.GetLatitude()

        MSGLatData[self.__MSGSubarrayIndex] = 0

        #MSGLatData = MSGLatData.reshape(row,-1)
        RowNumFY2E, ColumnNumFY2E = FY2ELatData.shape  # RowNum is not equal to ColumnNum
        RowNumMSG, ColumnNumMSG = MSGLatData.shape  # RowNum is not equal to ColumnNum

        #LatMasaic = MSGLatData * 2  # to define a big array to store masaicked data
        LatMasaic = N.tile(MSGLatData, 2) # to define a big array to store masaicked data
        LatMasaic[:, ColumnNumMSG:] = LatMasaic[
            0, 0]  # left half side is MSG data,set right half side of the big array as filled vaule of MSG
        RowStart = (RowNumMSG - RowNumFY2E) / 2
        RowEnd = RowNumMSG - (RowNumMSG - RowNumFY2E) / 2
        ColumnStart = ColumnNumMSG
        ColumnEnd = ColumnNumFY2E + ColumnNumMSG
        FillValuePosition = N.where(FY2ELatData == FY2ELatData[0, 0])
        #FY2ELatData[FillValuePosition] = 65535
        FY2ELatData[FillValuePosition] = MSGLatData[0,0]

        LatMasaic[RowStart:RowEnd, ColumnStart:ColumnEnd] = FY2ELatData  # add FY2E data to the big array

        print("----->End GetLatitude")
        return LatMasaic

    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        print band
        FY2EData = self.__FY2EProvider.GetOBSData(band)
        MSGData = self.__MSGProvider.GetOBSData(band)
        #FY2EData = FY2EData[:,self.__FY2ESubarrayIndex:]
        #MSGData = MSGData[:,:self.__MSGSubarrayIndex]
        FY2EData[self.__FY2ESubarrayIndex] = FY2EData[0,0]
        MSGData[self.__MSGSubarrayIndex] = MSGData[0,0]
        RowNumFY2E, ColumnNumFY2E = FY2EData.shape  # RowNum is not equal to ColumnNum
        RowNumMSG, ColumnNumMSG = MSGData.shape  # RowNum is not equal to ColumnNum

        retMasaic = N.tile(MSGData, 2)
        retMasaic[:, ColumnNumMSG:] = retMasaic[
            0, 0]  # left half side is MSG data,set right half side of the big array as filled vaule of MSG
        RowStart = (RowNumMSG - RowNumFY2E) / 2
        RowEnd = RowNumMSG - (RowNumMSG - RowNumFY2E) / 2

        ColumnStart = ColumnNumMSG
        ColumnEnd = ColumnNumFY2E + ColumnNumMSG
        FillValuePosition = N.where(FY2EData == FY2EData[0, 0])
        FY2EData[FillValuePosition] = 65535
        retMasaic[RowStart:RowEnd, ColumnStart:ColumnEnd] = FY2EData  # add FY2E data to the big array

        # file = h5py.File("/home/bozi/Downloads/TestData/"+str(band)+".HDF")
        # file.create_dataset("LatMasaic",data = retMasaic)
        # file.close()
        return retMasaic


    def GetOBSDataCount(self):
        return self.__obsDataCount


    def GetAuxiliaryData(self, dataname):
        print("get auxiliry begin")
        FY2EData = self.__FY2EProvider.GetAuxiliaryData(dataname)
        MSGData = self.__MSGProvider.GetAuxiliaryData(dataname)
        FY2EData[self.__FY2ESubarrayIndex] = FY2EData[0, 0]
        MSGData[self.__MSGSubarrayIndex] = MSGData[0, 0]
        RowNumFY2E, ColumnNumFY2E = FY2EData.shape  # RowNum is not equal to ColumnNum
        RowNumMSG, ColumnNumMSG = MSGData.shape  # RowNum is not equal to ColumnNum
        retMasaic = N.tile(MSGData, 2)
        retMasaic[:, ColumnNumMSG:] = retMasaic[0, 0]  # left half side is MSG data,set right half side of the big array as filled vaule of MSG
        RowStart = (RowNumMSG - RowNumFY2E) / 2
        RowEnd = RowNumMSG - (RowNumMSG - RowNumFY2E) / 2
        ColumnStart = ColumnNumMSG
        ColumnEnd = ColumnNumFY2E + ColumnNumMSG
        FillValuePosition = N.where(FY2EData == FY2EData[0, 0])
        FY2EData[FillValuePosition] = 65535
        retMasaic[RowStart:RowEnd, ColumnStart:ColumnEnd] = FY2EData  # add FY2E data to the big array
        print("get auxiliary end")
        print retMasaic
        return retMasaic

    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList

    def SetDataDescription(self, value):
        self.__description = value

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription() + '_' + str(
                self.GetParameter().ProjectResolution)
        return self.__description


