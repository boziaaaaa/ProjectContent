import h5py
import os
import numpy
from PIL import Image
def CheckHDF(filePath, maxLat_xml, minLat_xml, maxLon_xml, minLon_xml):
    fileHandle = h5py.File(filePath, 'a')
    groupPath = '/'
    latName = 'Latitude'
    lonName = 'Longitude'
    hdfgroup = fileHandle[groupPath]
    lat = hdfgroup[latName].value
    lon = hdfgroup[lonName].value
    lat = numpy.array(lat)
    lon = numpy.array(lon)

    fileHandle.close()
    lat_new = lat[numpy.where(lat > -999)]
    lon_new = lon[lon > -999]
    maxLat = numpy.max(lat_new)
    minLat = numpy.min(lat_new)
    maxLon = numpy.max(lon_new)
    minLon = numpy.min(lon_new)
    print "maxLat, minLat, maxLon, minLon"
    print maxLat, minLat, maxLon, minLon

    print(minLat_xml, maxLat_xml, minLon_xml, maxLon_xml)
    if (maxLat < minLat_xml or minLat > maxLat_xml or maxLon < minLon_xml or minLon > maxLon_xml):
        return 1

    return 0

if __name__ == "__main__":
    minLat = 0
    maxLat = 60
    minLon = 100
    maxLon = 140
    # inumpyutL1Path = "/OUTPUTDATA/HABOUT/FY3B/PROD/WATERCOLOR/ORBT/OCC/20130401/"
    inumpyutL1Path = "/OUTPUTDATA/HABOUT/FY3B/PROD/WATERCOLOR/ORBT_PROJ/20130401/"
    inumpyutL1Path = "/OUTPUTDATA/HABOUT/FY3B/PROD/WATERCOLOR/POAD/"
    files = os.listdir(inumpyutL1Path)
    print files
    for file in files:
        if ".HDF" in file and "201304" in file:
            L1file = inumpyutL1Path + file
            print L1file

            fileHandle = h5py.File(L1file)
            data = fileHandle["Ocean_Rw_443"].value
            fileHandle.close()
            print data[data<32767]




            # mask = data <32767
            # mask &= data > 0
            # try:
            #     minValue = min(data[mask])
            #     maxValue = max(data[mask])
            # except:
            #     print "exit!!\n"
            #     continue
            #
            # print data
            # print data.shape
            # data[data==32767] = 155
            # data = (data-minValue)
            # data = data/float(maxValue - minValue)*255
            # img = Image.fromarray(data)
            # img = img.convert("RGB")
            #
            # img.save(L1file.replace(".HDF",".jpg"))

