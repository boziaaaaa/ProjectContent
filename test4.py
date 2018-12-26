from netCDF4 import Dataset
import numpy
import os
def NC2DAT(inputNC,outputDAT):
    f = Dataset(inputNC)
    LAT = f.variables["LAT"][:]
    LON = f.variables["LON"][:]
    f.close()
    xTotal = 400
    yTotal = 700
    maxLon = 140
    minLon = 70
    maxLat = -15
    minLat = -55
    if len(LAT) != 0:
        if LAT[0] > 0:
            maxLat = 55
            minLat = 15
        else:
            maxLat = -15
            minLat = -55
    interval = 0.1

    # LAT = [-15.91,-15.91,-54.901,-55]
    # LON = [70.1,70.1,139.991,70]

    length = len(LAT)
    x_pixel = []
    y_pixel = []
    grid = numpy.zeros(xTotal*yTotal,dtype="i2")

    for i in range(length):
        print  LAT[i],LON[i],i
        if LAT[i] <  minLat or LAT[i] >= maxLat or LON[i] >= maxLon or LON[i] < minLon:
            continue
        for i_x in range(xTotal):
            if  LAT[i] < (maxLat - interval * i_x)  and LAT[i] >= (maxLat - interval * (i_x + 1)):
                x_pixel.append(i_x+1)
        for i_y in range(yTotal):
            if  LON[i] < (minLon + interval * (i_y + 1))  and LON[i] >= (minLon + interval * i_y):
                y_pixel.append(i_y+1)
    length_pixel = len(x_pixel)
    for i in range(length_pixel):
        index = (x_pixel[i] - 1) * yTotal + y_pixel[i]
        grid[index-1] += 1
    print x_pixel
    print y_pixel
    # import struct
    # with open(outputDAT, 'wb')as fp:
    #     # fp.write(grid.tobytes())
    #     for x in grid:
    #         a = struct.pack('B', x)
    #         fp.write(a)


if __name__=="__main__":
    # inputPath = "G:\\tiJiaoCaoLaoShi_20180829\\redo_LIO_20180626\\"
    # outputPath = "D:\\temp_10.24.189.195\\20180930\\"
    # files = os.listdir(inputPath)
    # for f in files:
    #     if "LMIF" in f and ".NC" in f:
    #         # print inputPath + f
    #         inputNC = inputPath + f
    #         print "---------------"
    #         outputDAT = outputPath + f.replace(".NC",".DAT")
    #         print inputNC
    #         print outputDAT
    #         NC2DAT(inputNC,outputDAT)

    inputPath = "G:\\tiJiaoCaoLaoShi_20180829\\redo_LIO_20180626\\FY4A-_LMI---_N_REGX_1047E_L2-_LMIF_SING_NUL_20180626160510_20180626161449_7800M_N02V1.NC"
    outputDAT = "D:\\temp_10.24.189.195\\20181018\\t.dat"
    NC2DAT(inputPath, outputDAT)



#
#
# if __name__=="__main2__":
#     # 33333333333333333333333333333333333333333333333
#     # 33333333333333333333333333333333333333333333333
#     def getluv(toplat, lat, leftlon, lon, dpp):
#         """
#         :param toplat: North-Latitude
#         :param lat:    Latitude
#         :param leftlon:West-Longitude
#         :param lon:    Longitude
#         :param dpp:    dot per degree
#         :return:
#         """
#         lat = toplat - lat
#         lon -= leftlon
#         lon %= 360
#         resulotion=1./dpp
#         u = numpy.floor_divide(lon, resulotion,dtype='f4').astype('u2')
#         v = numpy.floor_divide(lat, resulotion,dtype='f4').astype('u2')
#         return u, v

