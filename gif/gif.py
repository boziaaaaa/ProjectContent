import imageio
import os
import sys
from PIL import Image
class GIF(object):
    def __init__(self,t=0.1):
        self.timeResolution = t

    def ParseGIF(self,inputGIF,outputPath):
        tif = imageio.read(inputGIF)
        index = 0
        for i in tif:
            print i.shape
            img = Image.fromarray(i)
            index += 1
            img.save(inputGIF.replace(".gif",str(index).zfill(3)+".png"))
        tif.close

    def MakeGIF(self,inputPNGs,outputFile):
        files_gif = []
        for file in inputPNGs:
            gif_each = imageio.imread(file)
            files_gif.append(gif_each)
        imageio.mimsave(outputFile,files_gif,"GIF",duration = self.timeResolution)

def GetPNGS(inputPNGpath):
    files = os.listdir(inputPNGpath)
    pngs = []
    for file in files:
        # if "EVT" in file and "TOTAL" in file:
        if "LAD" in file :
            pngs.append(os.path.join(inputPNGpath, file))
    if len(pngs) == 0:
        print "no pngs exist!!"
        sys.exit()
    return pngs
if __name__=="__main__":
    timeResolution = 0.02
    inputDate = "20190117"
    inputPNGpath = r"D:\Data_ftp\\"+inputDate
    outputFile = r"D:\Data_ftp\gif_test\lad_"+inputDate+"_timeResolution_"+str(timeResolution)+"s.gif"

    pngs = GetPNGS(inputPNGpath)
    makeGif = GIF(timeResolution)
    makeGif.MakeGIF(pngs,outputFile)


