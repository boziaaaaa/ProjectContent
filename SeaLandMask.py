import numpy
import struct
from PIL import Image
def getRowColumn(MaxLon,MinLon,MaxLat,MinLat) :
    rows = 21600    #fixed row value of .dat
    columns = 43200 #fixed column value of .dat
    column_right = (MaxLon - (-180))/360.0*columns
    row_up = (90 - MaxLat)/180.0*rows
    column_left = (MinLon - (-180))/360.0*columns
    row_down = (90 - MinLat)/180.0*rows
    return int(row_up),int(row_down),int(column_left),int(column_right)

def getLandSeaMask(MaxLon,MinLon,MaxLat,MinLat,height,Width):
    row_up, row_down, column_left, column_right = getRowColumn(MaxLon, MinLon, MaxLat, MinLat)
    print row_up - row_down, column_left - column_right
    print row_up, row_down, column_left, column_right

    LandSea = []
    landSeaMask = numpy.NAN
    arsc_file = open(file, "rb")
    rows = 21600
    columns = 43200
    skip_num = (row_up - 1) * columns + (column_left - 1)
    arsc_file.seek(skip_num, 0)
    for i in range(0, row_down - row_up + 1):
        data = arsc_file.read(column_right - column_left + 1)
        hh = struct.unpack("%dB" % (column_right - column_left + 1), data)
        LandSea.append(hh)
        skip_num = columns - column_right + column_left - 1
        arsc_file.seek(skip_num, 1)

    LandSea = numpy.array(LandSea)
    img = Image.fromarray(numpy.uint8(LandSea))
    img = img.resize((Width, height))  # width , height
    print img
    # width_img = img.size[0]
    # height_img = img.size[1]
    FinalArray = numpy.zeros((height, width))
    print width, height
    for h in range(0, height):
        for w in range(0, width):
            pixel = img.getpixel((w, h))
            FinalArray[h, w] = pixel
    return FinalArray
if __name__ == "__main__":
    file = "D:\\temp_10.24.4.135_xBQ\\LAND_SGI.new"
    outputfile = "D:\\temp_10.24.4.135_xBQ\\LAND_SGI.hdf"
    MaxLon = 138
    MinLon = 104
    MaxLat = 34
    MinLat = 4
    width = 408
    height = 360

    #get landseamask according to the size of Sea temperature data
    LandSeaMask = getLandSeaMask(MaxLon, MinLon, MaxLat, MinLat, height, width)

    import h5py
    fileHandle = h5py.File(outputfile)
    fileHandle.create_dataset("dd",data = LandSeaMask)
    fileHandle.close()






