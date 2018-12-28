from PIL import Image
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def MakePicture(inputPicture2):
    mp = Basemap(projection="cyl",llcrnrlat=0,urcrnrlat=60,llcrnrlon=90,urcrnrlon=140)
    mp.drawcoastlines()
    plt.savefig(inputPicture2,transparent = True,dpi=100)
def MakeImageTransparent(img):
    # img = Image.open(inputPicture)
    img = img.convert('RGBA')
    img_array = numpy.array(img)
    width,height = img.size
    for i in range(height):
        for j in range(width):
            if numpy.sum(img_array[i,j,:]) == 255*4: #[255 255 255 255]
                img_array[i,j,0] = 155
                img_array[i,j,1] = 155
                img_array[i,j,2] = 155
                img_array[i,j,3] = 0
    img = Image.fromarray(img_array)
    return img

def ImageMerge(inputPicture1,inputPicture2,leftRightCorner):
    img_back = Image.open(inputPicture1)
    img_fore = Image.open(inputPicture2)
    img_fore = MakeImageTransparent(img_fore)
    r,g,b,a = img_fore.split()
    # img_back.paste(img_fore,(100, 100, 740,580),mask=a)
    imageSize = img_fore.size
    left = leftRightCorner[0]
    up = leftRightCorner[1]
    right = left + imageSize[0]
    down = up + imageSize[1]
    img_back.paste(img_fore,(left,up,right,down),mask=a)
    img_back.show()

if __name__=="__main__":
    inputPicture1 = "D:\ProjectContent\\test\FY4A-_AGRI--_N_REGI_1047E_L1C_MTCC_MULT_GLL_20181213050000_20181213051459_1000M_V0001.JPG"
    inputPicture2 = "D:\ProjectContent\\test\\0001.JPG"
    # MakePicture(inputPicture2)
    leftRightCorner = [1000,1000]
    ImageMerge(inputPicture1,inputPicture2,leftRightCorner)
