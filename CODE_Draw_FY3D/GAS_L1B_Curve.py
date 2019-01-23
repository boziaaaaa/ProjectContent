# coding=utf-8
import numpy
import h5py
from matplotlib import pyplot
from matplotlib import rcParams

class GAS_L1B_Curve(object):
    def makex(self,start, incr, cnt):
        return [start + n * incr for n in xrange(cnt)]
    def L1B_curve(self,L1b,frame):
        p = rcParams
        p["figure.subplot.hspace"] = 0.39

        f = h5py.File(L1b, 'r')
        lineColor = 'r'  # red##########################################

        #frame = 0  ###################################################

        Bnad1 = f['Data/Radiance_B1'][frame]
        Bnad2 = f['Data/Radiance_B2'][frame]
        Bnad3 = f['Data/Radiance_B3'][frame]
        Bnad4 = f['Data/Radiance_B4'][frame]

        waveNumber_1 = f['Data/BeginningWn_B1'].value[0]
        waveNumber_2 = f['Data/BeginningWn_B2'].value[0]
        waveNumber_3 = f['Data/BeginningWn_B3'].value[0]
        waveNumber_4 = f['Data/BeginningWn_B4'].value[0]

        incr_1 =f['Data/Interval_B1'].value[0]
        incr_2 = f['Data/Interval_B2'].value[0]
        incr_3 = f['Data/Interval_B3'].value[0]
        incr_4 = f['Data/Interval_B4'].value[0]

        #print waveNumber_1, waveNumber_2, waveNumber_3, waveNumber_4

        ZPD_b1 = numpy.argmax(Bnad1)
        ZPD_b2 = numpy.argmax(Bnad2)
        ZPD_b3 = numpy.argmax(Bnad3)
        ZPD_b4 = numpy.argmax(Bnad4)
        #print ZPD_b1, ZPD_b2, ZPD_b3, ZPD_b4
        pyplot.figure(1).suptitle(str(frame))  # ❶ # 选择图表1

        #pyplot.figure(1).suptitle(L1b[12:])  # ❶ # 选择图表1
        pyplot.subplot(411)  # .set_xticks(waveNumber_1,waveNumber_1,799)
        pyplot.plot(self.makex(waveNumber_1, incr_1, Bnad1.size),
                    Bnad1, color=lineColor, linewidth=0.2)
        pyplot.subplot(
            412)  # .set_xticklabels( [0,1,2,3,4,5,6],(0, waveNumber_2,0,0,(waveNumber_2+799/2),0,0,waveNumber_2+799))
        pyplot.plot(self.makex(waveNumber_2, incr_2, Bnad2.size),
                    Bnad2, color=lineColor, linewidth=0.2)
        pyplot.subplot(413)  # 在图表2中创建子图1
        pyplot.plot(self.makex(waveNumber_3, incr_3, Bnad3.size),
                    Bnad3, color=lineColor, linewidth=0.2)
        # ax.text(0.5,0.5,'AAA')
        pyplot.subplot(414)  # 在图表2中创建子图1
        # print makex(waveNumber_4, incr_4, Bnad4.size)
        pyplot.plot(self.makex(waveNumber_4, incr_4, Bnad4.size),
                    Bnad4, color=lineColor, linewidth=0.2)
        #L1b_png = L1b.replace("HDF", "png")
        #pyplot.savefig(L1b_png)
        L1a_png = L1b.replace(".HDF","_"+str(frame)+".pdf")
        L1a_png = L1a_png.replace("Data_GAS","Data_GAS/pdf")
        pyplot.savefig(L1a_png)
        pyplot.show()
        pyplot.close()

        f.close()

if __name__=="__main__":
    # p["figure.top"] = 0.9
    # L1a = r"D:\Data_GAS\FY3D_GASND_ORBT_1A_20160824_2211_013KM_MS.HDF"
    # L1b = r"D:\Data_GAS\FY3D_GASGL_ORBT_1B_20171126_0635_013KM_MS.HDF"
    # L1b = r"D:\Data_GAS\FY3D_GASGL_ORBT_1B_20171127_0449_013KM_MS.HDF"
    L1b = r"D:\Data_GAS\FY3D_GASGL_ORBT_1B_20171127_0436_013KM_MS.HDF"
    t = GAS_L1B_Curve()
    t.L1B_curve(L1b,0)