import numpy
from PIL import Image
import matplotlib.pyplot as plt
import os
import re
def colorbar_show(colorbar_txt,outputPNG):
    # colorbar_txt = "D:\\temp_10.24.4.135_xBQ\\20171201_self\\colorbar_NASA_final.txt"

    title_index = re.search("colorbar_",colorbar_txt)
    title = colorbar_txt[title_index.start():-4]
    data = numpy.loadtxt(colorbar_txt)
    value_min = numpy.min(data[:,0])
    value_max = numpy.max(data[:,0])
    # print numpy.max(value)
    data = data[:,1:]

    r = data[:,0]
    g = data[:,1]
    b = data[:,2]
    length = len(r)
    r = numpy.vstack((r,r,r,r,r,r,r,r,r,r,r))
    g = numpy.vstack((g,g,g,g,g,g,g,g,g,g,g))
    b = numpy.vstack((b,b,b,b,b,b,b,b,b,b,b))

    t = numpy.zeros((r.shape[0],r.shape[1],3),dtype='uint8')
    t[...,0] = r
    t[...,1] = g
    t[...,2] = b
    # print t.shape
    img = Image.fromarray(t,mode='RGB')
    plt.imshow(img)
    plt.title(title)
    plt.yticks([])
    plt.xticks((0,length),(str(value_min),str(value_max)))
    # plt.show()
    plt.savefig(outputPNG)
    plt.close()
if __name__=="__main__":
    inputPath = r"D:\\temp_10.24.4.135_xBQ\\test\\Ocean_slope_colorbar\\"
    for f in os.listdir(inputPath):
        if ".txt" in f and "new" in f:
            colorbar_txt = os.path.join(inputPath,f)
            print colorbar_txt
            outputPNG = colorbar_txt.replace(".txt",".png")
            colorbar_show(colorbar_txt,outputPNG)