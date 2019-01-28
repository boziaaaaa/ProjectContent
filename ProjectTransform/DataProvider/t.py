import h5py
import os
import os.path
import numpy as Np


def CheckHDF(filePath):
        fileHandle = h5py.File(filePath, 'a')
        groupPath = '/'
        latName = 'Geolocation/Latitude'
        lonName = 'Geolocation/Longitude'
        hdfgroup = fileHandle[groupPath]
        lat = hdfgroup[latName].value
        lon = hdfgroup[lonName].value
        lat = Np.array(lat)
        lon = Np.array(lon)

        fileHandle.close()
        lat_new = lat[Np.where(lat>-999)]
        lon_new = lon[lon>-999]
        maxLat = Np.max(lat_new)
        minLat = Np.min(lat_new)
        maxLon = Np.max(lon_new)
        minLon = Np.min(lon_new)
        print maxLat, minLat, maxLon, minLon
        #if(maxLat>42 or minLat<3 or maxLon>130 or minLon<105):
        if(maxLat < 3 or minLat > 42 or maxLon <105  or minLon > 130):
                return 1

        return 0




if __name__ == "__main__":

    inputPath = "D:/Data_Proj/FY3C_VIRRX/"
    files = os.listdir(inputPath)
    for f in files:
        if "GEOXX" in f:
            #time = "FY3C_VIRRX_GBAL_L1_20171119_0020_1000M_MS"
            str_t = inputPath+str(f)
            N = CheckHDF(str_t)
            if N == 1:
                print "no !!!!!!"
                continue
            time = f[19:32]
            print time
            commad = "D:\ProjectTransform\FY3CAutoProj.py "+time+" D:\\ProjectTransform\\FY3C_1000m_Proj.xml 1000 D:\\Data_Proj\\FY3C_VIRRX\\ D:\\Result_FY3C\\"
            status = os.system(commad)
            print status
    #D:\ProjectTransform\FY3CAutoProj.py 20171120_0255 D:\\ProjectTransform\\FY3C_1000m_Proj.xml 1000 D:\\Data_Proj\\FY3C_VIRRX\\ D:\\Result_FY3C\\


