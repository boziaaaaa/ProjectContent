from DataOuter.HdfDataOuter import *
from DataProvider.FY2E_MSG_Provider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import numpy as N



#from PIL import Image
#def dI(name,data):
#    Image.fromarray(data.astype('u1')*255,'L').save('/mnt/hgfs/D/temp_FY2E_MSG/%s.png'% name)

if __name__ == '__main__':
    # DataResolution = sys.argv[3]  #2017_4_7
    # DataTime = sys.argv[1]        #2017_4_7
    # DataTime = int(DataTime[9:11])#2017_4_7
    # L1FilePath = sys.argv[4]
    # paramparser = ParameterParser()
    # param = paramparser.parseXML(sys.argv[2])
    # param.OutputPath = sys.argv[5]

    # L1FilePath = sys.argv[4]

    HDFFilePath1 = '/mnt/hgfs/D/temp_FY2E_MSG/FY2E20170505_0606_LATLONG.HDF'
    HDFFilePath2 = '/mnt/hgfs/D/temp_FY2E_MSG/MSG_GLB_20170505_0606_LATLONG.HDF'
    # time1 = '20170517_0804'
    # time2 = '20170517_0507'
    # time1 = time1.replace('_', '')
    # time2 = time2.replace('_', '')
    # time1 = int(time1)
    # time2 = int(time2)

    OutImageFileName = '/mnt/hgfs/D/temp_FY2E_MSG/FY2E_MSG.HDF'
    if (os.path.exists(HDFFilePath1) == False):
        print("Input HDFFilePath1 Do Not Exist-->")
        print(HDFFilePath1)
        exit()
    if (os.path.exists(HDFFilePath2) == False):
        print("Input HDFFilePath2 Do Not Exist-->")
        print(HDFFilePath2)
        exit()
    # read data
    hdf_1 = h5py.File(HDFFilePath1)
    hdf_2 = h5py.File(HDFFilePath2)
    latData_1 = hdf_1['Latitude'].value / 100.0
    lonData_1 = hdf_1['Longitude'].value / 100.0
    #SunZenith_1 = hdf_1['SunZenith'].value
    Band1_1 = hdf_1['EVB0060'].value
    #Band2_1 = hdf_1['EVB2'].value
    # Band4_1 = hdf_1['EVB3'].value
    latData_2 = hdf_2['Latitude'].value / 100.0
    lonData_2 = hdf_2['Longitude'].value / 100.0
    #SunZenith_2 = hdf_2['SunZenith'].value
    Band1_2 = hdf_2['EVB0060'].value
    # Band2_2 = hdf_2['EVB2'].value
    # Band4_2 = hdf_2['EVB3'].value

    # mask_FY2E = mask_MSG = latData_1
    # mask_FY2E[:,:] = 0
    # mask_MSG[:,:] = 0
    mask_FY2E = latData_1 < 65535e-2
    mask_MSG = latData_2 < 655.35

    mask_repeat = mask_FY2E & mask_MSG

    mask_temp = N.argwhere(mask_repeat).T[1]
    midx = mask_temp.max() + mask_temp.min()
    midx /= 2

    #dI('mask_repeat', mask_repeat)
    #dI('mask_FY2E', mask_FY2E)
    #dI('mask_MSG', mask_MSG)
    #print midx
    mask_repeat[:,:midx] = 0
    #mask_tempRight[:,midx+1:] = 0

    mask_MSG -= mask_repeat
    Index_MSG = mask_MSG==0

    #dI('Index_MSG', Index_MSG)
    #dI('Band1_1', Band1_1/65535.)
    #dI('Ban8d1_2', Band1_2/65535.)

    Band1_2[Index_MSG]=Band1_1[Index_MSG]
    with h5py.File(OutImageFileName,'w') as f: #
        # file.require_group('FF')
        # file.create_dataset()
        f['band1']=Band1_2






