from DataOuter.HdfDataOuter import *
#from DataProvider.H8DataProvider import *
#from DataProvider.FY3AVirrProvider import *
from DataProvider.FY3CVirrProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing
import time
import os
import re
L1FilePath = ''


def CreateStdProjProvider(resolution):
    provider = FY3CVirrProvider()
    L2file = sys.argv[4]
    # temp_str = sys.argv[4] + 'FY3C_VIRRX_GBAL_L1_'+sys.argv[1]+'_GEOXX_MS.HDF'
    # temp_str = temp_str.replace("SST","VIRRX")
    # temp_str = temp_str.replace("-bak","")
    # Lonfile = Latfile = temp_str.replace("SST","VIRRX")
    Lonfile = Latfile = sys.argv[6] + sys.argv[1][0:8] + '/FY3C_VIRRX_GBAL_L1_' + sys.argv[1] + '_GEOXX_MS.HDF'
    print  Lonfile
    if (os.path.exists(L2file) == False):
        print("Input L2file Do Not Exist:")
        print(L2file)
        exit()
    if (os.path.exists(Lonfile) == False):
        print("Input LatitudeFile/LongitudeFile Do Not Exist:")
        print(Latfile)
        exit()

    provider.SetLonLatFile(Latfile, Lonfile)
    temp_str = re.split("[/.]",L2file)[-2]
    temp_str = temp_str.replace("_1000M_","_"+str(resolution)+"M_")
    temp_str = temp_str.replace("_NUL_","_GLL_")
    print temp_str
    #provider.SetDataDescription('FY3C_' + sys.argv[1])
    provider.SetDataDescription(temp_str)

    AuxiliaryName = dict()
    AuxiliaryPath = dict()
    AuxiliaryName['sea_surface_temperature'] = 'sea_surface_temperature'
    AuxiliaryName['quality_flag'] = 'quality_flag'
    AuxiliaryPath['sea_surface_temperature'] = L2file
    AuxiliaryPath['quality_flag'] = L2file
    provider.SetAuxiliaryDataFile(AuxiliaryName, AuxiliaryPath)

    return provider


def ProcessProj(param, resolution):
    provider = CreateStdProjProvider(resolution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()


def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = sys.argv[5]  # 2016.10.12
    auxparam.ProjectResolution = resolution
    auxparam.IsAuxiliaryFileMode = True
    ProcessProj(auxparam, resolution)


if __name__ == '__main__':
    starttime = time.clock()
    #print "@@@@@@@@@@@@@@@"
    # L1FilePath = sys.argv[4]
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])

    param.OutputPath = sys.argv[5]

    # L1FilePath = sys.argv[4]
    ProcessAuxProj(int(sys.argv[3]))

    endtime = time.clock()

    print "read: %f s" % (endtime - starttime)
