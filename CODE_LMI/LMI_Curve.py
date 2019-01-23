# -*- coding:utf-8 -*-
import h5py
import numpy
import struct
import matplotlib.pyplot as plt


def ReadHDF(filePath):
    print >> sys.stderr, filePath
    with h5py.File(filePath) as HDFfile:
      VData = HDFfile.get('VData')
      radiance = []
      data_cal = []

      for data in VData.values():
          howMany = len(data['Event_radiance'])
          for i in range(howMany):
            r = data['Event_radiance'][i]
            X_pixel = data['X_pixel'][i]
            Y_pixel = data['Y_pixel'][i]
            bg = data['Bg_radiance'][i]
            index = X_pixel * 600 + Y_pixel
            c = (r+bg - b[index])/a[index]
            data_cal.append(c)
            radiance.append(r)
    radiance = numpy.array(radiance)
    data_cal = numpy.array(data_cal)
    # return stat(radiance)
    return numpy.array(data_cal)

def Image(filePaht,titleName,Yname,data):
    temp = []
    for i in data:
        temp.extend(list(i))
    plt.plot(temp)
    plt.title(titleName)
    plt.savefig(filePaht)
    plt.close()
def ReadDat(datPath):
    f = open(datPath, "rb")
    dat = f.read()
    data_f = struct.unpack("240000f", dat)
    f.close()
    return data_f

abInpputPath = "D:/temp_10.24.189.195/ab/"
aPath = abInpputPath + "a.dat"
bPath = abInpputPath + "b.dat"
a = ReadDat(aPath)
import sys
b = ReadDat(bPath)
if __name__ == "__main__":   # after after after
    import glob
    import datetime
    timeBegin = datetime.datetime.now()
    temp = glob.glob("D:/temp_10.24.189.195/L1B/*.HDF")

    from multiprocessing import Pool
    pp=Pool(4)
    results = pp.map(ReadHDF,temp)
    pp.close()
    pp.join()

    results = numpy.array(results)
    print results

    imageFilePath = "D:/temp_10.24.189.195/bbbbbbbbbbbb.png"
    titleName = "Curve"
    Yname = "Radiance"
    Image(imageFilePath,titleName,Yname,results)

    timeEnd = datetime.datetime.now()
    tmeCost = timeEnd - timeBegin
    print tmeCost
