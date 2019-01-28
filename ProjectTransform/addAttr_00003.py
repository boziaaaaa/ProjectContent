import os
import h5py
if __name__=="__main__":
    inputfile = "/GDS/OUTPUT/SST/FY3C/PROD/L2/POAD/00000/"
    files = os.listdir(inputfile)
    for f in files:
        if ".HDF" in f:
            inputHDF  = inputfile+f
            try:
                fileHandle = h5py.File(inputHDF)
                fileHandle.attrs["CenterLatitude"] = 20
                fileHandle.attrs["CenterLongitude"] = 116
                fileHandle.attrs["MaxLat"] = 30
                fileHandle.attrs["MaxLon"] = 122
                fileHandle.attrs["MinLat"] = 11
                fileHandle.attrs["MinLon"] = 110
                fileHandle.attrs["ProjString"] = "+units=m +lon_0=116 +datum=WGS84 +proj=latlong _11-30-110-122"
                fileHandle.attrs["SatelliteName"] = "FY3C"
                fileHandle.attrs["SensorName"] = "VIRR"
                fileHandle.attrs["UResolution"] = 5000
                fileHandle.attrs["VResolution"] = 5000
                fileHandle.close()
            except:
                continue

