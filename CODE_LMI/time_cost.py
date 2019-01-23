#-*-coding=utf-8-*-
import xlrd
import xlwt
import re
import datetime


def writeEXCEL(excelFile,data):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    for i in range(len(data)):
        print data[i]
        sheet.write(i, 0, str(data[i]))
    wbk.save(excelFile)
    return 0

def time(inputExcelFile):
    fileHandle = xlrd.open_workbook(inputExcelFile)
    sheet = fileHandle.sheets()[0]
    timeStart = sheet.col_values(1)[1:]
    timeEnd = sheet.col_values(2)[1:]
    diff = []
    # 转换成时间数组
    for i in range(len(timeStart)):
        start_each = datetime.datetime.strptime(timeStart[i], "%m/%d/%Y %H:%M:%S")
        if timeEnd[i] != "":
            end_each = datetime.datetime.strptime(timeEnd[i], "%m/%d/%Y %H:%M:%S")
            print
            diff.append(end_each-start_each)
        else:
            diff.append("")
    return diff

if __name__=="__main__":
    inputExcelFile = u"D:/temp_10.24.189.195/programTime/L3频数跃变产品20180101_20180306.xlsx"
    # ouputExcelFile = "D:/temp_10.24.189.195/programTime/F4ALREGJumpR_SuccessOrFalse.txt"
    ouputExcelFile = "D:/temp_10.24.189.195/programTime/ttt.xls"

    data = time(inputExcelFile)
    writeEXCEL(ouputExcelFile,data)