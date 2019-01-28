from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD
from PIL import Image


class FY3B_MersiProvider(DataProvider):
    def __init__(self):
        super(FY3B_MersiProvider, self).__init__()
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
        super(FY3B_MersiProvider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'FY3B'
        self.OrbitInfo.Sensor = 'Mersi'
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
        super(FY3B_MersiProvider, self).OnParametersUpdate()

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
        print "did i com here"
        # self.__L1DataFileHandle = self.__HdfOperator.Open(file)
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)


        if '_0250M' in file:
            self.__dataRes = 250
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
        # lon = N.array(lon)
        # height,width = lon.shape
        # lon = Image.fromarray(lon)
        # lon = lon.resize((width*4,height*4))
        # lon = N.array(lon)
        return lon
    def GetLatitude(self):

        lat = self.GetDataSet(self.__HdfFileHandleList['Latitude'], '/', 'Latitude')
        # lat = N.array(lat)
        # height,width = lat.shape
        # lat = Image.fromarray(lat)
        # lat = lat.resize((width*4,height*4))
        # lat = N.array(lat)
        print lat.shape
        return lat
    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):
        bandname = self.__GetOBSDatasetName(band[3:], self.__dataRes)
        print bandname
        ret = None
        if bandname != '':

            data = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', bandname)[:, :].astype(N.int32)
            if "Ref" in bandname:
               Slope = self.__HdfFileHandleList['L1'][bandname].attrs["Slope"][0]
               # data = data * Slope
               print data
               VIS_Cal_Coeff = self.__HdfFileHandleList['L1']['RSB_Cal_Cor_Coeff'][:]
               # k = 0
               # if "_b1" in bandname:
               #     k = 0
               # elif "_b2" in bandname:
               #     k = 1
               # elif "_b3" in bandname:
               #     k = 2
               # a = VIS_Cal_Coeff[k][0]
               # b = VIS_Cal_Coeff[k][1]
               # c = VIS_Cal_Coeff[k][2]
               #
               # data = a + b*data + c*(data*data)
               # data = data * 1000
               # print "222222222",a,b,c
               # print data

            elif "Emissive" in bandname:
               IR_Cal_Coeff = self.__HdfFileHandleList['L1']['Calibration/IR_Cal_Coeff'][:]
            ret = data
        return ret

    def __GetOBSDatasetName(self, band, datares):
        #470,550,650,865,10800,12000
        bandname = ''        
        #bandname = 'EV_250_RefSB_b' + band
        if band == "470":
          bandname = 'EV_250_RefSB_b1'
        elif band == "550":
          bandname = 'EV_250_RefSB_b2'
        elif band == "650":
          bandname = 'EV_250_RefSB_b3'
        elif band == "865":
          bandname = 'EV_250_RefSB_b4'
        elif band == '10800':
          bandname = "EV_250_Emissive_b24" 
        elif band == '12000':
          bandname = "EV_250_Emissive_b25"
        #if self.OrbitInfo.BandsType[band] == 'REF':
        #    bandname = 'EV_250_RefSB_b' + band
        #else:
         #   bandname = 'EV_250_Emissive_b25' + waveLength + '_' + str(datares)
        return bandname

    def GetOBSDataCount(self):
        return self.__obsDataCount

    def GetDataSet(self, filehandle, group, ds):
        print "========>",ds
        if "Latitude" in ds or "ongitude" in ds:
            data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)
            data = N.array(data.value)
            height,width = data.shape
            data = Image.fromarray(data)
            data = data.resize((width*4,height*4))
            data = N.array(data)
        else:
            data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)
        # print data.value
        startLine = self.startLine
        endlLine = self.endLine
        ret = None

        if startLine != -1 & endlLine != -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:, :]
        print ret
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


