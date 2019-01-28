from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD


class MersiProvider(DataProvider):
    def __init__(self):
        super(MersiProvider, self).__init__()
        self.__AuxiliaryDataNamesList = dict()
        self.__HdfFileHandleList = dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        self.__BandWaveLenthList = None

        self.__HdfOperator = HdfOperator()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataWidthAndHeight = 0
        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList = None

        # del self.__AuxiliaryDataNamesList
        for filehandleName in self.__HdfFileHandleList:
            filehandle = self.__HdfFileHandleList[filehandleName]
            if filehandle.id.valid:
                filehandle.close()

        self.__HdfFileHandleList.clear()

        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(MersiProvider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'Himawari8'
        self.OrbitInfo.Sensor = 'OBI'
        self.OrbitInfo.OrbitDirection = ''

        self.OrbitInfo.Width = self.__dataWidthAndHeight
        self.OrbitInfo.Height = self.__dataWidthAndHeight

        # solarzenith = self.GetSolarZenith()
        # if solarzenith[int(self.__dataWidthAndHeight/2),int(self.__dataWidthAndHeight/2)] <=85:
        #     self.OrbitInfo.DNFlag = 'D'
        # else:
        #     self.OrbitInfo.DNFlag = 'N'

        self.OrbitInfo.Date = self.GetDate()
        self.OrbitInfo.Time = self.GetTime()

    def GetDate(self):
        pass

    def GetTime(self):
        pass

    def OnParametersUpdate(self):
        super(MersiProvider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount = len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

    def SetLonLatFile(self, latfile, lonfile):
        # self.__latFileHandle = self.__HdfOperator.Open(latfile)
        # self.__lonFileHandle = self.__HdfOperator.Open(lonfile)l
        self.__HdfFileHandleList['Latitude'] = self.__HdfOperator.Open(latfile)
        self.__HdfFileHandleList['Longitude'] = self.__HdfOperator.Open(lonfile)

    def SetL1File(self, file):

        # self.__L1DataFileHandle = self.__HdfOperator.Open(file)
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)


        if '_1000M' in file:
            self.__dataRes = 1000
            #self.__dataWidthAndHeight = 11000

        self.__InitOrbitInfo()

    def SetAuxiliaryDataFile(self, AuxiliaryNameDict, AuxiliaryDataDict):

        for key in AuxiliaryDataDict:
            self.__HdfFileHandleList[key] = self.__HdfOperator.Open(AuxiliaryDataDict[key])
            self.__AuxiliaryDataNamesList[key] = AuxiliaryNameDict[key]
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

        lon = self.GetDataSet(self.__HdfFileHandleList['Longitude'], '/', 'Longitude')
        return lon
    def GetLatitude(self):

        lat = self.GetDataSet(self.__HdfFileHandleList['Latitude'], '/', 'Latitude')
        return lat
    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):

        bandname = self.__GetOBSDatasetName(band, self.__dataRes)
        caltableName = 'CAL' + self.OrbitInfo.BandsWavelength[band]
        ret = None
        if bandname != '':

            data = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', bandname)[:, :].astype(N.int32)
            # caltable = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', caltableName)
            # caltable = self.__HdfOperator.ReadHdfDataset(self.__HdfFileHandleList['L1'], '/', caltableName)[:].astype(
            #     N.float32)
            # height = data.shape[0]
            # width = data.shape[1]
            # bantype = 1
            # if self.OrbitInfo.BandsType[band] == 'REF':
            #     bantype = 0
            # ret = SD.CreateH8CalibrationData(int(width), int(height), bantype, caltable, data)
            ret = data
        return ret

    def __GetOBSDatasetName(self, band, datares):
        bandname = ''
        waveLength = self.OrbitInfo.BandsWavelength[band]
        if self.OrbitInfo.BandsType[band] == 'REF':
            bandname = 'NOMChannelVIS' + waveLength + '_' + str(datares)
        else:
            bandname = 'NOMChannelIRX' + waveLength + '_' + str(datares)
        bandname = "Kd490"
        return bandname

    def GetOBSDataCount(self):
        return self.__obsDataCount

    def GetDataSet(self, filehandle, group, ds):
        #print "========>",ds
        data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)

        startLine = self.startLine
        endlLine = self.endLine
        ret = None

        # Interpolate 2016_11_4_yuanbo
        if (ds == 'NOMSunAzimuth' or ds == 'NOMSunZenith') and (self.__dataRes == 500 or self.__dataRes == 1000):
            RowNum = len(data)
            ColumnNum = len(data[0])
            InputArray = N.array(data).reshape(-1)
            zoomRate = 2000 / self.__dataRes
            data = SD.BilinearInterPolateData(int(RowNum), int(ColumnNum), int(zoomRate), InputArray)
            data = data.reshape((RowNum * zoomRate), (ColumnNum * zoomRate))

        if startLine != -1 & endlLine != -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:, :]
        #print ret
        return ret

    def GetAuxiliaryData(self, dataname):

        dsname = self.__AuxiliaryDataNamesList[dataname]
        ret = None
        if dsname == '':
            return ret

        ret = self.GetDataSet(self.__HdfFileHandleList[dataname], '/', dsname)

        # RowNum = len(ret)
        # ColumnNum =len(ret[0])
        # InputArray = ret.reshape(-1)
        # zoomRate = 2
        # ret = INTERPOLATE.InterPolateData(int(RowNum),int(ColumnNum),int(zoomRate),InputArray)
        # ret = ret.reshape(RowNum*2, ColumnNum*2)

        return ret

    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList

    def SetDataDescription(self, value):
        self.__description = value

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription() + '_' + str(
                self.GetParameter().ProjectResolution)
        return self.__description


