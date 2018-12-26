import matplotlib.pyplot as plt
from matplotlib.cm import cmap_d
import numpy
from PIL import Image

def getAllColorbarsFromPlt():
    outputPath = "D:\\temp_10.24.4.135_xBQ\\colorbar_OCC\\"
    gradient = numpy.linspace(0,1,256)
    gradient = numpy.vstack((gradient,gradient,gradient,gradient,gradient,gradient,gradient,gradient,
                             gradient, gradient, gradient, gradient, gradient, gradient, gradient, gradient))
    for name in cmap_d:
        if "_r" not in name:
            fig, ax = plt.subplots()
            outputColorbar = outputPath + name + ".png"
            cmp = cmap_d[name]
            ax.imshow(gradient,cmap=cmp)
            plt.axis("off")
            # plt.show()
            plt.savefig(outputColorbar)
            plt.close()

def readColorbar(inputPNG,outputTxt):
     data = Image.open(inputPNG)
     data = numpy.array(data,dtype = "i4")
     data = data[240:241,:,:]
     a,x,y = data.shape
     data = numpy.reshape(data,(x,y))
     make = data[:,0] != 255
     make |= data[:,1] !=255
     make |= data[:,2] !=255
     make |= data[:,3] !=255
     data = data[make]
     data = data[:,:3]
     data = numpy.array(data)
     return data
def makeColorbar(colorbar,RW,outputTxt):
    colorbarShape = colorbar.shape
    occ = numpy.linspace(RW["minValue"],RW["maxValue"],colorbarShape[0])
    result = numpy.column_stack((occ,colorbar))
    print result.shape
    numpy.savetxt(outputTxt,result,fmt="%f")
if __name__ == "__main__":
    inputPNG = "D:\\temp_10.24.4.135_xBQ\\colorbar_OCC\\jet.png"
    outputTxt = inputPNG.replace(".png","_0_0.04.txt")
    # getAllColorbarsFromPlt()
    RW412 = {"minValue":0 , "maxValue":0.04}
    RW488 = RW412
    RW551 = RW412
    RW869 = RW412
    colorbar = readColorbar(inputPNG,outputTxt)
    makeColorbar(colorbar,RW412,outputTxt)
