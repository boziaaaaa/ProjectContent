#coding=utf-8
from netCDF4 import Dataset
import xlwt
import os
import numpy
import sys
def writeEXCEL(excelFile,files_L1B,flash_num,falseFlash_num):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0, 0, u"文件名")
    sheet.write(0, 1, u"真实闪电总数")
    sheet.write(0, 2, u"虚假闪电总数")
    index = 0
    for f in files_L1B:
        sheet.write(index+1, 0,f)
        sheet.write(index+1, 1, flash_num[index])
        sheet.write(index+1, 2, falseFlash_num[index])
        index = index + 1
    wbk.save(excelFile)
    return 0

if __name__=="__main__":
    # inputTime = "20170401"
    # inputPath = "F:\\TongJi\\L2data\\LIOF\\REGX\\2017\\"+inputTime+"\\"
    # outputPath = "D:\\temp_10.24.189.195\\"

    inputTime = sys.argv[1]
    inputPath = sys.argv[2]
    outputPath = sys.argv[3]
    excelFile = outputPath + "L2_LIOE"+inputTime+".xls"

    flash_num = []
    falseFlash_num = []
    output_fileName = []
    files_L1B = os.listdir(inputPath)

    for f in files_L1B:
        if inputTime in f and ".NC" in f:
            filename = inputPath + f
            try:
                fileHandle = Dataset(filename, mode='r')
            except:
                continue
            dataset = fileHandle.variables["DQF"][:]

            flash_num.append(len(dataset[dataset == 0]))
            falseFlash_num.append(len(dataset[dataset != 0]))
            output_fileName.append(f)
            fileHandle.close()

    writeEXCEL(excelFile,output_fileName,flash_num,falseFlash_num)
