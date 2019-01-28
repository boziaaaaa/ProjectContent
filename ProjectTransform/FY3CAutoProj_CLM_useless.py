from DataOuter.HdfDataOuter import *
from DataProvider.FY3CVirrProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import time
import os
L1FilePath = ''


def CreateStdProjProvider(resolution):
    provider = FY3CVirrProvider()
    Lonfile = Latfile =sys.argv[4] + 'FY3C_VIRRX_GBAL_L1_'+sys.argv[1]+'_GEOXX_MS.HDF'
    CLMfile = sys.argv[4] + 'CLM/FY3C_VIRRX_ORBT_L2_CLM_MLT_NUL_'+sys.argv[1]+'_1000M_MS.HDF'
    if(os.path.exists(Lonfile) == False):
        print("Input LatitudeFile/LongitudeFile Do Not Exist:")
        print(Latfile)
        exit()

    provider.SetLonLatFile(Latfile,Lonfile)

    print sys.argv[1]
    #provider.SetL1File(L1file)
    #provider.SetDataDescription('FY3C'+sys.argv[1])

    AuxiliaryName = dict()
    AuxiliaryPath = dict()
    AuxiliaryName['SDS1'] = 'SDS1'
    AuxiliaryPath['SDS1']  =  CLMfile
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
    auxparam.OutputPath = sys.argv[5] #2016.10.12
    auxparam.ProjectResolution = resolution
    auxparam.IsAuxiliaryFileMode = True
    ProcessProj(auxparam, resolution)
if __name__ == '__main__':
    starttime = time.clock()

    #L1FilePath = sys.argv[4]
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])

    param.OutputPath = sys.argv[5]

    #L1FilePath = sys.argv[4]
    ProcessAuxProj( int(sys.argv[3]))

    endtime = time.clock()

    print "read: %f s" % (endtime - starttime)
