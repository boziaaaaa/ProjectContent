# coding=utf8
import re
import numpy
import matplotlib.pyplot as plt

def txtAll2txtEach():
    station = ["Dunhuang",
              "Libya1",
              "Libya4",
              "Arabia2",
              "Lanai",
              "Algeria5",
              "Sonora",
              "Algeria3",
              "Mauritania2"]

    inputTXT = r"D:\temp_10.24.34.219\useless\BRDF_2019_all.txt"
    for Index in range(9):
        # Index = 9
        outTXT = r"D:\temp_10.24.34.219\useless\BRDF_2019_"+station[Index]+".txt"
        f_out = open(outTXT,"w")
        with open(inputTXT,"r") as f:
            lines = f.readlines()
            for line in lines:
                line = re.split(" |,",line)
                line_new = []
                for num in line:
                    if num:
                        line_new.append(num)
                station1 = []
                station1.append(line_new[0])
                try:
                    for i in range(7):
                        station1.append(line_new[i*9+1+Index])
                except:
                    continue
                print station1
                for j in station1:
                    f_out.write(j)
                    f_out.write("   ")
                f_out.write("\n")
        f_out.close()

def getBandN(inputFile,year):
    bandN = [[],[],[],[],[],[],[]]
    flag = 0
    for day in range(365):
        with open(inputFile,'r') as f:
            lines = f.readlines()
            for l in lines:
                if year+str(day+1).zfill(3) in l:
                    b1 = l.split()
                    if len(b1)<8:
                        flag = 0
                        break
                    else:
                        flag = 1
                        break
                else:
                    flag = 0
        for j in range(7):
            if flag == 1:
                b1_tmp = float(b1[j + 1])
                bandN[j].append(float(b1_tmp))
            else:
                bandN[j].append(0)
    bandN = numpy.asarray(bandN)
    bandN[bandN>32] = 1
    return bandN

def plotBandN(bandAll,year,outputFile,station):
    plt.figure(figsize=(15, 7))
    plt.ylim([0,1])
    plt.xlim([1,365])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title(unicode(year)+u"年"+station+"BRDF")
    plt.text(1.1,0.9,u"值为0表示缺失数据\n值为1表示填充值32767")
    plt.ylabel("Reflectance")
    plt.xlabel("DSL")
    colors = ['black','red','blue','fuchsia','g','midnightblue','darkorchid']
    markers = ['s','o','^','^','D','<','>']
    pN = plt.plot()
    pN = [pN,pN,pN,pN,pN,pN,pN]
    note = ['645nm','859nm','470nm','555nm','1240nm','1640nm','2130nm']
    for i in range(7):
        bandN = bandAll[i]
        pN[i] = plt.plot(bandN,color = colors[i],linestyle=' ',marker =markers[i],markersize=5,label = note[i])
    plt.legend(loc='upper right')
    # plt.show()
    plt.savefig(outputFile,dpi=100)
    plt.close()

if __name__ == "__main__":
    year = '2019'
    stations = ["Dunhuang",
               "Libya1",
               "Libya4",
               "Arabia2",
               "Lanai",
               "Algeria5",
               "Sonora",
               "Algeria3",
               "Mauritania2"]
    for station in stations:
        inputFile = r"D:\temp_10.24.34.219\useless\BRDF_"+year+"_"+station+".txt"
        outputFile = inputFile.replace(".txt",".png")
        bandN_2018 = getBandN(inputFile,year)
        plotBandN(bandN_2018,year,outputFile,station)
