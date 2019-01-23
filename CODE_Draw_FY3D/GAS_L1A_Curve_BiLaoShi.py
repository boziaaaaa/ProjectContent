# coding=utf-8
import numpy
import h5py
from matplotlib import pyplot
from matplotlib import rcParams
import re

class GAS_L1A_Curve(object):
    def L1A_curve(self,L1a,frame):
        p = rcParams
        #p["figure.subplot.hspace"] = 0.3
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

        Time = re.findall(r"\d{8}_\d{4}",L1a)
        print Time
        pyplot.figure(2) .suptitle("GAS Interferogram 2017.12.05-19:41(UTC)",size=15) # ❶ # 选择图表1

        pyplot.subplot(111).set_xlim(beginNumber,endNumber)
        pyplot.plot(dd1,color = lineColor,linewidth=0.5)
        #pyplot.text(39967, 0, "cm-1", fontsize=10)
        pyplot.xticks(fontsize = 13)
        pyplot.yticks(fontsize = 13)


        L1a_png = L1a.replace(".HDF","_"+str(frame)+".pdf")
        L1a_png = L1a_png.replace("Data_GAS","Data_GAS/pdf")
        #L1a_png = L1a.replace(".HDF",".png")
        #pyplot.savefig(L1a_png)
        L1a_png = "D:\\Data_GAS\\yuan\\Interferogram.png"
        pyplot.savefig(L1a_png)
        pyplot.show()

        pyplot.close()

        f.close()

if __name__=="__main__":

    L1a = r"D:\Data_GAS\FY3D_GASGL_ORBT_1A_20171127_0436_013KM_MS.HDF"
    GAS_L1A_Curve = GAS_L1A_Curve()
    GAS_L1A_Curve.L1A_curve(L1a,0)