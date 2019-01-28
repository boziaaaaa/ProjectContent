from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from DataProvider.FY2EProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing
import time

L1FilePath = ''


def CreateStdProjProvider(resolution):
    provider = FY2EProvider()

    Lonfile = Latfile ='/home/bozi/Downloads/FY2E/FY2E_IJToLatLon.NOM'
    L1file = '/home/bozi/Downloads/FY2E/FY2E_FDI_ALL_NOM_20170115_0430.hdf'


    provider.SetLonLatFile(Latfile,Lonfile)

    print sys.argv[1]
    provider.SetL1File(L1file)
    #provider.SetDataDescription('Himawari8_OBI_'+sys.argv[1])
    provider.SetDataDescription('FY2E'+sys.argv[1])

    AuxiliaryName = dict()
    AuxiliaryPath = dict()
    # AuxiliaryName['SunAzimuth'] = 'NOMAzimuth'
    # AuxiliaryName['SunZenith'] = 'NOMSunZenith'
    # AuxiliaryPath['SunAzimuth'] = AuxiliaryPath['SunZenith'] = L1file
    AuxiliaryName['Latitude'] = 'Lat'
    AuxiliaryName['Longitude'] = 'Lon'
    AuxiliaryPath['Latitude'] = AuxiliaryPath['Longitude'] = Lonfile
    provider.SetAuxiliaryDataFile(AuxiliaryName, AuxiliaryPath)

    return  provider

def ProcessProj(param,resolution):

    provider = CreateStdProjProvider(resolution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = '/mnt/hgfs/D/temp_FY2E_MSG/' #2016.10.12
    auxparam.ProjectResolution = resolution

    ProcessProj(auxparam, resolution)
if __name__ == '__main__':
    starttime = time.clock()

    L1FilePath = sys.argv[4]
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])

    param.OutputPath = '/mnt/hgfs/D/temp_FY2E_MSG/'

    L1FilePath = sys.argv[4]
    ProcessProj(param, int(sys.argv[3]))

    endtime = time.clock()

    print "read: %f s" % (endtime - starttime)
