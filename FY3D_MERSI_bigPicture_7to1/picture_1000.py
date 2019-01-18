#-*-coding=UTF-8-*-
import h5py
import numpy as N
from PIL import Image
from matplotlib import colors
from matplotlib import pyplot
# from matplotlib import
def Trans(inputArray,MIN,MAX):
      # MIN = 280
      # MAX = 290
      single = {65535.0:[255,255,255]}
      colorbarFile = "./colorbar_"+str(MIN)+"_"+str(MAX)+".txt"
      print "colorbarFile",colorbarFile
      colorbar = N.loadtxt(colorbarFile)
      print "1111",colorbar[0,0]
      print "2222",colorbar[1,0]
      step = colorbar[1,0] - colorbar[0,0]
      step = step + step/5
      print step
      gradient = {}
      len = colorbar.shape[0] # rows number in colorbar
      for i in range(0,len):
         gradient[colorbar[i,0]] =  list(colorbar[i,1:4]) #make a dict ,same as single(above)
      inputArray = N.array(inputArray)
      r = N.zeros(inputArray.shape)
      g = N.zeros(inputArray.shape)
      b = N.zeros(inputArray.shape)
      for key in single:
        r[inputArray == key] = single[key][0]
        g[inputArray == key] = single[key][1]
        b[inputArray == key] = single[key][2]
      mask_150 = inputArray<MIN
      inputArray[mask_150] = MIN
      mask_300 = inputArray >MAX
      mask_300 &= inputArray < 65535
      inputArray[mask_300] = MAX  #the range of temperature is 0~32

      for key in gradient:
        if key >= MIN and key < MAX:#temperature is 0~32
          mask = inputArray >= key
          # mask &= inputArray < (key+0.31) #interval of colorbar is 0.3
          mask &= inputArray < (key+step) #interval of colorbar is 0.3

          r[mask] = int(gradient[key][0])
          g[mask] = int(gradient[key][1])
          b[mask] = int(gradient[key][2])
      return r,g,b

def Image_RGB(BandData,PNGname,MIN,MAX):
    r, g, b = Trans(BandData,MIN,MAX)  # bb bigger Image Redder
    Height, Width = BandData.shape
    f = 255
    rgbArray = N.zeros((Height, Width, 4), 'uint8')
    rgbArray[..., 0] = r
    rgbArray[..., 1] = g
    rgbArray[..., 2] = b
    rgbArray[..., 3] = ((r!=f) | (g!=f) | (b!=f)).astype('u1')*255

    OutputImg = Image.fromarray(rgbArray,mode="RGBA")
    OutputImg.save(PNGname)

    im = Image.open(PNGname)
    # colorbar = N.loadtxt("./colorbar2.txt")
    # colorbar = N.loadtxt("./colorbar_280_300.txt")
    colorbarFile = "./colorbar_" + str(MIN) + "_" + str(MAX) + ".txt"
    print "colorbarFile33",colorbarFile
    colorbar = N.loadtxt(colorbarFile)

    im1 = colorbar.squeeze()[:, 1:] / 255.
    color_max = N.max(colorbar[:, 0])
    color_min = N.min(colorbar[:, 0])
    cmapp = colors.ListedColormap(colors=im1)
    # cmapp.set_bad(alpha=0)
    cmapp.set_bad(color="white")
    print "color_min,color_max",color_min,color_max
    pyplot.imshow(im, cmap=cmapp, interpolation='nearest', vmax=color_max, vmin=color_min)
    pyplot.colorbar()

    pyplot.axis('off')
    pyplot.savefig(PNGname, transparent=True)
    pyplot.close()

    return 0

if __name__=="__main__":
    MIN = 270
    MAX = 310
    inputFile = "D:\\temp_10.24.4.116\\result_20180625\\FY3D_MERSI_201805131750_1000_proj.HDF"
    # colorbar = ".txt"
    bandnameS = ["EVB3800","EVB4050","EVB7200","EVB8550"]
    data = 0
    hdf_in = h5py.File(inputFile)
    for bandname in bandnameS:
        data = hdf_in[bandname].value[:]
        Slope = hdf_in[bandname].attrs["slope"]
        mask = N.where(data == 65535)
        data = data * Slope
        data[mask] = 65535
        outputFile = inputFile.replace(".HDF",bandname+"_"+str(MIN) + "_" + str(MAX)+".png")
        outputFile = outputFile.replace("result_20180625\\","result_20180625\\outputPNG\\")

        tt = data[data<65535]
        print bandname,min(tt),"------",max(tt)
        # data[data>MAX]=MAX
        # data[data<MIN]=MIN
        Image_RGB(data,outputFile,MIN,MAX)
    hdf_in.close()

