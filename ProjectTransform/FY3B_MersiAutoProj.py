from DataOuter.HdfDataOuter import *
from DataProvider.FY3B_MersiProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing
import time
import os
L1FilePath = ''


def CreateStdProjProvider(resolution):
    provider = FY3B_MersiProvider()

    YYMMDD_HHMM = sys.argv[1][0:8]+"_"+sys.argv[1][8:]
    L1file =           sys.argv[4] + "FY3B_MERSI_GBAL_L1_"+YYMMDD_HHMM+"_0250M_MS.HDF"
    # Lonfile = Latfile = sys.argv[4] +"FY3B_MERSI_GBAL_L1_"+YYMMDD_HHMM+"_GEOQK_MS.HDF"
    Lonfile = Latfile = L1file

    print L1file
    if(os.path.exists(L1file) == False):
        print("Input L1file Do Not Exist:")
        print(L1file)
        exit()
    if(os.path.exists(Lonfile) == False):
        print("Input LatitudeFile/LongitudeFile Do Not Exist:")
        print(Latfile)
        exit()

    provider.SetL1File(L1file)
    provider.SetLonLatFile(Latfile,Lonfile)

#    print sys.argv[1]
    #provider.SetL1File(L1file)
    #provider.SetDataDescription('Himawari8_OBI_'+sys.argv[1])
    provider.SetDataDescription('FY3B_MERSI_'+sys.argv[1]+"_"+sys.argv[3])

    AuxiliaryName = dict()
    AuxiliaryPath = dict()
    AuxiliaryName['Latitude'] = 'Latitude'
    AuxiliaryName['Longitude'] = 'Longitude'

    AuxiliaryPath['Latitude'] = \
    AuxiliaryPath['Longitude'] = Lonfile
    # AuxiliaryPath['SunAzimuth'] = \
    #     AuxiliaryPath['SunZenith'] = \
    #     AuxiliaryPath['Latitude'] = \
    #     AuxiliaryPath['Longitude'] = \
    #     AuxiliaryPath['SensorAzimuth'] = \
    #     AuxiliaryPath['SensorZenith'] = \
    #     AuxiliaryPath['LandCover'] = \
    #     AuxiliaryPath['LandSeaMask'] =  GEOfile
    #
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
    # auxparam = paramparser.parseXML(sys.argv[2])
    # auxparam.OutputPath = sys.argv[5] #2016.10.12
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = sys.argv[5]
    auxparam.ProjectResolution = resolution
    #auxparam.IsAuxiliaryFileMode = True

    ProcessProj(auxparam, resolution)
    
    
def remakeXML():

    YYMMDD_HHMM = sys.argv[1][0:8]+"_"+sys.argv[1][8:]
    L1file =           sys.argv[4] + "FY3B_MERSI_GBAL_L1_"+YYMMDD_HHMM+"_0250M_MS.HDF"
    # Lonfile = Latfile = sys.argv[4] +"FY3B_MERSI_GBAL_L1_"+YYMMDD_HHMM+"_GEOQK_MS.HDF"
    Lonfile = Latfile = L1file

    print Lonfile
    import h5py
    import numpy
    fileHandle = h5py.File(Lonfile)
    Latitude = fileHandle["Latitude"]
    Longitude = fileHandle["Longitude"]
    maxLatitude = numpy.max(Latitude)
    minLatitude = numpy.min(Latitude)
    maxLongitude = numpy.max(Longitude)
    minLongitude = numpy.min(Longitude)
    fileHandle.close()
    print maxLatitude,minLatitude,maxLongitude,minLongitude
if __name__ == '__main__':
    starttime = time.clock()
    

    L1FilePath = sys.argv[4]
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
    param.OutputPath = sys.argv[5]
    ProcessAuxProj(int(sys.argv[3]))
    # YYMMDD_HHMM = sys.argv[1][0:8]+"_"+sys.argv[1][8:]
    #
    # inputHDF = sys.argv[4] + "FY3B_MERSI_GBAL_L1_"+YYMMDD_HHMM+"_0250M_MS.HDF"
    # outputHDF = sys.argv[5]+'FY3B_MERSI_'+sys.argv[1]+"_"+sys.argv[3]+".HDF"
    # print inputHDF
    # print projHDF
    #
    # f_in = h5py.File(inputHDF)
    # attrs = f_in["EV_250_RefSB_b1"].attrs
    # RSB_Cal_Cor_Coeff = f_in["RSB_Cal_Cor_Coeff"].value
    # f_in.close()
    #
    # f_out = h5py.File(outputHDF)
    # f_out.create_dataset("RSB_Cal_Cor_Coeff",data = RSB_Cal_Cor_Coeff)
    # f_out["EV_250_RefSB_b1"].attrs = attrs
    # f_out.close



    endtime = time.clock()
    print "read: %f s" % (endtime - starttime)
