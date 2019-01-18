import h5py
import numpy as N
import os
import sys
from PIL import Image
from matplotlib import colors
from matplotlib import pyplot

def mosiac(PNGname,MIN,MAX):
    im = Image.open(PNGname)
    w,h = im.size
    colorbar = N.loadtxt("./colorbar_"+str(MIN)+"_"+str(MAX)+".txt")

    print "colorbar",colorbar
    im1 = colorbar.squeeze()[:, 1:] / 255.
    color_max = N.max(colorbar[:, 0])
    color_min = N.min(colorbar[:, 0])
    cmapp = colors.ListedColormap(colors=im1)
    cmapp.set_bad(alpha=0)
    # cmapp.set_bad(color="white")
    print cmapp
    print im
    print color_max
    print color_min
    rgba=cmapp(im)
    pyplot.figure(figsize=[15,10])
    ax=pyplot.axes([0.1,0.1,0.8,.8])
    #pyplot.imshow(im,cmap=cmapp)
    pyplot.imshow(im, cmap=cmapp, interpolation='nearest', vmax=color_max, vmin=color_min)
    pyplot.colorbar(cmap=cmapp)
    pyplot.axis('off')
    pyplot.savefig(PNGname, transparent=True,dpi=h/8)
    pyplot.close()

if __name__=="__main__":

    MIN = 270
    MAX = 300
    mosiac("D:\\temp_10.24.4.116\\result_20180625\\all_test.png",MIN,MAX)

