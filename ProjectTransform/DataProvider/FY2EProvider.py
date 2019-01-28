from DataProvider import *
from HdfOperator import *
import types
import numpy as N
import struct
from Parameters import *
import ProjOutputData_module as SD


class FY2EProvider(DataProvider):
    def __init__(self):
        super(FY2EProvider, self).__init__()
        self.__AuxiliaryDataNamesList = dict()
        self.__HdfFileHandleList = dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        #self.__BandWaveLenthList = None # temporary changed as below
        self.__BandWaveLenthList = ['0060','1100','1200','0700','0380']
        self.__HdfOperator = HdfOperator()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        #self.__dataWidthAndHeight = 0
        self.__dataWidthAndHeight = 2288

        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList = None

        # del self.__AuxiliaryDataNamesList
        for filehandleName in self.__HdfFileHandleList:
            filehandle = self.__HdfFileHandleList[filehandleName]
            if filehandleName != 'Latitude' and filehandleName != 'Longitude':
              if filehandle.id.valid:
                 filehandle.close()

        self.__HdfFileHandleList.clear()

        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(FY2EProvider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'FY2E'
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
        #filehandle = self.__HdfFileHandleList['L1']
        #
        #year = self.__HdfOperator.ReadHdfAttri(filehandle, '/', 'iStartYear')
        #month = self.__HdfOperator.ReadHdfAttri(filehandle, '/', 'iStartMonth')
        #day = self.__HdfOperator.ReadHdfAttri(filehandle, '/', 'iStartDay')
        # strmonth = '{:0>2}'.format(str(month[0]))
        # srtday = '{:0>2}'.format(str(day[0]))
        # stryear = '{:0>4}'.format(str(year[0]))
        #return stryear + strmonth + srtday
        return

    def GetTime(self):
        # filehandle = self.__HdfFileHandleList['L1']
        #
        # hour = self.__HdfOperator.ReadHdfAttri(filehandle, '/', 'iStartHour')
        # minute = self.__HdfOperator.ReadHdfAttri(filehandle, '/', 'iStartMinute')
        #
        # strhour = '{:0>2}'.format(str(hour[0]))
        # srtminute = '{:0>2}'.format(str(minute[0]))

        return #strhour + srtminute

    def OnParametersUpdate(self):
        super(FY2EProvider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount = len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

    def SetLonLatFile(self, latfile, lonfile):
        # self.__latFileHandle = self.__HdfOperator.Open(latfile)
        # self.__lonFileHandle = self.__HdfOperator.Open(lonfile)l
        self.__HdfFileHandleList['Latitude'] = latfile
        self.__HdfFileHandleList['Longitude'] = lonfile

    def SetL1File(self, file):

        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)
        self.__dataRes = 1250
        self.__dataWidthAndHeight = 2288
        self.__InitOrbitInfo()

    def SetAuxiliaryDataFile(self, AuxiliaryNameDict, AuxiliaryDataDict):

        for key in AuxiliaryDataDict:
            if key=='Latitude' or key == 'Longitude':#lat/lon file is not hdf, is binary file
                self.__HdfFileHandleList[key] = AuxiliaryDataDict[key]
            else:
                self.__HdfFileHandleList[key] = self.__HdfOperator.Open(AuxiliaryDataDict[key])
            self.__AuxiliaryDataNamesList[key] = AuxiliaryNameDict[key]

        return

    def CreateBandsInfo(self):

        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB' + str(wavelength)] = wavelength
            if int(wavelength) > 230:
                self.OrbitInfo.BandsType['EVB' + str(wavelength)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB' + str(wavelength)] = 'REF'

    def IsLittle_Endian(self):
        '''to judge wether this mechine is Little Endian or Big Endian'''
        a = 0x12345678
        result = struct.pack('i', a)  # 'result' is a string
        if hex(ord(result[0])) == '0x78':
            print 'this mechine is Little End,Need Change!'
            IsLittleEnd = '1'
        else:
            #print 'this mechine is Big End,Do not need Change'
            IsLittleEnd = '0'
        return IsLittleEnd
    def LittleEndToBigEnd(self,WidthAndHeight,LonLatData):
        Length = WidthAndHeight * WidthAndHeight * 2
        Format1 = ">" + str(Length) + "file"  # Big end
        Format2 = "<" + str(Length) + "file"  # Little end
        LonLatData_binary = struct.pack(Format1, *LonLatData)  # Little end need this convert
        LonLatData_float = struct.unpack(Format2, LonLatData_binary)  # Little end need this convert
        return LonLatData_float
    def GetLongitude(self):
        Lon = self.GetDataSet(self.__HdfFileHandleList['Longitude'], '/', 'Lon')
        file = h5py.File('/home/bozi/Downloads/TestData/Lon.HDF.h5', 'w')
        file.create_dataset('Lon', data=Lon)
        file.close
        Lon = N.array(Lon)
        return Lon

    def GetLatitude(self):
        Lat = self.GetDataSet(self.__HdfFileHandleList['Latitude'], '/', 'Lat')
        file = h5py.File('/home/bozi/Downloads/TestData/Lat.HDF.h5', 'w')
        file.create_dataset('Lat', data=Lat)
        file.close
        Lat = N.array(Lat)
        return Lat

    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):

        bandname,caltableName = self.__GetOBSDatasetName(band)
        ret = None
        if bandname != '':
            data = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', bandname)[:, :].astype(N.int32)
            caltable = self.__HdfOperator.ReadHdfDataset(self.__HdfFileHandleList['L1'], '/', caltableName)[:].astype(
                N.float32)
            height = data.shape[0]
            width = data.shape[1]
            bantype = 1
            ref_slope = 1.0
            if self.OrbitInfo.BandsType[band] == 'REF':
                bantype = 0
                ref_slope = 0.01
            ret = SD.CreateH8CalibrationData(int(width), int(height), bantype, caltable, data)
            ret = ret * ref_slope
            # file = h5py.File('/home/bozi/Downloads/TestData/GetOBSData'+band+'.HDF.h5', 'w')
            # file.create_dataset('bandname', data=ret)
            # file.close()
        return ret

    def __GetOBSDatasetName(self, band):
        bandname = ''
        waveLength = self.OrbitInfo.BandsWavelength[band]
        if waveLength == '1100':
            bandname = 'NOMChannelIR1'
            caltableName = 'CALChannelIR1'
        elif waveLength == '1200':
            bandname = 'NOMChannelIR2'
            caltableName = 'CALChannelIR2'
        elif waveLength == '0700':
            bandname = 'NOMChannelIR3'
            caltableName = 'CALChannelIR3'
        elif waveLength == '0380':
            bandname = 'NOMChannelIR4'
            caltableName = 'CALChannelIR4'
        elif waveLength == '0060':
            bandname = 'NOMChannelVIS'
            caltableName = 'CALChannelVIS'
        return bandname,caltableName

    def GetOBSDataCount(self):
        return self.__obsDataCount



    def GetDataSet(self, filehandle, group, ds):
        print(ds)
        if ds == "Lon" or ds == "Lat": #read latitude and longitude data
            filehandle = open(filehandle)  # read binary file
            rawdata = filehandle.read()
            LonLatData = N.frombuffer(rawdata, 'file')
            LonLatData = N.array(LonLatData)
            IsLittleEnd = self.IsLittle_Endian() #to judge wether mechine is Little Endian
            if IsLittleEnd == '1':#latitude and longitude data need byte position convert
                LonLatData_float = self.LittleEndToBigEnd(self.__dataWidthAndHeight, LonLatData)
            else:# do not need
                LonLatData_float = LonLatData

            if ds == "Lon":
                Lon = N.array(LonLatData_float[0:2288 * 2288])
                data = Lon.reshape(2288, 2288)
            else:
                Lat = N.array(LonLatData_float[2288 * 2288:])
                data = Lat.reshape(2288, 2288)
        else: #read reflectece and brightness temperature data
            data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)

        startLine = self.startLine
        endlLine = self.endLine

        if startLine != -1 & endlLine != -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:, :]

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


