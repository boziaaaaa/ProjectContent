# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy
import h5py
from PIL import Image
import pandas
import os
import math
import struct

def getLandSeaMask_singlePoint(inputDAT,outputHDF):
    rows = 21600
    columns = 43200
    arsc_file = open(inputDAT, "rb")
    with h5py.File(outputHDF,"w") as f_HDF:
        LandSeaMask= f_HDF.create_dataset("LandSeaMask", shape=(rows, columns), dtype="i1")
        for i in xrange(0,rows):
            LandSeaMask[i:i+1,:] = numpy.fromfile(arsc_file,dtype='i1',count=columns)#.reshape(-1,columns)

def writeHDF(dataset,datasetName,outputHDF):
    with h5py.File(outputHDF,"w") as f_HDF:
        f_HDF.create_dataset(datasetName,data=dataset)

if __name__=="__main__":
    inputDAT = "D:\\temp_10.24.4.135_xBQ\\useless\\LAND_SGI.new" # land sea mask file
    outputHDF = "D:\\temp_10.24.4.135_xBQ\\useless\\LAND_SGI.HDF"
    getLandSeaMask_singlePoint(inputDAT,outputHDF)
