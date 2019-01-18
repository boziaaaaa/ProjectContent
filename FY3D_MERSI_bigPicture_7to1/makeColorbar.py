import numpy
data = numpy.loadtxt("D:\\untitled3\\colorbar.txt")
data = data[:,1:]
len = data.shape[0]
print len
minT = 270
maxT = 300
Temperature = []
for i in range(len):
    Temp = minT+float(maxT-minT)*i/len
    Temperature.append([Temp,data[i,0],data[i,1],data[i,2]])

Temperature = numpy.array(Temperature)
print Temperature

# numpy.savetxt("D:\\untitled3\\colorbar_280_310.txt",Temperature)
numpy.savetxt("D:\\untitled3_FY3D_MERSI_qinZong\\colorbar_"+str(minT)+"_"+str(maxT)+".txt",Temperature)

