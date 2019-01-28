from DataOuter.HdfDataOuter import *
from DataProvider.FY2E_MSG_Provider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing
import AuxiliaryDict

#L1FilePath = ''

def CreateAuxilaryProvider(resolution):
    provider_FY2E_MSG = FY2E_MSG_Provider()
    #set FY2E file path
    Lonfile_FY2E = Latfile_FY2E ='/home/bozi/Downloads/FY2E/FY2E_IJToLatLon.NOM'
    #set MSG file path
    Latfile_MSG = Lonfile_MSG ='/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc'

    provider_FY2E_MSG.SetLonLatFile(Latfile_FY2E,Lonfile_FY2E,Latfile_MSG,Lonfile_MSG)

    AuxiliaryNameDict_FY2E = dict()
    AuxiliaryDataDict_FY2E = dict()
    AuxiliaryNameDict_MSG = dict()
    AuxiliaryDataDict_MSG = dict()

    AuxiliaryNameDict_FY2E['SolarZenith'] = 'NOMSunZenith'
    AuxiliaryDataDict_FY2E['SolarZenith'] = '/home/bozi/Downloads/FY2E/FY2E_FDI_ALL_NOM_20170115_0430.hdf'
    AuxiliaryNameDict_FY2E['Latitude'] = 'Lat'
    AuxiliaryDataDict_FY2E['Latitude'] = '/home/bozi/Downloads/FY2E/FY2E_IJToLatLon.NOM'
    AuxiliaryNameDict_FY2E['Longitude'] = 'Lon'
    AuxiliaryDataDict_FY2E['Longitude'] = '/home/bozi/Downloads/FY2E/FY2E_IJToLatLon.NOM'

    AuxiliaryNameDict_MSG['SolarZenith'] = 'SolarZenith'
    AuxiliaryDataDict_MSG['SolarZenith'] = '/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc' #need be cacluated by lat/lon/time
    AuxiliaryNameDict_MSG['Latitude'] = 'lat'
    AuxiliaryDataDict_MSG['Latitude'] = '/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc'
    AuxiliaryNameDict_MSG['Longitude'] = 'lon'
    AuxiliaryDataDict_MSG['Longitude'] = '/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc'

    provider_FY2E_MSG.SetAuxiliaryDataFile(AuxiliaryNameDict_FY2E, AuxiliaryDataDict_FY2E,AuxiliaryNameDict_MSG, AuxiliaryDataDict_MSG)

    return  provider_FY2E_MSG


def ProcessProj(param, resolution):

    provider = CreateAuxilaryProvider(resolution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = '/home/bozi/Downloads/TestData/'
    auxparam.ProjectResolution = resolution
    auxparam.IsAuxiliaryFileMode = True
    ProcessProj(auxparam, resolution)
if __name__ == '__main__':

    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
    #param.OutputPath = '/FY4COMM/FY4A/L2/AGRIX/PRJ/'		#2016_10_14
    # ProcessProj(param, 2000,False)
    #
    # p1 = multiprocessing.Process(target = ProcessProj, args = (param,2000,False,))
    # p1.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,1000,False,))
    # p2.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,500,False,))
    # p2.start()
#    L1FilePath = sys.argv[4]
#    ProcessProj(param, int(sys.argv[3]),False)
#    auxfile = '/FY4COMM/FY4A/COM/PRJ/'+ param.GetParamDescription() + '_'+sys.argv[3]+'_'+param.ProjectTaskName+'.HDF'		#2016_10_14
    auxfile = '/home/bozi/Downloads/TestData/'+ param.GetParamDescription() + '_'+sys.argv[3]+'_'+param.ProjectTaskName+'.HDF'
    #auxfile ='/home/bozi/Downloads/TestData/'+ param.GetParamDescription() + '_'+'2000'+'_'+param.ProjectTaskName+'.HDF'
    if os.path.exists(auxfile) == False:
        ProcessAuxProj(int(sys.argv[3]))
        #ProcessAuxProj(2000)
    # auxfile = param.OutputPath + param.GetParamDescription() + '_1000_Proj.HDF'
    # if os.path.exists(auxfile) == False:
    #     ProcessAuxProj(1000)

    # auxfile = param.OutputPath + param.GetParamDescription() + '_500_Proj.HDF'
    # if os.path.exists(auxfile) == False:
    #     ProcessAuxProj(500)

    # p1 = multiprocessing.Process(target = ProcessProj, args = (param,2000,))
    # p1.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,1000,))
    # p2.start()
    #
    # p3 = multiprocessing.Process(target = ProcessProj, args = (param,500,))
    # p3.start()
    # ProcessProj(param,2000)
    # ProcessProj(param, 1000)
    # ProcessProj(param, 500)