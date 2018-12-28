import h5py
import numpy
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import collections
# def del_no_ocean(position, COLUMNS, ROWS, root_dir):
#     # position:lon,lat(2*1)
#     column = int((position[0, 0] - (-180)) / 360.0 * COLUMNS)
#     row = int((90 - position[1, 0]) / 180.0 * ROWS)
#     with h5py.File(root_dir + 'LAND_SGI.HDF') as ls:
#         ls_value = ls['LandSeaMask'][row, column]
#         if ls_value != 6 and ls_value != 7 and ls_value != 0:
#             return True

def CheckSeaOrNot(lat,lon):
    mp = Basemap(projection='cyl',llcrnrlat=0,urcrnrlat=60,llcrnrlon=20,urcrnrlon=90)
    mp.drawcoastlines()
    plt.scatter(lat,lon,s=10)
    plt.show()
def CheackLandSeaMaskHDF(LandSeaMaskHDF):
    with h5py.File(LandSeaMaskHDF) as f_HDF:
        data = numpy.array(f_HDF['LandSeaMask'].value)
    print numpy.max(data)
    # data = data.tolist()
    # count = collections.Counter(data)
    # print count
    # plt.hist(data)
    # plt.show()
if __name__=="__main__":
    minLat = 0
    maxLat = 60
    minLon = 20
    maxLon = 90
    lat =[47.692333,46.25683 ,45.66151 ]
    lon = [29.176577,42.132828,47.89882]
    # CheckSeaOrNot(lat,lon)
    LandSeaMaskHDF = r"D:\Data_LandSeaMask\LandSeaMask.HDF"
    CheackLandSeaMaskHDF(LandSeaMaskHDF)
