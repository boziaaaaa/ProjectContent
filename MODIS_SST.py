from netCDF4 import Dataset
import h5py
import numpy
import os
from scipy import interpolate
from PIL import Image
def Interpolate(sst,height, width):
        img = Image.fromarray(numpy.int16(sst))
        img = img.resize((width, height))  # width , height
        result = numpy.zeros((height, width))
        print "1111111111111"
        print width, height
        for h in range(0, height):
            for w in range(0, width):
                pixel = img.getpixel((w, h))
                result[h, w] = pixel
        print "222222222222"

        return result

def NCtoHDF(inputFile,outputFile):
    fileHandle = Dataset(inputFile)
    sst = fileHandle["analysed_sst"][:]
    lat = fileHandle["lat"][:]

    lon = fileHandle["lon"][:]
    fileHandle.close()
    sst = numpy.array(sst)
    temp,height,width = sst.shape
    sst = sst.reshape(height,width)

    lat = numpy.array(lat)
    lat = numpy.tile(lat,width)
    lat = lat.reshape(width,height)
    lat = numpy.transpose(lat)
    lon = numpy.array(lon)
    lon = numpy.tile(lon,height)
    lon = lon.reshape(height,width)
    sst = numpy.array(sst)

    sst = Interpolate(sst, height*4, width*4)
    lat = Interpolate(lat, height*4, width*4)
    lon = Interpolate(lon, height*4, width*4)

    fileHandle = h5py.File(outputFile)
    fileHandle.create_dataset("sea_surface_temperature",data=sst,dtype=numpy.int16)
    fileHandle.create_dataset("latitude",data=lat)
    fileHandle.create_dataset("longitude",data=lon)
    fileHandle.close()
    return 0
# if __name__=="__main__":
#     inputFile = "D:\\temp_10.24.4.135_xBQ\\20170424120000-NCEI-L4_GHRSST-SSTblend-AVHRR_OI-GLOB-v02.0-fv02.0.nc"
#     outputFile = inputFile.replace(".nc",".hdf")
#     if os.path.exists(outputFile) == True:
#         os.system("rm "+outputFile)
#     NCtoHDF(inputFile,outputFile)
