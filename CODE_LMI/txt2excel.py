
#-*-coding=utf-8-*-
import xlrd
import xlwt
import re

def writeEXCEL(excelFile):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0, 1, 'test text')
    sheet.write(1, 1, 'test text')
    wbk.save(excelFile)
    return 0

def ReadTxt(txtFile):
    # f = open(txtFile)
    with open(txtFile) as f:
        for line in f.readlines():
            line = line.split("     ")
            fileName = line[0]
            frameNum = line[1]
            evnetNum = line[2]
            print fileName,frameNum,evnetNum
    return 0


if __name__=="__main__":
    for i in range(2,29):
        inputTXTFile = "F:\\Tongji_TiJiao\\LIOF_201802_\\L2_LIO_201802"+str(i).zfill(2)+".txt"
        outputExcelFile = inputTXTFile.replace(".txt",".xls")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        sheet.write(0, 0, u'文件名称')
        sheet.write(0, 1, u'真实闪电个数')
        sheet.write(0, 2, u'虚假闪电个数')
        index = 1
        with open(inputTXTFile) as f:
            # print inputTXTFile
            for line in f.readlines():
                line = line.split("     ")
                if len(line) < 3 :
                    continue
                fileName = line[0]
                frameNum = line[1]
                evnetNum = line[2]
                sheet.write(index, 0, fileName)
                sheet.write(index, 1, frameNum)
                sheet.write(index, 2, evnetNum)
                index = index + 1
        wbk.save(outputExcelFile)