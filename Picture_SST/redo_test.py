

import h5py
import numpy
import matplotlib.pyplot as plt
from collections import Counter
import os
inputPath = "/OUTPUTDATA/SSTOUT/SST/SST/FY3C/PROD/L2/ORBIT_PROJ/"
files = os.walk(inputPath)
for f in files:
  for inputFile in f:
    # print
    inputFile = os.path.join(inputPath,inputFile)
    print inputFile
    if ".HDF" in inputFile:
        filehandle = h5py.File(f[0]+'/'+inputFile,"r")
        data = filehandle["quality_flag"].value
        filehandle.close()
        data=data[data!=255]
        t = Counter(data.tolist())
        print t