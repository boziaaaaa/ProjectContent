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

def Excel_temp(inputExcelFile,ouputExcelFile):

    txtFileHandle = open(ouputExcelFile,"a")
    fileHandle = xlrd.open_workbook(inputExcelFile)
    sheet = fileHandle.sheets()[0]
    timeStart = sheet.col_values(1)[1:]
    trueOrFalse = sheet.col_values(4)[1:]

    month_last = 0
    day_last = 0
    total_0 = 0
    total_1 = 0
    index = 0
    for i in timeStart:
        a = re.search(r"(.*?)\d/", i)
        b = re.search(r"/(.*?)(\d)/", i)
        month = a.group()[:-1]
        day = b.group()[1:-1]

        if (day != day_last or month != month_last) and (month_last != 0):
            outString = "2017."+str(month_last) + "." + str(day_last) + "      " + str(total_0) + "      " + str(total_1) + "        " + str(total_0 + total_1) + "\n"
            txtFileHandle.write(outString)
            total_0 = 0
            total_1 = 0

        if trueOrFalse[index] == 0:
            total_0 = total_0+1
        else:
            total_1 = total_1+1

        month_last = month
        day_last = day
        index = index + 1
    outString = "2017."+str(month_last) + "." + str(day_last) + "      " + str(total_0) + "      " + str(
        total_1) + "        " + str(total_0 + total_1) + "\n"
    txtFileHandle.write(outString)
    txtFileHandle.close()
    return 0




def Excel(inputExcelFile,ouputExcelFile):

    txtFileHandle = open(ouputExcelFile,"a")
    fileHandle = xlrd.open_workbook(inputExcelFile)
    sheet = fileHandle.sheets()[0]
    timeStart = sheet.col_values(1)[1:]
    trueOrFalse = sheet.col_values(4)[1:]

    month_last = 0
    day_last = 0
    total_0 = 0
    total_1 = 0
    index = 0
    for i in timeStart:
        a = re.search(r"(.*?)\d/", i)
        b = re.search(r"/(.*?)(\d)/", i)
        month = a.group()[:-1]
        day = b.group()[1:-1]

        if (day != day_last or month != month_last) and (month_last != 0):
            outString = "2017."+str(month_last) + "." + str(day_last) + "      " + str(total_0) + "      " + str(total_1) + "        " + str(total_0 + total_1) + "\n"
            txtFileHandle.write(outString)
            total_0 = 0
            total_1 = 0

        if trueOrFalse[index] == 0:
            total_0 = total_0+1
        else:
            total_1 = total_1+1

        month_last = month
        day_last = day
        index = index + 1
    outString = "2017."+str(month_last) + "." + str(day_last) + "      " + str(total_0) + "      " + str(
        total_1) + "        " + str(total_0 + total_1) + "\n"
    txtFileHandle.write(outString)
    txtFileHandle.close()
    return 0

if __name__=="__main__":
    inputExcelFile = "D:/temp_10.24.189.195/F4ALREGJumpR.xlsx"
    ouputExcelFile = "D:/temp_10.24.189.195/F4ALREGJumpR_SuccessOrFalse.txt"
    Excel(inputExcelFile,ouputExcelFile)