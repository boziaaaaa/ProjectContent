#-*-coding=UTF-8-*-
import h5py
import numpy as N
from PIL import Image
from matplotlib import colors
from matplotlib import pyplot
# from matplotlib import
def Trans(inputArray,MIN,MAX):
      single = {65535.0:[255,255,255]}
      colorbar = N.loadtxt("./colorbar_"+str(MIN)+"_"+str(MAX)+".txt")
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
    # N.save("D:\\temp_10.24.4.116\\result\\temp\\")
    OutputImg = Image.fromarray(rgbArray,mode="RGBA")
    print PNGname
    OutputImg.save(PNGname)

    # im = Image.open(PNGname)
    # colorbar = N.loadtxt("./colorbar2.txt")
    #
    # im1 = colorbar.squeeze()[:, 1:] / 255.
    # color_max = N.max(colorbar[:, 0])
    # color_min = N.min(colorbar[:, 0])
    # cmapp = colors.ListedColormap(colors=im1)
    # cmapp.set_bad(alpha=0)
    # cmapp.set_bad(color="white")
    #
    # pyplot.imshow(im, cmap=cmapp, interpolation='nearest', vmax=color_max, vmin=color_min)
    # pyplot.colorbar()
    #
    # pyplot.axis('off')
    # pyplot.savefig(PNGname, transparent=True)
    # pyplot.close()

    return 0

if __name__=="__main__":

    MIN = 270
    MAX = 300

    inputFile = "D:\\temp_10.24.4.116\\result\\FY3D_MERSI_201805131750_250_proj.HDF"
    # bandnameS = ["EVB10800","EVB12000"]
    bandnameS = ["EVB10800"]
    data = 0
    hdf_in = h5py.File(inputFile)

    startIndex = 0
    for i in xrange(7):
        startIndex =  2000*i
        endIndex = startIndex + 2000
        print startIndex
        print endIndex
        for bandname in bandnameS:
            data = hdf_in[bandname].value[:]
            if endIndex > 12000:
                data = data[:,12000:]
            else:
                print startIndex,endIndex-1
                data = data[:,startIndex:endIndex-1]
            Slope = hdf_in[bandname].attrs["slope"]
            mask = N.where(data == 65535)
            print data.shape
            print Slope
            data = data * Slope
            data[mask] = 65535
            outputFile = inputFile.replace(".HDF",bandname+".png")
            outputFile = inputFile.replace(".HDF",bandname+"_"+str(startIndex)+"_"+str(endIndex)+"_"+str(MIN) + "_" + str(MAX)+".png")
            outputFile = outputFile.replace("result\\","result_20180625\\outputPNG_250\\")
            Image_RGB(data,outputFile,MIN,MAX)

    hdf_in.close()