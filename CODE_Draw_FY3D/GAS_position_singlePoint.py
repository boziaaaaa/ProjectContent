# coding=utf-8
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import h5py
import numpy as np


class GAS_position(object):
    def GlobalPosition(self,L1a,frame):
        f = h5py.File(L1a,'r')
        lon = f['Geolocation/CenterLon'].value
        lat = f['Geolocation/CenterLat'].value
        lon = lon[lon<65535]
        lat = lat[lat<65535]

        plt.figure(3)
        m = Basemap()
        #m.drawcoastlines()
        #m = Basemap(projection='lcc', resolution=None,width=8E6, height=8E6,lat_0=lat[0], lon_0=lon[0]) #lcc投影图 平面图
        m = Basemap(projection='ortho', resolution=None, lat_0=lat[0], lon_0=lon[0])
        m.drawmeridians(np.arange(0,360,30),color='y')#格网
        m.drawparallels(np.arange(-90,90,30),color='y')#格网
        m.bluemarble(scale=1)

        Title = L1a[12:]
        index = 0
        for i in lon:
            x, y = m(lon[index],lat[index])
            if index == frame:
                plt.plot(x, y, 'ok', color='y', markersize=3)
            else:
                plt.plot(x, y, 'ok',color = 'r' , markersize=3)
            index=index+1
        plt.title(Title)
        plt.show()
        plt.close()
        f.close()
if __name__=="__main__":
    L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1B_20171127_0436_013KM_MS.HDF"
    GAS_position = GAS_position()
    GAS_position.GlobalPosition(L1a)