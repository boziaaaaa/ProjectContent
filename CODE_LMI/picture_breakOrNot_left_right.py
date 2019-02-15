#coding=utf8
from PIL import Image
import numpy
import os
import shutil

def getLeftAndRight(imgFile):
    if os.path.exists(imgFile) == False:
        print "do not exist"
        return -1,-1
    img = Image.open(imgFile,"r")
    img_left = img.crop((0,100,300,460))
    img_right = img.crop((300,100,600,460))
    img.close()
    return img_left,img_right

def statics(img):
    img_array = numpy.array(img)
    return numpy.mean(img_array),numpy.var(img_array)

def breakOrNot(img):
    img_left, img_right = getLeftAndRight(file_each)
    mean_left, var_left = statics(img_left)
    mean_right, var_right = statics(img_right)
    img = Image.open(file_each)
    mean_img,var_img = statics(img)
    #左右两侧差异较大 且 全图不为夜晚
    if (var_left / var_right > 10 or var_right / var_left > 10) and \
       (var_right < 100 and mean_right > 10) or  (var_left < 100 and mean_left > 10) and \
       (var_img > 700 and mean_img > 30):
            print mean_left,mean_right,mean_img," ",var_left,var_right,var_img
            return 1
    return 0

if __name__=="__main__":
    inputFiles = []
    inputDate = r"\20190211"
    inputPath = r"D:\Data_ftp"+inputDate
    inputPath_break = r"D:\Data_ftp" + inputDate + "_break"
    inputPath_nobreak = r"D:\Data_ftp" + inputDate + "_nobreak"
    file_each_new = ""
    if os.path.exists(inputPath_break) == False:
        os.mkdir(inputPath_break)
    if os.path.exists(inputPath_nobreak) == False:
        os.mkdir(inputPath_nobreak)
    for file in os.listdir(inputPath):
        if "1B_LAD-_SING_NUL_" in file:
            file_each = os.path.join(inputPath,file)
            breakOrNotBreak = breakOrNot(file_each)
            if breakOrNotBreak == 1:
                file_each_new = os.path.join(inputPath_break, file)
                shutil.copy(file_each, file_each_new)
            else:
                file_each_new = os.path.join(inputPath_nobreak,file)
            # shutil.copy(file_each,file_each_new)

