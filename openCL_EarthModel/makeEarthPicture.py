#coding=utf8
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from PIL import Image
# pl = plt.figure(figsize=(12,6))
# plt.axis('off')
# mp = Basemap()
# mp.bluemarble()
# # mp.drawcoastlines()
fileName = "blue.jpg"
# plt.savefig(fileName,dpi=200,bbox_inches='tight')

img = Image.open(fileName)
# img = img.resize((8192,4096))
img = img.resize((1024,1024))

fileName = "blue2.jpg"

img.save(fileName)