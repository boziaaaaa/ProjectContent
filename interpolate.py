#coding=cp936
import numpy as np
import h5py
import math
from PIL import Image
def readHDF(inputFile,datasetName):
    with h5py.File(inputFile,'r') as f:
        data =f[datasetName].value
    return data
def outputHDF(outputFile,data_new):
    with h5py.File(outputFile,'w') as f:
        f.create_dataset("test",data=data_new)
def Interpolate(data,resolution_original,resolution_destiny,interpolate_method):
    shape_original = data.shape
    ratio = resolution_original/resolution_destiny
    shape_desity = (shape_original[0] * ratio,shape_original[1] * ratio)
    img = Image.fromarray(data)
    if interpolate_method == 'NEAREST':
        method = Image.NEAREST
    elif interpolate_method == 'BILINEAR':
        method = Image.BILINEAR
    elif interpolate_method == 'BICUBIC':
        method = Image.BICUBIC
    znew = img.resize(shape_desity,resample=method)
    znew = np.array(znew)
    return znew
if __name__=="__main__":
    inputFile = r"D:\temp_10.24.4.116\ProjectTransform\FY4A-_AGRI--_N_DISK_1047E_L2-_PRD-_MULT_GLL_20181211070000_20181211071459_4000M_VPRJ5.HDF"
    outputFile = r"D:\temp_10.24.4.116\ProjectTransform\test_new.hdf"
    resolution_original = 4000
    resolution_destiny = 2000
    interpolate_method = 'NEAREST'# 'BILINEAR'  'BICUBIC'
    # interpolate_method = 'BILINEAR'
    # interpolate_method = 'BICUBIC'
    datasetName = "SunZenith"
    data = readHDF(inputFile,datasetName)
    print data.shape
    data_new = Interpolate(data,resolution_original,resolution_destiny,interpolate_method)#begin interpolate
    print data_new.shape
    # outputHDF(outputFile,data_new)
