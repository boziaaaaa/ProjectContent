from PIL import Image
import numpy
import math


# PNG = Image.open('D:\\temp_10.24.4.135_xBQ\\colorbar_OCC_blue.PNG')
# outputTxt = "D:\\temp_10.24.4.135_xBQ\\colorbar_OCC.txt"
PNG = Image.open('D:\\temp_10.24.4.135_xBQ\\colorbar_OCC.PNG')
outputTxt = "D:\\temp_10.24.4.135_xBQ\\colorbar_OCC.txt"

colorbar = numpy.array(PNG)
colorbar = colorbar[1,:,0:3]
colorbar = numpy.transpose(colorbar)
# print colorbar

howmuchColor = colorbar.shape[1]
temperature = numpy.zeros(howmuchColor)
list_temp = []
color_last = [0,0,0]
for i in range(howmuchColor): #remove repeat
    if color_last[0] == colorbar[:,i][0] and color_last[1] == colorbar[:,i][1] and color_last[2] == colorbar[:,i][2]:
        # print color_last,colorbar[:,i]
        continue
    color_last = colorbar[:,i]
    list_temp.append(color_last)
list_temp = numpy.array(list_temp)
print list_temp

colorbar = list_temp
colorbar = numpy.transpose(colorbar)
colorbar = colorbar[:,::5]
howmuchColor = colorbar.shape[1]
temperature = numpy.zeros(howmuchColor)

index = 0
print howmuchColor
# for x in range(-1*100000,1*100000,numpy.int(2*100000/(howmuchColor))):
#     # print x,index
#     temperature[index] = math.pow(10,x/100000.0)
#     index = index + 1
#     if index >= howmuchColor:
#         break
min = -1
max = 1
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
    f.write("\n")