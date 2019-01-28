from DataOuter.HdfDataOuter import *
from DataProvider.FY4A_DAT_Provider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing


#L1FilePath = ''

def CreateAuxilaryProvider(resolution):
    provider = FY4A_DAT_Provider()
    AuxiliaryNameDict = {}
    AuxiliaryDataDict = {}
    #AuxiliaryNameDict['Latitude'] = 'Lat'
    #AuxiliaryNameDict['Longitude'] = 'Lon'
    AuxiliaryNameDict['f30yInterpSSTData'] = 'f30yInterpSSTData'
    #AuxiliaryDataDict['Latitude'] = 'D:/FY4A_DAT/FY4A_OBI_2000M_NOM_LATLON.HDF'
    #AuxiliaryDataDict['Longitude'] = 'D:/FY4A_DAT/FY4A_OBI_2000M_NOM_LATLON.HDF'
    AuxiliaryDataDict['f30yInterpSSTData'] = 'D:/FY4A_DAT/AHI8_OBI_2000M_NOM_XXXX1231.dat'

    Latfile =Lonfile= 'D:/FY4A_DAT/AHI8_OBI_2000M_NOM_LATLON.HDF'

    provider.SetLonLatFile(Latfile,Lonfile)
    provider.SetAuxiliaryDataFile(AuxiliaryNameDict, AuxiliaryDataDict)

    return  provider


def ProcessProj(param, resolution):

    provider = CreateAuxilaryProvider(resolution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = 'D:/FY4A_DAT/'
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
    auxfile = 'D:/FY4A_DAT/'+ param.GetParamDescription() + '_'+sys.argv[3]+'_'+param.ProjectTaskName+'.HDF'
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