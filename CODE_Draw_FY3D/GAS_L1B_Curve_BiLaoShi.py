# coding=utf-8
import numpy
import h5py
from matplotlib import pyplot
from matplotlib import rcParams
import re
class GAS_L1B_Curve(object):
    def makex(self,start, incr, cnt):
        return [start + n * incr for n in xrange(cnt)]
    def L1B_curve(self,L1b,frame):
        p = rcParams
        p["figure.subplot.hspace"] = 0.39
        #p["axes.labelsize"] = 1
        f = h5py.File(L1b, 'r')
        lineColor = 'r'  # red##########################################

        Bnad1 = f['Data/Radiance_B1'][frame]
        Bnad2 = f['Data/Radiance_B2'][frame]
        Bnad3 = f['Data/Radiance_B3'][frame]
        Bnad4 = f['Data/Radiance_B4'][frame]

        waveNumber_1 = f['Data/BeginningWn_B1'].value[0]

        incr_1 =f['Data/Interval_B1'].value[0]


        ZPD_b1 = numpy.argmax(Bnad1)
        ZPD_b2 = numpy.argmax(Bnad2)
        ZPD_b3 = numpy.argmax(Bnad3)
        ZPD_b4 = numpy.argmax(Bnad4)

        Time = re.findall(r"\d{8}_\d{4}",L1b)

        pyplot.figure(2) .suptitle("GAS Spectrogram 2017.12.05-19:41(UTC)",size=15) # ❶ # 选择图表1

        #pyplot.figure(1).suptitle(L1b[12:])  # ❶ # 选择图表1
        pyplot.subplot(111)  # .set_xticks(waveNumber_1,waveNumber_1,799)
        pyplot.plot(self.makex(waveNumber_1, incr_1, Bnad1.size),
                    Bnad1, color=lineColor, linewidth=0.5)

        pyplot.xticks(fontsize = 13)
        pyplot.yticks(fontsize = 13)
        #pyplot.text(12910, 5.3/10000000, "W/cm2/sr/cm-1", fontsize=10)
        #pyplot.text(13360, -1.9/100000000, "cm-1", fontsize=10)
        pyplot.xlabel("wavenumber($cm^{-1}$)",fontsize=14)
        pyplot.ylabel("radiance(W/c$m^2$/sr/c$m^{-1}$)",fontsize=14)



        L1a_png = L1b.replace(".HDF","_"+str(frame)+".pdf")
        L1a_png = L1a_png.replace("Data_GAS","Data_GAS/pdf")
        L1a_png = "D:\\Data_GAS\\yuan\\Spectrogram.png"
        pyplot.savefig(L1a_png)
        pyplot.show()
        pyplot.close()

        f.close()

if __name__=="__main__":
    # p["figure.top"] = 0.9

    L1b = r"D:\Data_GAS\FY3D_GASGL_ORBT_1B_20171127_0436_013KM_MS.HDF"
    t = GAS_L1B_Curve()
    t.L1B_curve(L1b,0)