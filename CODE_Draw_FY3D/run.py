# coding=utf-8
import numpy
import h5py
from matplotlib import pyplot
from matplotlib import rcParams
from GAS_L1B_Curve import GAS_L1B_Curve
from GAS_L1A_Curve import GAS_L1A_Curve
from GAS_position_singlePoint import GAS_position
def CheckCT_Angle(L1a):
    f = h5py.File(L1a, 'r')

    frame = -1  ###################################################
    index = 0
    CT_Angle = f['Geolocation/CT_Angle']
    for i in CT_Angle:
        print i
        if abs(i)<10:
            print "oh Low->",i,index
            index=index+1
            continue
        else:
            frame = index
            f.close()
            print "oh great-->return "
            return frame
    f.close()
    return frame
if __name__=="__main__":
    #L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1A_20171126_0635_013KM_MS.HDF"
    #L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1A_20171127_0449_013KM_MS.HDF"
    #L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1A_20171127_0436_013KM_MS.HDF"
    #L1a = r"D:\Data_GAS\FY3D_GASND_ORBT_1A_20171126_0822_013KM_MS.HDF"
    #L1a = r"D:\Data_GAS\FY3D_GASND_ORBT_1A_20171126_0822_013KM_MS.HDF"
    #L1a = r"D:\Data_GAS\FY3D_GASND_ORBT_1A_20171128_0137_013KM_MS.HDF"
    L1a = r"D:\\temp_10.24.171.20\FY3D_GASND_ORBT_1A_20171205_1941_013KM_MS.HDF"


    L1b = L1a.replace("_1A_","_1B_")
    # frame = CheckCT_Angle(L1a)
    # print "frame-->",frame
    # if frame == -1:
    #     print "all CT Angles are lower than 10 "
    #     import matplotlib.pyplot as plt
    #     pyplot.figure(1).suptitle("All CT Angles lower than 10 ",size=20)
    #     #plt.text( "all CT Angles are lower than 10 ")
    #     plt.show()
    #     plt.close()
    #     frame = 0
    # else:
    #     print "CT_Angle > 10,    frame: ",frame
    #     import multiprocessing
    #     def thrun(fun):
    #         def wapprer(*args,**kwargs):
    #             multiprocessing.Process(target=fun,args=args,kwargs=kwargs).start()
    #         return wapprer
    #
    #     GAS_L1A_Curve = GAS_L1A_Curve()
    #     thrun(GAS_L1A_Curve.L1A_curve)(L1a,frame)
    #
    #     GAS_L1B_Curve = GAS_L1B_Curve()
    #     thrun(GAS_L1B_Curve.L1B_curve)(L1b,frame)
    #
    #     GAS_position = GAS_position()
    #     thrun(GAS_position.GlobalPosition)(L1b,frame)


    import multiprocessing
    def thrun(fun):
        def wapprer(*args,**kwargs):
            multiprocessing.Process(target=fun,args=args,kwargs=kwargs).start()
        return wapprer
    frame = 1
    GAS_L1A_Curve = GAS_L1A_Curve()
    GAS_L1B_Curve = GAS_L1B_Curve()
    GAS_position = GAS_position()
    #frame = 201 301 501
    for i in range(0,10):
        frame = 451

        thrun(GAS_L1A_Curve.L1A_curve)(L1a,frame)

        thrun(GAS_L1B_Curve.L1B_curve)(L1b,frame)

        #thrun(GAS_position.GlobalPosition)(L1b,frame)
        #i = i+50
        break

    # @thrun
    # def aaa(bb):
    #     pass