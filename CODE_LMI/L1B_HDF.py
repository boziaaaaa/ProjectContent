import numpy
from netCDF4 import Dataset
import h5py
NC_03 = "D:/temp_10.24.189.195/20180726_2/old/FY4A-_LMI---" +\
        "_N_REGX_1047E_L1B_EVT-_SING_NUL_20180905172912_20180905173449_7800M_N03V1.HDF"
# f = Dataset(NC_03)
# f.close(D:/temp_10.24.189.195/20180726_2/FY4A-_LMI---_N_REGX_1047E_L1B_EVT-_SING_NUL_20180905172912_20180905173449_7800M_N02V1.txt)

file_txt = NC_03.replace(".HDF",".txt")
fp_txt = open(file_txt,"w")
f = h5py.File(NC_03)
data = f["VData"]

index = 0
for i in data:
    data_temp = data[i].value
    for d in data_temp:
        # print d
        if d[0]>0 :
            print d
            index = index + 1
        # fp_txt.write(str(d))
        # fp_txt.write("\n")
print len(data)
print index

f.close()
fp_txt.close()