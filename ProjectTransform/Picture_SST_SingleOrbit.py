import h5py
from PIL import Image
import numpy as N
import sys
import os
from picture_Base import MosaicImage_RGB
# from fileNameToSQL import fileNameToSQL
def find_last(string,str):
    last_position=-1
    while True:
        last_position = last_position + 1
        position=string.find(str,last_position)
        if position==-1:
            return last_position
def input_outputPath(configureFile,YYYYMMDD,DayOrNight):
    f_txt = open(configureFile)
    lines = f_txt.readlines()
    inputPath = ""
    outputPath = ""
    for line in lines:
        if "inputPath_SST_HDF" in line:
            index_begin = line.find('/')
            index_end = find_last(line,'/')
            inputPath = line[int(index_begin):int(index_end)] + YYYYMMDD + "/" + DayOrNight + "/"
        elif "outputPath_SST_PNG" in line:
            index_begin = line.find('/')
            index_end = find_last(line,'/')
            outputPath = line[int(index_begin):int(index_end)] + YYYYMMDD + "/" + DayOrNight + "/"
    return inputPath,outputPath
if __name__ == "__main__":
    YYYYMMDD = sys.argv[1]
    DayOrNight = sys.argv[2]
    configureFile = "/GDS/SSTWORK/ProjectTransform/PARAM/Picture_SST_SingleOrbit.txt"
    inputPath, outputPath = input_outputPath(configureFile,YYYYMMDD,DayOrNight)
    print "inputPath",inputPath
    print "outputPath",outputPath
    if os.path.exists(inputPath) == False:
        print "inputPath do not exist",inputPath
        exit(0)
    HDFfiles = os.listdir(inputPath)
    for HDFfile in HDFfiles:
        if ".HDF" in HDFfile:
            print HDFfile
            input_HDF = inputPath+HDFfile
            output_PNGname = outputPath + HDFfile
            output_PNGname = output_PNGname.replace('.HDF', '.png')
            # MosaicImage_gray(input_HDF,output_PNGname)
            MosaicImage_RGB(input_HDF)

            #write every fileName to SQL
            command = "python /GDS/SSTWORK/ProjectTransform/fileNameToSQL.py "\
                      +output_PNGname+" "+input_HDF+ " "+DayOrNight
            os.system(command)
