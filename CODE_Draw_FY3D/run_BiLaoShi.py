# coding=utf-8
import numpy
import h5py
from matplotlib import pyplot
from matplotlib import rcParams
from GAS_L1B_Curve_BiLaoShi import GAS_L1B_Curve
from GAS_L1A_Curve_BiLaoShi import GAS_L1A_Curve
from GAS_position_singlePoint import GAS_position

if __name__=="__main__":
    L1a = r"D:\\temp_10.24.171.20\FY3D_GASND_ORBT_1A_20171205_1941_013KM_MS.HDF"


    L1b = L1a.replace("_1A_","_1B_")

    import multiprocessing
    def thrun(fun):
        def wapprer(*args,**kwargs):
            multiprocessing.Process(target=fun,args=args,kwargs=kwargs).start()
        return wapprer
    frame = 1
    GAS_L1A_Curve = GAS_L1A_Curve()
    GAS_L1B_Curve = GAS_L1B_Curve()
    #GAS_position = GAS_position()
    #frame = 201 301 501 451
    frame = 451

    thrun(GAS_L1A_Curve.L1A_curve)(L1a,frame)

    thrun(GAS_L1B_Curve.L1B_curve)(L1b,frame)



