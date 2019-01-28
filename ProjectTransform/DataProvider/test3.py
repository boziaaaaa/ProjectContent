# -*- coding:utf-8 -*-
import h5py
import os
import numpy
import struct
import matplotlib.pyplot as plt
from cStringIO import StringIO

def stat(x):
    tmp = (x > 50).astype('u4')
    tmp += x > 100
    tmp += x > 150
    tmp += x > 200
    ret = numpy.bincount(tmp)
    ret = numpy.array(ret,dtype='f4') / numpy.sum(ret)
    # return ret, ret.size
    return ret
def stat_cal(x):
    tmp = (x > 500).astype('u4')
    tmp += x > 1000
    tmp += x > 1500
    tmp += x > 2000
    ret = numpy.bincount(tmp)
    ret = numpy.array(ret,dtype='f4') / numpy.sum(ret)
    # return ret, ret.size
    return ret
def ReadHDF(filePath):
    #print >> sys.stderr, filePath
    HDFfile = h5py.File(filePath)
    VData = HDFfile.get('VData')
    radiance = []
    bg = []
    X_pixel = []
    Y_pixel = []
    for data in VData.values():
        howMany = len(data['Event_radiance'])
        for i in range(howMany):
          radiance.append(data['Event_radiance'])
          bg.append(data['Bg_radiance'])
          X_pixel.append(data['X_pixel'])
          Y_pixel.append(data['Y_pixel'])

    index = X_pixel * 600 + Y_pixel
    data = radiance + bg
    data_cal = (data - b[index])/a[index]
    # radiance = numpy.array(radiance)
    # cnt, i = stat(radiance)
    data_cal = numpy.array(data_cal)
    cnt = stat_cal(data_cal)
    #print cnt
    return cnt


def Image(filePaht,titleName,Yname,data):
    plt.plot(data)
    plt.title(titleName)
    plt.xlabel("time(1 min)")
    plt.ylabel(Yname)
    plt.savefig(filePaht)
    plt.close()


def ReadDat(datPath):
    f = open(datPath, "rb")
    dat = f.read()
    data_f = struct.unpack("240000f", dat)
    f.close()
    return data_f

aPath = "D:/temp_10.24.189.195/ab/a.dat"
bPath = "D:/temp_10.24.189.195/ab/b.dat"
a = ReadDat(aPath)
import sys
b = ReadDat(bPath)
if __name__ == "__main__":
    import glob
    temp = glob.glob("D:/temp_10.24.189.195/data_201709/*2017092300*.HDF")

    from multiprocessing import Pool
    pp=Pool(4)
    results = pp.map(ReadHDF,temp)
    pp.close()
    pp.join()
    x = numpy.zeros((len(results), 5), 'file')
    for i, j in enumerate(results):
        x[i, :j.size] = j
    print results
    print x
    results=x
    imageFilePath = "D:/temp_10.24.189.195/txt_test/0_500.png"
    titleName = "0-500 percent curve"
    Yname = "percent"
    Image(imageFilePath,titleName,Yname,results[:,0])
    imageFilePath = imageFilePath.replace("0_500.png","501-1000.png")
    titleName = "501-1000 percent curve"
    Yname = "percent"
    Image(imageFilePath,titleName,Yname,results[:,1])
    imageFilePath = imageFilePath.replace("501-1000.png","1001-1500.png")
    titleName = "1001-1500 percent curve"
    Yname = "percent"
    Image(imageFilePath,titleName,Yname,results[:,2])
    imageFilePath = imageFilePath.replace("1001-1500","1501-2000.png")
    titleName = "1501-2000 percent curve"
    Yname = "percent"
    Image(imageFilePath,titleName,Yname,results[:,3])
    imageFilePath = imageFilePath.replace("1501-2000.png","2000.png")
    titleName = ">2000 percent curve"
    Yname = "percent"
    Image(imageFilePath,titleName,Yname,results[:,4])