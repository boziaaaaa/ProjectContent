from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from DataProvider.MSGProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing
import time

L1FilePath = ''


def CreateStdProjProvider(resolution):
    provider = MSGProvider()
    #Latfile = Lonfile = L1file = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103123011.nc"
    #Latfile = Lonfile = L1file ="/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101153011.nc"
    #Latfile = Lonfile = L1file = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc"
    #Latfile = Lonfile = L1file = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101140011.nc"
    Latfile = Lonfile = L1file ="/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101114510.nc"
    provider.SetLonLatFile(Latfile,Lonfile)
    print sys.argv[1]
    provider.SetL1File(L1file)
    provider.SetDataDescription('MSG_GLB_'+sys.argv[1])


    AuxiliaryName = dict()
    AuxiliaryPath = dict()
    #AuxiliaryName['SunAzimuth'] = 'NOMAzimuth'
    #AuxiliaryName['SunZenith'] = 'NOMSunZenith'
    #AuxiliaryPath['SunAzimuth'] = \
    #AuxiliaryPath['SunZenith'] = '/home/bozi/Downloads/TestData/MSGSolarZenith20100101_1145.HDF.h5'
    AuxiliaryName['Latitude'] = 'lat'
    AuxiliaryName['Longitude'] = 'lon'
    AuxiliaryPath['Longitude'] = AuxiliaryPath['Latitude'] = L1file
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
#    auxparam.OutputPath = sys.argv[5]								#2016.10.12
    auxparam.ProjectResolution = resolution
##    auxparam.IsAuxiliaryFileMode = True
##    ProcessProj(auxparam, resolution, True)
    ProcessProj(auxparam, resolution)
if __name__ == '__main__':
    starttime = time.clock()
    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103123011.nc"
    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101153011.nc"
    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc"
    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101140011.nc"
    L1FilePath ="/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101114510.nc"
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
#    param.OutputPath = '/FY4COMM/FY4A/L2/AGRIX/PRJ/' #2016.10.12
#####    param.OutputPath = sys.argv[5]										#2016.10.12
    param.OutputPath = '/mnt/hgfs/D/temp_FY2E_MSG/'
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

    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103123011.nc"
    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101153011.nc"

    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100103121510.nc"
    #L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101140011.nc"
    L1FilePath = "/home/bozi/Downloads/MSG/W_XX-EUMETSAT-Darmstadt,VIS+IR+IMAGERY,MSG2+SEVIRI_C_EUMG_20100101114510.nc"

    ProcessProj(param, int(sys.argv[3]))

    endtime = time.clock()
    print(endtime-starttime)
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