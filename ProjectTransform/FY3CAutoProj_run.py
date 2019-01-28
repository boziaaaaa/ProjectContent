import MySQLdb
import h5py
import os
import os.path
import numpy as Np
import sys
import xml.etree.ElementTree as ET
from DataOuter.HdfDataOuter import *
#from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *

#
# def loadLonLat():
#     minlat = 0
#     minlon = 0
#     maxlat = 0
#     maxlon = 0
#     conn = MySQLdb.connect(
#         host='localhost',
#         port=3306,
#         user='gds',
#         passwd='gds',
#         db='GDS',
#     )
#     cur = conn.cursor()
#     checkSQL = "SELECT * FROM SST_Area_Config"  # WHERE JPGfile "#> '%s'" % (1000)
#     cur.execute(checkSQL)
#     results = cur.fetchall()
#     if len(results) > 0:
#         return float(results[0][2]), float(results[0][4]), float(results[0][5]), float(results[0][3])
#     else:
#         return float(maxlat), float(minlat), float(maxlon), float(minlon)


def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    minlat = 0
    minlon = 0
    maxlat = 0
    maxlon = 0

    for projrange in root.iter('ProjRange'):
        maxlon = projrange.find('MaxLon').text
        minlon = projrange.find('MinLon').text
        maxlat = projrange.find('MaxLat').text
        minlat = projrange.find('MinLat').text

    return int(maxlat), int(minlat), int(maxlon), int(minlon)


def CheckHDF(filePath, xmlfile):
    fileHandle = h5py.File(filePath, 'a')
    groupPath = '/'
    latName = 'Geolocation/Latitude'
    lonName = 'Geolocation/Longitude'
    hdfgroup = fileHandle[groupPath]
    lat = hdfgroup[latName].value
    lon = hdfgroup[lonName].value
    lat = Np.array(lat)
    lon = Np.array(lon)

    fileHandle.close()
    lat_new = lat[Np.where(lat > -999)]
    lon_new = lon[lon > -999]
    maxLat = Np.max(lat_new)
    minLat = Np.min(lat_new)
    maxLon = Np.max(lon_new)
    minLon = Np.min(lon_new)
    print "maxLat, minLat, maxLon, minLon"
    print maxLat, minLat, maxLon, minLon

    maxLat_xml, minLat_xml, maxLon_xml, minLon_xml = parseXML(xmlfile)

    # if(maxLat < 3 or minLat > 42 or maxLon <105  or minLon > 130):
    print(minLat_xml, maxLat_xml, minLon_xml, maxLon_xml)
    if (maxLat < minLat_xml or minLat > maxLat_xml or maxLon < minLon_xml or minLon > maxLon_xml):
        return 1

    return 0

# this function only intend to find data that in range!
if __name__ == "__main__":
    inpu_sstdata_tPath = sys.argv[1]
    outputPath = sys.argv[2]

    print "Project of L1 FY3C VIRRX Begin!"
    print "input L1 file Path is : ", inpu_sstdata_tPath
    print "output L1 mosaic file Path is : ", outputPath
    date = sys.argv[3]
    xmlfile = sys.argv[4]
    geopath = sys.argv[5]
    dnflag = sys.argv[6]

    files = os.listdir(inpu_sstdata_tPath)
    print  inpu_sstdata_tPath
    i = 0;
    for file in files:
        if ".HDF" in file:
            print 'input HDF :' + file
            time = file[31:44]
            GEOfile = geopath + date + '/FY3C_VIRRX_GBAL_L1_' + time + '_GEOXX_MS.HDF'
            print(GEOfile)
            if os.path.exists(GEOfile) == False:
                print("Input GEOfile Do Not Exist:")
                print(GEOfile)
                exit(0)
            N = CheckHDF(GEOfile, xmlfile) # check which HDF is in the range of XML
            if N == 1:
                print "not in the range !!!!!!"
                continue
            command = "python /GDS/SSTWORK/ProjectTransform/FY3CAutoProj.py " + time + " " + xmlfile + " 5000 " + os.path.join(
                inpu_sstdata_tPath, file) + " " + outputPath + " " + geopath

            print command
            status = os.system(command)
            print status
            i = i + 1
    if i == 0:
        print "Wrong!!!no suitable PROJ input file!"
