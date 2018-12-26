from PIL import Image
import numpy
import math
import re

def colorbar(txtFile,outputTxt,min,max):

    colorbar = test(txtFile)

    colorbar = numpy.transpose(colorbar)
    howmuchColor = colorbar.shape[1]

    # min = -100
    # max = 100
    temperature = numpy.linspace(min*100,max*100,howmuchColor)
    print temperature
    print len(temperature)
    print howmuchColor
    temperature = temperature/100.0
    temperature = numpy.transpose(temperature)

    f = open(outputTxt,"w")
    for i in range(0,howmuchColor):
        f.write(str(round(temperature[i],3)))
        f.write("   ")
        f.write(str(colorbar[0,i]))
        f.write("   ")
        f.write(str(colorbar[1,i]))
        f.write("   ")
        f.write(str(colorbar[2,i]))
        # f.write("\n")

def test(txtFile):
    rgb = []
    with open(txtFile) as f:
        lines = f.readlines()
        for line in lines:
            print line
            # data = re.split(",| ",line)
            data = re.split(" ",line)
            # rgb.append([data[1],data[3],data[5]])
            rgb.append([data[1],data[2],data[3]])

    return rgb
if __name__ == "__main__":
    txtFile = r"D:\temp_10.24.4.135_xBQ\test\Ocean_slope_colorbar\colorbar_OCC_Ocean_YS443.txt"
    outputTxt = r"D:\temp_10.24.4.135_xBQ\test\Ocean_slope_colorbar\colorbar_OCC_Ocean_YS443_new.txt"
    minValue = 0.001
    maxValue = 10
    colorbar(txtFile,outputTxt,minValue,maxValue)