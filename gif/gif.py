import imageio
import os
import sys
from PIL import Image
import matplotlib.pyplot as plt
def ParseGIF(inputGIF,outputPath):
    tif = imageio.read(inputGIF)
    index = 0
    for i in tif:
        print i.shape
        img = Image.fromarray(i)
        index += 1
        img.save(inputGIF.replace(".gif",str(index).zfill(3)+".png"))
    tif.close
def MakeGIF(inputPNGs,outputFile):
    files_gif = []
    for file in inputPNGs:
        # img = Image.open(file)
        # plt.imshow(img)
        # fileBasename = os.path.basename(file)
        # date = fileBasename.split("_")
        # title =  "EVT_" + date[9] + "_" + date[10]
        # plt.title(title)
        # plt.show()
        gif_each = imageio.imread(file)
        files_gif.append(gif_each)
    imageio.mimsave(outputFile,files_gif,"GIF",duration = 0.1)
if __name__=="__main__":
    inputGIF = r"D:\ProjectContent\gif\ce4.gif"
    outputPath = os.path.dirname(inputGIF)
    inputPNGpath = os.path.dirname(inputGIF)
    inputPNGpath = r"D:\Data_ftp\20190110"


    files = os.listdir(inputPNGpath)
    pngs = []
    outputFile = os.path.join(inputPNGpath,"test_evt.gif")
    for file in files:
        if "EVT" in file and "TOTAL" in file:
            pngs.append(os.path.join(inputPNGpath,file))
    if len(pngs) == 0:
        print "no pngs exist!!"
        sys.exit()
    MakeGIF(pngs,outputFile)


