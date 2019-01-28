from DataOuter.HdfDataOuter import *
from DataProvider.FY2E_MSG_Provider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing


L1FilePath = ''


def CreateStdProjProvider(resolution):
    #provider = FY2Eprovider()
    provider_FY2E_MSG = FY2E_MSG_Provider()
    #set FY2E file path
    Lonfile_FY2E = Latfile_FY2E ='/home/bozi/Downloads/FY2E/FY2E_IJToLatLon.NOM'
    L1file_FY2E = '/home/bozi/Downloads/FY2E/FY2E_FDI_ALL_NOM_20170115_0430.hdf'
    #set MSG file path
    Latfile_MSG = Lonfile_MSG = L1file_MSG ='/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc'
    provider_FY2E_MSG.SetFile(Latfile_FY2E,Lonfile_FY2E,L1file_FY2E,Latfile_MSG,Lonfile_MSG,L1file_MSG)
    #set description
    provider_FY2E_MSG.SetDataDescription('FY2E_MSG'+sys.argv[1])

    return  provider_FY2E_MSG

def ProcessProj(param,resolution):

    provider = CreateStdProjProvider(resolution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = '/home/bozi/Downloads/TestData/' #2016.10.12
#    auxparam.OutputPath = sys.argv[5]								#2016.10.12
    auxparam.ProjectResolution = resolution
##    auxparam.IsAuxiliaryFileMode = True
##    ProcessProj(auxparam, resolution, True)
    ProcessProj(auxparam, resolution)
if __name__ == '__main__':
	
    #L1FilePath = sys.argv[4]
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
#    param.OutputPath = '/FY4COMM/FY4A/L2/AGRIX/PRJ/' #2016.10.12
#####    param.OutputPath = sys.argv[5]										#2016.10.12
    param.OutputPath = '/home/bozi/Downloads/TestData/'
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
    L1FilePath = sys.argv[4]
    ProcessProj(param, int(sys.argv[3]))


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