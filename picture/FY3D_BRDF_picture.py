# coding=utf8
# import pyproj
# import numpy
# import matplotlib.pyplot as plt
# from PIL import Image
# import h5py
# import math
# from cStringIO import StringIO
# from mpl_toolkits.basemap import Basemap
# def readLatLongFile(inputLatLong):
#     latlon = numpy.fromfile(inputLatLong,">f4")
#     widthAndHeight = int(math.sqrt(len(latlon)/2))
#     lat = latlon[len(latlon)/2:]
#     lon = latlon[:len(latlon)/2]
#     return lat[::10],lon[::10]
# def readBandFile(inputBandFile,bandNames):
#     fHandle = h5py.File(inputLatLong,"r")
#     print fHandle
#     fHandle.close()
# def proj(lat,lon):
#     pass
# if __name__ == "__main__":
#     inputBandFile = r"D:\CODE_dust_ChenLin\inputdata数据\FY2E\FY2E_FDI_ALL_NOM_20100319_1400.hdf"
#     inputLatLong = "D:\CODE_dust_ChenLin\inputdata数据\FY2_latLon\FY2E_IJToLatLon.NOM"
#     outputBandFile = r"C:\Users\bozi\Desktop\test\FY2E_FDI_ALL_NOM_20100319_1400_test.hdf"
#     lat,lon = readLatLongFile(inputLatLong)
#     print lat[lat<300]
#     print lon[lon<300]
#     fig = plt.figure(figsize=(7.2,3.6))
#     plt.axes([0, 0, 1, 1]
#              , frameon=False)
#     map = Basemap(llcrnrlon=-180,
#                   llcrnrlat=-90,
#                   urcrnrlon=180,
#                   # urcrnrlat=90,
#                   resolution='c', projection='cyl', lat_0=0, lon_0=0,)
#     x,y = map(lon,lat)
#     map.scatter(x,y,marker = ',',s=1)
#     data = numpy.asarray(plt)
#     buffer_tmp = StringIO()
#     # plt.box()
#     # map.drawcoastlines()
#     # plt.show()
#     plt.savefig(buffer_tmp,format = 'png',dpi=200)
#     data = Image.open(buffer_tmp)
#     data = numpy.asarray(data)
#     Index = data[:,:,0] == 255
#     Index &=data[:,:,1] == 255
#     Index &=data[:,:,2] == 255
#     Index_out = numpy.zeros(Index.shape)
#     Index_out[Index == False] = 1
#     with h5py.File(outputBandFile,"w") as f_out:
#         f_out.create_dataset("test",data = Index_out)

# -*- coding: utf-8 -*-
"""
演示二维插值。
"""
import numpy
import matplotlib.pyplot as plt

def getBandN(inputFile,year):
    bandN = [[],[],[],[],[],[],[]]
    flag = 0
    for day in range(365):
        with open(inputFile,'r') as f:
            lines = f.readlines()
            for l in lines:
                if year+str(day+1).zfill(3) in l:
                    b1 = l.split()
                    if len(b1)<8:
                        flag = 0
                        break
                    else:
                        flag = 1
                        break
                else:
                    flag = 0
        for j in range(7):
            if flag == 1:
                b1_tmp = float(b1[j + 1])
                bandN[j].append(float(b1_tmp))
            else:
                bandN[j].append(0)
    bandN = numpy.asarray(bandN)
    bandN[bandN>32] = 1
    return bandN

def plotBandN(bandAll,year,outputFile):
    plt.figure(figsize=(30, 80))
    plt.ylim([0,1])
    plt.xlim([1,365])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # plt.title(unicode(year)+u"年甘肃敦煌BRDF")
    plt.title(unicode(year)+u"年Libya4BRDF")

    plt.text(1.1,0.9,u"值为0表示缺失数据\n值为1表示填充值32767")
    plt.ylabel("Reflectance")
    plt.xlabel("DSL")
    colors = ['black','red','blue','fuchsia','g','midnightblue','darkorchid']
    markers = ['s','o','^','^','D','<','>']
    pN = plt.plot()
    pN = [pN,pN,pN,pN,pN,pN,pN]
    note = ['645nm','859nm','470nm','555nm','1240nm','1640nm','2130nm']
    for i in range(7):
        bandN = bandAll[i]
        pN[i] = plt.plot(bandN,color = colors[i],linestyle=' ',marker =markers[i],markersize=5,label = note[i])
    plt.legend(loc='upper right')
    plt.show()
    # plt.savefig(outputFile,dpi=100)
    plt.close()

if __name__ == "__main__":
    # year = '2017'
    # inputFile = r"C:\Users\bozi\Desktop\test\BRDF_test_"+year+".txt"
    # outputFile = r"C:\Users\bozi\Desktop\test\BRDF_test_"+year+".png"
    # bandN_2017 = getBandN(inputFile,year)
    # plotBandN(bandN_2017,year,outputFile)

    year = '2018'
    inputFile = r"C:\Users\bozi\Desktop\test\BRDF_test_Libya4_"+year+".txt"
    outputFile = r"C:\Users\bozi\Desktop\test\BRDF_test_"+year+".png"
    bandN_2018 = getBandN(inputFile,year)
    plotBandN(bandN_2018,year,outputFile)
