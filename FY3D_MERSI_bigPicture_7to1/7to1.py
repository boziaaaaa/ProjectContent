import h5py
import numpy as N
import os
import sys
from PIL import Image
from matplotlib import colors
from matplotlib import pyplot

PNGPath = "D:\\temp_10.24.4.116\\result_20180625\\outputPNG_250\\"
files = os.listdir(PNGPath)
ims = [Image.open(PNGPath+f) for f in files]
print ims[0].mode
width = 14401
height = 9201
result = Image.new(ims[0].mode,(width,height))
for i,im in enumerate(ims):
    print i,im
    result.paste(im,box=(2000*i,0))
result.save("D:\\temp_10.24.4.116\\result_20180625\\"+"all.png")