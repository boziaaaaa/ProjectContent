import math
import numpy
from PIL import Image

def readColorbar(inputPNG):
     data = numpy.loadtxt(inputPNG)
     data = data[:,1:]
     return data
def EXP(howmuchColor,minValue,maxValue):
    howmuchColor = howmuchColor + 83
    print howmuchColor,minValue,maxValue
    temperature = numpy.zeros(howmuchColor)
    index = 0
    print howmuchColor
    total = maxValue - minValue
    for x in range(minValue*100000,maxValue*100000,numpy.int(total*100000/(howmuchColor))):
        temperature[index] = math.pow(10,x/100000.0)
        index = index + 1
        if index >= howmuchColor:
            break
    temperature = temperature[temperature>=0.015]
    # temperature = temperature[temperature<=200]
    return temperature
def makeColorbar(colorbar,RW,outputTxt):
    colorbarShape = colorbar.shape
    occ = EXP(colorbarShape[0],RW["minValue"],RW["maxValue"])
    result = numpy.column_stack((occ[:435],colorbar))
    numpy.savetxt(outputTxt,result,fmt="%f")
    # numpy.savetxt(outputTxt,occ,fmt="%f")

if __name__ == "__main__":
    inputPNG = "D:\\temp_10.24.4.135_xBQ\\colorbar_OCC_spectral\\test.txt"
    outputTxt = inputPNG.replace(".txt","hoho.txt")
    # getAllColorbarsFromPlt()
    RW412 = {"minValue":-2 , "maxValue":0}

    colorbar = readColorbar(inputPNG)
    makeColorbar(colorbar,RW412,outputTxt)
