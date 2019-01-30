#-*-coding:utf-8-*-
import seaborn as sns
import pandas as pd
import h5py
import matplotlib.pyplot as plt
class struct_LMI():
    def __init__(self):
        self.X_pixel = []
        self.Y_pixel = []
        self.lat = []
        self.lon = []
        self.rad = []
        self.rad_bg = []

def ReadHDF(inputHDF,LMI):
    with h5py.File(file) as f:
        keys = f["VData"].keys()
        for key in keys:
            data = f["VData"][key].value
            for i_data in range(len(data)):
                LMI.rad.append(data[i_data][4])
                LMI.rad_bg.append(data[i_data][5])
    return LMI

def Sns(LMI):
    fig = plt.figure()
    sns.distplot(LMI.rad)
    sns.distplot(LMI.rad_bg)
    plt.show()
if __name__=="__main__":
    file = r"D:\temp_10.24.189.195\20190130\FY4A-_LMI---_N_REGX_1047E_L1B_EVT-_SING_NUL_20190129170510_20190129171411_7800M_N02V1.HDF"
    LMI = struct_LMI()
    LMI = ReadHDF(file,LMI)
    Sns(LMI)
