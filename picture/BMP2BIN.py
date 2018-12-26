from PIL import Image
import numpy
import sys

def savePicture(data,outputName):
    im = Image.fromarray(data)
    im.save(outputName)
    return 0
def saveHDF(data,ouputName):
    import h5py
    f = h5py.File(ouputName)
    f.create_dataset("RGB",data=data,dtype=numpy.uint8)
    f.close()
    return 0
def JPGtoBIN(PictureFile):
    RGB = Image.open(PictureFile)
    data = numpy.array(RGB)
    XYZ = data.shape
    print data
    print data.shape
    print data.dtype
    lastString = str(data.dtype)+"_"+str(XYZ[0])+"_"+str(XYZ[1])+"_"+str(XYZ[2])+".bin"
    binFile = PictureFile.replace(".bmp",lastString)
    binFile = PictureFile.replace(".BMP",lastString)
    data.tofile(binFile)
    return 0
if __name__=="__main__":
    inputJPG = sys.argv[1]
    JPGtoBIN(inputJPG)