import math
import numpy
from PIL import Image

def readColorbar(inputPNG):
     data = Image.open(inputPNG)
     data = numpy.array(data,dtype = "i4")
     data = data[30:31,::3,:]

     print data.shape
     a,x,y = data.shape
     data = numpy.reshape(data,(x,y))
     make = data[:,0] != 255
     make |= data[:,1] !=255
     make |= data[:,2] !=255
     # make |= data[:,3] !=255
     data = data[make]
     data = data[:,:3]
     data = numpy.array(data)
     return data
def EXP(howmuchColor,minValue,maxValue):
    howmuchColor = howmuchColor
    print howmuchColor,minValue,maxValue
    temperature = numpy.zeros(howmuchColor)
    index = 0
    print howmuchColor
    total = maxValue - minValue
    for x in range(numpy.int(minValue*100000),numpy.int(maxValue*100000),numpy.int(total*100000/(howmuchColor))):
        temperature[index] = math.pow(10,x/100000.0)
        index = index + 1
        if index >= howmuchColor:
            break
    return temperature
def makeColorbar(colorbar,RW,outputTxt):
    colorbarShape = colorbar.shape
    occ = EXP(colorbarShape[0],RW["minValue"],RW["maxValue"])
    result = numpy.column_stack((occ[0:394],colorbar))
    numpy.savetxt(outputTxt,result,fmt="%f")
    # numpy.savetxt(outputTxt,occ,fmt="%f")

if __name__ == "__main__":
    inputPNG = "D:\\temp_10.24.4.135_xBQ\\colorbar_OCC_spectral\\test.JPG"
    outputTxt = inputPNG.replace(".JPG",".txt")
    # getAllColorbarsFromPlt()
    minValue = 0.001
    maxValue = 10
    minV = math.log(10,10)
    maxV = math.log(1000,10)
    print minV,maxV

    RW412 = {"minValue":minV , "maxValue":maxV}

    colorbar = readColorbar(inputPNG)
    makeColorbar(colorbar,RW412,outputTxt)
