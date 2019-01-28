import os
import h5py
if __name__=="__main__":
    inputfile = "/GDS/OUTPUT/SST/FY3C/PROD/L2/POAD/00000/"
    files = os.listdir(inputfile)
    for f in files:
        if ".HDF" in f and "201703" in f:
            inputHDF  = inputfile+f
            try:
                fileHandle = h5py.File(inputHDF)
                fileHandle.attrs["CenterLatitude"] = 19
                fileHandle.attrs["CenterLongitude"] = 122
                fileHandle.attrs["MaxLat"] = 34
                fileHandle.attrs["MaxLon"] = 140
                fileHandle.attrs["MinLat"] = 4
                fileHandle.attrs["MinLon"] = 104
                fileHandle.attrs["ProjString"] = "+units=m +lon_0=122 +datum=WGS84 +proj=latlong _4-34-104-140"
                fileHandle.attrs["SatelliteName"] = "FY3C"
                fileHandle.attrs["SensorName"] = "VIRR"
                fileHandle.attrs["UResolution"] = 5000
                fileHandle.attrs["VResolution"] = 5000
                fileHandle.close()
            except:
                continue
