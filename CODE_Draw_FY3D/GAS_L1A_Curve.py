# coding=utf-8
import numpy
import h5py
from matplotlib import pyplot
from matplotlib import rcParams
class GAS_L1A_Curve(object):
    def L1A_curve(self,L1a,frame):
        p = rcParams
        p["figure.subplot.hspace"] = 0.3
        f = h5py.File(L1a,'r')

        #frame = 0 ###################################################

        Bnad1 = f['Data/IGM_B4'][frame]
        Bnad2 = f['Data/IGM_O2A'][frame]
        Bnad3 = f['Data/IGM_SCO2'][frame]
        Bnad4 = f['Data/IGM_WCO2'][frame]

        ZPD_b1 = numpy.argmax(Bnad1)
        ZPD_b2 = numpy.argmax(Bnad2)
        ZPD_b3 = numpy.argmax(Bnad3)
        ZPD_b4 = numpy.argmax(Bnad4)
        #print ZPD_b1,ZPD_b2,ZPD_b3,ZPD_b4

        # ZPD_b1 = 38169
        # ZPD_b2 = 39696
        lineColor = 'r' # red##########################################
        width = 200#####################################################
        beginNumber =   ZPD_b1-width
        endNumber =     ZPD_b1+width
        beginNumber_2 = ZPD_b2-width
        endNumber_2 =   ZPD_b2+width
        beginNumber_3 = ZPD_b3-width
        endNumber_3 =   ZPD_b3+width
        beginNumber_4 = ZPD_b4-width
        endNumber_4 =   ZPD_b4+width

        dd1 = Bnad1
        dd2 = Bnad2
        dd3 = Bnad3
        dd4 = Bnad4
        pyplot.figure(2) .suptitle(L1a[12:]) # ❶ # 选择图表1
        #pyplot.title(L1a)

        pyplot.subplot(411).set_xlim(beginNumber,endNumber)
        pyplot.plot(dd1,color = lineColor,linewidth=0.5)
        pyplot.subplot(412).set_xlim(beginNumber_2,endNumber_2)
        pyplot.plot(dd2,color = lineColor,linewidth=0.5)
        pyplot.subplot(413).set_xlim(beginNumber_3,endNumber_3)
        pyplot.plot(dd3,color = lineColor,linewidth=0.5)
        pyplot.subplot(414).set_xlim(beginNumber_4,endNumber_4)
        pyplot.plot(dd4,color = lineColor,linewidth=0.5)

        L1a_png = L1a.replace(".HDF","_"+str(frame)+".pdf")
        L1a_png = L1a_png.replace("Data_GAS","Data_GAS/pdf")
        pyplot.savefig(L1a_png)

        pyplot.show()

        pyplot.close()

        f.close()

if __name__=="__main__":
    # L1a = r"D:\Data_GAS\FY3D_GASND_ORBT_1A_20160824_2211_013KM_MS.HDF"

    # L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1A_20171126_0635_013KM_MS.HDF"
    # L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1A_20171127_0449_013KM_MS.HDF"
    L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1A_20171127_0436_013KM_MS.HDF"
    GAS_L1A_Curve = GAS_L1A_Curve()
    GAS_L1A_Curve.L1A_curve(L1a,0)