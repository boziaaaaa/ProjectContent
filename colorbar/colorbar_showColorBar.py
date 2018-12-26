
# import Image
from PIL import Image
import matplotlib.pyplot as plt
import numpy

inputFile = "D:\\temp_10.24.4.135_xBQ\\SST\\colorbar_sst.txt"
data = numpy.loadtxt(inputFile)
data = data[:,2:]
# data = data[2:,:]
print data.shape
r = data[:,0]
g = data[:,1]
b = data[:,2]
r = numpy.vstack((r,r,r,r,r,r,r,r,r,r))
g = numpy.vstack((g,g,g,g,g,g,g,g,g,g))
b = numpy.vstack((b,b,b,b,b,b,b,b,b,b))
sst = numpy.zeros((10,176,3),dtype="uint8")
sst[...,0] = r
sst[...,1] = g
sst[...,2] = b
img = Image.fromarray(sst,mode='RGB')
# img.show()
# img.save(inputFile.replace(".txt",".png"))
plt.imshow(img)
# plt.axis("1")
# plt.xlabel('xxxxxxxxxxx')
plt.xticks([0,175],["-2","35"])
plt.yticks([])
plt.savefig(inputFile.replace(".txt",".png"))

plt.show()
# print r.shape